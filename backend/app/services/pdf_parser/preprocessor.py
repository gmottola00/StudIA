import os
from typing import List, Dict, Any
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PDFReader
from ollama import Client
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import Document
from llama_index.core.prompts import PromptTemplate
import multiprocessing
import logging
import json
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
import os
import json
import logging
from typing import List, Dict, Any
from modules.generative.consts import QUERY_SEARCH_META, SYS_PROMPT_META, QUERY_CONTEXT_META

logging.basicConfig(level=logging.INFO)


class MetadataExtractor:
    def __init__(self, model_name="phi4-mini:3.8b"):
        self.llm = Client(host="http://localhost:11434")
        self.model_name = model_name
        # Prompt template per l’estrazione dei metadati da tutto il testo
        self.prompt_template = PromptTemplate(QUERY_CONTEXT_META)
        
    def extract(self, text: str) -> Dict[str, Any]:
        prompt = self.prompt_template.format(context=text[:8000])  # tagliato se troppo lungo
        response = self.llm.chat(
                model=self.model_name,
                messages=[
                    {'role': 'system', 'content': SYS_PROMPT_META},
                    {'role': 'user', 'content': prompt}
                ],
                options={
                    'temperature': 0.0
                }
        ) 
        raw = response['message']['content']
        # Pulisci da eventuali blocchi ```json o testo extra
        if raw.startswith("```json"):
            raw = raw.removeprefix("```json").removesuffix("```").strip()
        elif raw.startswith("```"):
            raw = raw.removeprefix("```").removesuffix("```").strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            logging.warning(f"[MetadataExtractor] JSON malformato: {e}\nContenuto:\n{raw}")
            return {
                "ente_appaltante": "",
                "cig": "",
                "oggetto": "",
                "importo_base_asta": "",
                "scadenza_contratto": "",
                "scadenza_chiarimenti": ""
            }
       

