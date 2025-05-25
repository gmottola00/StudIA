from typing import List, Optional
import os
from ollama import Client
import logging
logging.basicConfig(level=logging.INFO)

# Imposta il livello di logging per 'httpx' a 'WARNING' per sopprimere i messaggi 'INFO'
logging.getLogger("httpx").setLevel(logging.WARNING)

class EmbeddingModelOLLAMA:
    def __init__(self, host: Optional[str] = None, model: Optional[str] = None):
        """
        Initializes the embedding model.

        Args:
            host (Optional[str]): The host URL for the Ollama client.
            model (Optional[str]): The name of the embedding model to use.
        """
        self.host = host or os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = model or os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
        self.llm = Client(host=self.host)


    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Embeds a list of texts into vectors.

        Args:
            texts (List[str]): List of texts to embed.

        Returns:
            List[List[float]]: List of embedding vectors.
        """
        embeddings = []
        for text in texts:
            embedding = self.embed_query(text)
            if embedding:
                embeddings.append(embedding)
            else:
                logging.error(f"Embedding fallito per il testo: {text}")
        return embeddings

    
    def embed_query(self, query:str) -> List[float]:
        """
        Embeds a query into a vector.

        Args:
            query (str): The query to embed.

        Returns:
            List[float]: The embedding vector.
        """
        try:
            response = self.llm.embeddings(model=self.model, prompt=query)
            embedding = response.embedding
            return embedding
        except Exception as e:
            logging.error(f"Errore durante l'embedding del testo: {e}")
            return []
        
