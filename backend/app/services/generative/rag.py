from typing import List, Dict, Any, Optional
import json
from ollama import Client
import logging
from services.vector_db_manager.milvus_collection import MilvusHandlerCollection
from services.vector_db_manager.embedding import EmbeddingModelOLLAMA
from services.generative.consts import QUERY_CONTEXT, QUERY_SEARCH, SYS_PROMPT, QUERY_CONTEXT_META, QUERY_SEARCH_META, SYS_PROMPT_META
logging.basicConfig(level=logging.INFO)


class RagSystem:
    def __init__(self, milvus: MilvusHandlerCollection, embedding: EmbeddingModelOLLAMA):
        """
        Inizializza il RAG system con le configurazioni Milvus e embedding
            
        Parameters
        ----------
        milvus: MilvusHandler
            Instanza della classe per gestire il db vettoriale
        emebdding: EmbeddingModel
            Instanza della classe per gestire gli embedding
            
        Return
        ---------
        self: RagSystem
            instanza della classe per gestire il RAG

        Author: Gianmarco Mottola
        """
        self.embedding = embedding
        self.milvus = milvus
        # Initialize the Ollama LLM
        self.llm = Client(host="http://localhost:11434")


    def retrieve(self, query: str) -> str:
        """
        Metodo per ricercare sul VectorDB il contesto

        Args:
            query(str) : Domanda dell'utente

        Returns:
            context : str 
            risultato della ricerca

        Author: Gianmarco Mottola
        """
        results = self.milvus.search_gare(query)
        logging.info(f"====== RISULTATO RICERCA ====== \n {results}")
        # Costruisci il contesto dai documenti recuperati
        context = " ".join([item['search_context'] for item in results])
        return context


    def get_json_from_llm(self, model: str) -> dict:
        """
        Gestisce la query di un utente e restituisce la risposta generata.
        
        Parameters
        ----------
        model: str
            modello da interrogare
            
        Return
        ---------
        answer: dict
            Risposta generata dall'LLM
        """
        answer = self.generate_gara_json(model)
        try:
            return json.loads(answer.strip())
        except Exception as e:
            logging.warning(f"Errore nel parsing JSON: {e}")
            return answer


    def generate_gara_json(self, model:str) -> str:
        """
        Genera un json chiamando LLM 
        
        Author: Gianmarco Mottola

        Parameters
        ----------
        model: str
            modello da interrogare

        Returns:
            str: La risposta generata dall'LLM.
        """

        # Preparazione del system prompt dello user prompt
        context = self.retrieve(QUERY_SEARCH_META)
        query_context = QUERY_CONTEXT_META.replace("{context}", context)
        response = self.llm.chat(
                model=model,
                messages=[
                    {'role': 'system', 'content': SYS_PROMPT_META},
                    {'role': 'user', 'content': query_context}
                ],
                options={
                    'temperature': 0.0
                }
            ) 
        
        # Return della risposta generate
        return response['message']['content']