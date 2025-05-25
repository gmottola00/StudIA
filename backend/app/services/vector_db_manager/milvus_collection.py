"""
Modulo per la gestione delle collection del Milvus Vector Store

Authors: Gianmarco Mottola
Date: //2024

"""
from pymilvus import (
    DataType,
    utility,
    MilvusClient
)
import json
from typing import List, Dict, Any, Optional
from .embedding import EmbeddingModelOLLAMA
from .milvus_connection import MilvusConnectionManager
from modules.pdf_parser.pdf_parser import PDFParser
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging
import time
import numpy as np

logging.basicConfig(level=logging.INFO)

class MilvusHandlerCollection:
    def __init__(self, 
                embedding_dim: int, 
                collection_name: str, 
                connection_manager: MilvusConnectionManager, 
                directory: str,
                client: MilvusClient):
        """
        Inizializza il Milvus Handler per la gestione delle collection del db vettoriale
        
        Parameters
        ----------
        embedding_dim: int
            Dimensione degli embedding
        collection_name: str
            Nome della collezione
        directory : str
            Path dei file in input (.pdf)
        Client : MilvusClient 
            MilvusClient per la gestione del Milvus Standalone
        Return
        ---------
        self: MilvusHandlerCollection
            instanza della classe per gestire le collection del Milvus
        """
        self.client = client
        self.embedding_dim = embedding_dim
        self.collection_name = collection_name
        chunk_size = 1300
        chunk_overlap = np.round(chunk_size * 0.10, 0)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,  # Adjust the chunk size as needed
            chunk_overlap=chunk_overlap  # Overlap between chunks to maintain context
        )
        self.embedding =  EmbeddingModelOLLAMA()
        self.connection_manager = connection_manager
        self.alias = self.connection_manager.get_alias()
        self.pdf_parser = PDFParser()
        self.directory = directory

        # Verifica se la collection_name è valida
        if self.directory is None:
            raise ValueError(f"Collection name non valida: {self.collection_name}")

        self.create_collection()
    
    
    def create_collection(self):
        """
        Crea la collezione con un determinato Schema e indice
        """
        # controlla se la collezione esiste, se non esiste la crea
        has = utility.has_collection(self.collection_name, using=self.alias)
        if not has:
            # Create schema
            schema = self.client.create_schema(auto_id=True, enable_dynamic_field=False)

            # Add fields to schema
            schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True, auto_id=True)
            schema.add_field(field_name="context", datatype=DataType.VARCHAR, max_length=65535)
            schema.add_field(field_name="search_context", datatype=DataType.VARCHAR, max_length=65535, enable_analyzer=True, enable_match=True)
            schema.add_field(field_name="vector_context", datatype=DataType.FLOAT_VECTOR, dim=self.embedding_dim)
            
            schema.add_field(field_name="file_name", datatype=DataType.VARCHAR, max_length=1024)
            schema.add_field(field_name="chunk_id", datatype=DataType.INT64)

            schema.add_field(field_name="ente_appaltante", datatype=DataType.VARCHAR, max_length=1024)
            schema.add_field(field_name="cig", datatype=DataType.VARCHAR, max_length=1024)
            schema.add_field(field_name="oggetto", datatype=DataType.VARCHAR, max_length=1024)
            schema.add_field(field_name="importo_base_asta", datatype=DataType.VARCHAR, max_length=1024)
            schema.add_field(field_name="scadenza_contratto", datatype=DataType.VARCHAR, max_length=1024)
            schema.add_field(field_name="scadenza_chiarimenti", datatype=DataType.VARCHAR, max_length=1024)

            # Set up index params for vector field
            index_params = self.client.prepare_index_params()
            index_params.add_index(
                field_name="vector_context",
                metric_type="COSINE",
                index_type="AUTOINDEX"
            )

            # Create collection with defined schema
            self.client.create_collection(
                collection_name=self.collection_name,
                schema=schema,
                index_params=index_params
            )
            self.load_collection()
        else:
            # Load the existing collection    
            self.load_collection()


    def load_collection(self):
        """
        Carica la collection
        """
        self.client.load_collection(
            collection_name=self.collection_name
        )

    def search_gare(self, query_text: str, top_k: int = 5) -> list[dict]:
        """
        Esegue una ricerca semantica + strutturata nel DB vettoriale Milvus.
        Parameters
        ----------
        query_text : str
            Testo della query da confrontare semanticamente.
        filters : dict
            Filtri strutturati sui metadati (es. {"ente_appaltante": "Regione Puglia"}).
        top_k : int
            Numero massimo di risultati da restituire.
        Returns
        -------
        List[dict]
            Lista di risultati pertinenti con testo, punteggio e metadati associati.
        """
        # Step 1 - Genera embedding della query
        query_vector = self.embedding.embed_query(query_text)

        # Step 2 - Esegui ricerca su Milvus
        results = self.client.search(
            collection_name=self.collection_name,
            data=[query_vector],
            anns_field="vector_context",
            search_params={"params": {"metric_type": "COSINE", "nprobe": 10, "ef": 128}},
            limit=top_k,
            output_fields=[
                "context", "search_context", "file_name", "ente_appaltante", "cig",
                "oggetto", "importo_base_asta", "scadenza_contratto", "scadenza_chiarimenti"
            ]
        )
    
        # Step 3 - Post-processing (estrae info utili da ogni risultato)
        output = []
        for hit in results[0]:
            output.append({
                "distance": hit['distance'],
                "context": hit['entity']['context'],
                "search_context": hit['entity']['search_context'],
                "file_name": hit['entity']["file_name"],
                "ente_appaltante": hit['entity']["ente_appaltante"],
                "cig": hit['entity']["cig"],
                "oggetto": hit['entity']["oggetto"],
                "importo_base_asta": hit['entity']["importo_base_asta"],
                "scadenza_contratto": hit['entity']["scadenza_contratto"],
                "scadenza_chiarimenti": hit['entity']["scadenza_chiarimenti"]
            })
        return output
    

    def migration(self):
        """
        Metodo per fare la migrazione dei file PDF contenuti nella cartella di input nel VectorDB
        """
        logging.info("Inizio migrazione")
        start_time = time.time()
        self.extract_data_from_json()
        end_time = time.time()
        logging.info(f"Fine migrazione in {end_time - start_time:.2f} secondi")

    def extract_data_from_json(self):
        """
        Metodo per leggere la directory dove sono contenuti i file, 
        estrapola i dati, li pulisce e li inserisce nel vector db
        """
        for filename in os.listdir(self.directory):
            if filename.endswith(".json"):
                file_path = os.path.join(self.directory, filename)
                try:
                    logging.info(f"Elaboro file: {file_path}")
                    chunks = self.load_dict_from_json(file_path)
                    self.process_structured_chunks_and_insert(chunks)
                except json.JSONDecodeError as e:
                    logging.info(f"Error decoding JSON from file {file_path}: {e}")
                except Exception as e:
                    logging.info(f"An error occurred while processing file {file_path}: {e}")


    def process_structured_chunks_and_insert(self, chunks: list[dict]):
        """
        Inserisce nel DB vettoriale i chunk già pre-processati con metadati ed embedding.

        Parameters
        ----------
        chunks : list[dict]
            Lista di dizionari con struttura:
            {
                "context": str,
                "embedding": list[float],
                "metadata": dict
            }
        """
        start_time = time.time()
        data_to_insert = []
        for chunk in chunks:
            meta = chunk.get("metadata", {})
            record = {
                "context": chunk["context"],
                "search_context": chunk["search_context"][0],
                "vector_context": chunk["vector_context"],
                "file_name": meta.get("file_name", ""),
                "chunk_id": meta.get("chunk_id", 0),
                "ente_appaltante": meta.get("ente_appaltante", ""),
                "cig": meta.get("cig", ""),
                "oggetto": meta.get("oggetto", ""),
                "importo_base_asta": meta.get("importo_base_asta", ""),
                "scadenza_contratto": meta.get("scadenza_contratto", ""),
                "scadenza_chiarimenti": meta.get("scadenza_chiarimenti", "")
            }
            data_to_insert.append(record)

        # Inserimento in Milvus
        self.client.insert(
            collection_name=self.collection_name,
            data=data_to_insert
        )
        end_time = time.time()
        logging.info(f"Inserted {len(data_to_insert)} records into '{self.collection_name}' in {end_time - start_time:.2f} seconds.")


    @staticmethod
    def save_dict_to_json(data, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    
    @staticmethod
    def load_dict_from_json(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            loaded_data = json.load(file)
        return loaded_data

    def get_directory(self):
        return self.directory