class Preprocessor:
    def __init__(self, output_dir, embedding_model="nomic-embed-text", llm_model="phi4-mini:3.8b"):
        self.output_dir = output_dir
        chunk_size = 1300 # prima era 512
        chunk_overlap = np.round(chunk_size * 0.10, 0) # prima era 20
        self.splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.embedder = OllamaEmbedding(model_name=embedding_model, base_url="http://localhost:11434")
        self.metadata_extractor = MetadataExtractor(model_name=llm_model)

    def load_documents(self, directory:str) -> List[Document]:
        reader = SimpleDirectoryReader(
            directory,
            required_exts=[".pdf"],
            file_extractor={".pdf": PDFReader()}
        )
        return reader.load_data()
    
    def contain_metadata_keyword(self, full_text_lower):
        KEYWORD = [
            "ente appaltante", "cig", "importo base",
            "oggetto", "scadenza"
        ]
        return any(keyword in full_text_lower for keyword in KEYWORD)
    

    def process_document(self, doc) -> List[Dict[str, Any]]:
        """
        Elabora un singolo documento, estraendo i chunk, arricchendo il testo con i metadati non nulli,
        generando gli embedding e salvando i risultati in un file JSON (senza sovrascrivere se non ci sono nuovi chunk).
        
        Parameters
        ----------
        doc : Document
            Un oggetto Document (ad es. proveniente da SimpleDirectoryReader) che contiene il testo del documento e i metadati.
        
        Returns
        -------
        List[Dict[str, Any]]
            Una lista di record (dizionari) generati per il documento, ognuno contenente:
                - "context": il testo originale del chunk,
                - "search_context": il testo arricchito con metadati inline,
                - "vector_context": il vettore embedding generato dal testo arricchito,
                - "metadata": il dizionario dei metadati associato al chunk.
        """
        filename = doc.metadata.get("file_name", "unknown")
        full_text = doc.text.lower()
        #verifica se il testo contiene parole chiave prima di chiamare l'LLM
        if not self.contain_metadata_keyword(full_text):
            logging.info(f"[{filename}] Nessuna keyword rilevante trovata, skip estrazione metadati.")
            return [] 
        # Estrai i metadati dal documento tramite il MetadataExtractor (che restituisce un dizionario valido)
        metadata_dict = self.metadata_extractor.extract(full_text)
        logging.info(f"[{filename}] Estratti metadati: {metadata_dict}")
        # Estrai i chunk dal documento usando il text splitter
        chunks = self.splitter.get_nodes_from_documents([doc])
        # Costruisci il nuovo testo "enriched" per ciascun chunk aggiungendo metadati non vuoti
        enriched_texts = []
        for chunk in chunks:
            enriched_context = chunk.text.lower()
            # Per ogni chiave, se il valore non è vuoto, lo aggiunge al testo
            for key, value in metadata_dict.items():
                if key not in ["file_name", "chunk_id"] and isinstance(value, str) and value.strip():
                    enriched_context += f" [{key}: {value.strip()}]"
            enriched_texts.append(enriched_context)

        # Genera gli embedding in batch utilizzando il testo arricchito
        embeddings = self.embedder.get_text_embedding_batch(enriched_texts)
        # Inizializza una lista per i record elaborati per questo documento
        doc_results = []
        # Definisci i campi chiave da controllare per considerare un chunk valido
        key_fields = [
            "ente_appaltante", "cig", "importo_base_asta", "oggetto",
            "scadenza_contratto", "scadenza_chiarimenti"
        ]

        for i, chunk in enumerate(chunks):
            # Costruisce il dizionario dei metadati per il chunk
            chunk_metadata = {
                "file_name": filename,
                "chunk_id": i,
                **metadata_dict
            }

            # Conta il numero di campi chiave non vuoti
            non_empty_fields = [chunk_metadata.get(k, "").strip() 
                                for k in key_fields if chunk_metadata.get(k, "").strip()]
            if len(non_empty_fields) < 2:
                logging.info(f"[{filename}][chunk {i}] Chunk scartato: solo {len(non_empty_fields)} metadati validi.")
                continue
            record = {
                "context": chunk.text,               # Testo originale del chunk
                "search_context": enriched_texts[i], # Testo arricchito, usato per full-text
                "vector_context": embeddings[i],     # Embedding generato dal search_context
                "metadata": chunk_metadata
            }
            doc_results.append(record)
        return doc_results

    def process_all_documents(self, directory: str) -> List[Dict[str, Any]]:
        """
        Elabora tutti i file PDF presenti in una directory.
        Legge i documenti dalla directory, li processa in parallelo e restituisce una lista combinata di tutti i record elaborati.
        Al termine, salva un file JSON unico contenente tutti i record elaborati.
        Parameters
        ----------
        directory : str
            La directory contenente i file PDF da processare.
        Returns
        -------
        List[Dict[str, Any]]
            Lista di record (chunk elaborati) da tutti i documenti.
        """
        os.makedirs(self.output_dir, exist_ok=True)
        
        documents = self.load_documents(directory)
        all_results = []

        max_workers = min(multiprocessing.cpu_count(), 4)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.process_document, doc): doc for doc in documents}
            for future in as_completed(futures):
                try:
                    doc_results = future.result()
                    all_results.extend(doc_results)
                except Exception as exc:
                    doc = futures[future]
                    filename = doc.metadata.get("file_name", "unknown")
                    logging.error(f"Errore durante il processing di {filename}: {exc}")

        # Salva tutti i risultati in un unico file JSON
        output_path = os.path.join(self.output_dir, "all_results_3.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        logging.info(f"Salvati complessivamente {len(all_results)} record in: {output_path}")
        return all_results
    


    def process_with_augmented_context(self, directory:str) -> List[Dict[str, Any]]:
        """
        Elabora i documenti, estrae i chunk e li arricchisce con i metadati non null.
        Genera gli embedding dai testi arricchiti e inserisce i dati nel DB (o li salva in un JSON).
        Restituisce una lista di dizionari con struttura:
            {
                "context": <testo originale chunk>,
                "vector_context": <embedding dal testo arricchito>,
                "metadata": 
            }
        """
        documents = self.load_documents(directory)
        all_results = []
        os.makedirs(self.output_dir, exist_ok=True)
        for doc in documents:
            filename = doc.metadata.get("file_name", "unknown")
            full_text = doc.text
            full_text = full_text.lower()
            logging.info(f"{type(full_text)}")
            # controllo early exit per evitare di chiamare LLM inutilmente
            if not self.contain_metadata_keyword(full_text):
                logging.info(f"Nessuna Keyword trovata")
                continue

            # Estrai i metadati dal documento (la funzione extract restituisce un dizionario valido)
            metadata_dict = self.metadata_extractor.extract(full_text)
            logging.info(f"[{filename}] Estratti metadati: {metadata_dict}")

            # Estrai i chunk dal documento (usando il text splitter)
            chunks = self.splitter.get_nodes_from_documents([doc])

            # Costruisci il nuovo testo "enriched" per ciascun chunk:
            # aggiungi al testo originale solo i metadati non vuoti.
            enriched_texts = []
            for chunk in chunks:
                enriched_context = chunk.text

                # Per ogni coppia key:value, aggiungi se value non è vuoto e se il campo è rilevante
                for key, value in metadata_dict.items():
                    # Escludi i campi già gestiti in metadata separati, ad esempio "file_name" e "chunk_id"
                    if key not in ["file_name", "chunk_id"]:
                        if isinstance(value, str) and value.strip():
                            enriched_context += f" [{key}: {value.strip()}]"
                enriched_texts.append(enriched_context)
            
            # Genera gli embedding in batch usando il testo arricchito
            embeddings = self.embedder.get_text_embedding_batch(enriched_texts)
            doc_results = []  # Per salvare i record di questo documento

            # Specifica quali campi chiave vuoi verificare per decidere se un chunk è valido
            key_fields = [
                "ente_appaltante", "cig", "importo_base_asta",
                "oggetto", "scadenza_contratto", "scadenza_chiarimenti"
            ]

            for i, chunk in enumerate(chunks):
                # Costruisci il dizionario dei metadati per il chunk
                chunk_metadata = {
                    "file_name": filename,
                    "chunk_id": i,
                    **metadata_dict
                }

                # Conta quanti metadati rilevanti NON sono vuoti
                non_empty_fields = [chunk_metadata.get(k, "").strip() 
                                    for k in key_fields if chunk_metadata.get(k, "").strip()]
                if len(non_empty_fields) < 2:
                    logging.info(f"[{filename}][chunk {i}] Chunk scartato: solo {len(non_empty_fields)} metadati validi.")
                    continue

                record = {
                    "context": chunk.text,  # conserva il testo originale (non arricchito) per riferimento
                    "search_context": enriched_texts,
                    "vector_context": embeddings[i],
                    "metadata": chunk_metadata
                }
                doc_results.append(record)
                all_results.append(record)

            # Salva/aggiorna il JSON per questo documento, senza sovrascrivere i record già presenti
            output_path = os.path.join(self.output_dir, f"{filename}.json")
            if os.path.exists(output_path):
                with open(output_path, "r", encoding="utf-8") as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        existing_data = []
            else:
                existing_data = []
            updated_data = existing_data + doc_results
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(updated_data, f, indent=2, ensure_ascii=False)
            logging.info(f"[{filename}] Salvato/aggiornato in: {output_path}")
        return all_results