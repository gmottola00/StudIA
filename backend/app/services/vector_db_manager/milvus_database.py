"""
Modulo per la gestione dei database del Milvus Vector Store.

Date: 03/2025
"""

from pymilvus import (
    db,
    exceptions,
    MilvusClient
)
import logging

logging.basicConfig(level=logging.INFO)

class MilvusHandlerDatabase:
    """
    Classe per la gestione dei database in Milvus.

    Parameters
    ----------
    db_name : str
        Nome del database da gestire.
    client : MilvusClient
        Oggetto MilvusClient per la gestire il db vettoriale
    """

    def __init__(self, db_name: str, client: MilvusClient):
        self.db_name = db_name
        self.client = client

    def create_database(self):
        """
        Crea un nuovo database in Milvus.

        Raises
        ------
        MilvusException
            Se si verifica un errore durante la creazione del database.
        """
        try:
            db.create_database(self.db_name)
            logging.info(f"Database '{self.db_name}' creato con successo.")
        except exceptions.MilvusException as e:
            logging.error(f"Errore durante la creazione del database '{self.db_name}': {e}")
            raise

    def use_database(self):
        """
        Seleziona il database corrente per le operazioni successive.

        Raises
        ------
        MilvusException
            Se il database non esiste o si verifica un errore durante la selezione.
        
        """
        try:
            db.using_database(self.db_name)
            logging.info(f"Utilizzo del database '{self.db_name}'.")
        except exceptions.MilvusException as e:
            logging.error(f"Errore durante la selezione del database '{self.db_name}': {e}")
            raise

    def list_databases(self):
        """
        Restituisce una lista di tutti i database esistenti.

        Returns
        -------
        List[str]
            Lista dei nomi dei database.

        Raises
        ------
        MilvusException
            Se si verifica un errore durante l'elenco dei database.
        
        """
        try:
            databases = db.list_database()
            logging.info(f"Elenco dei database: {databases}")
            return databases
        except exceptions.MilvusException as e:
            logging.error(f"Errore durante l'elenco dei database: {e}")
            raise

    def drop_database(self):
        """
        Elimina il database specificato.

        Raises
        ------
        MilvusException
            Se il database non esiste o si verifica un errore durante l'eliminazione.

        """
        try:
            db.drop_database(self.db_name)
            logging.info(f"Database '{self.db_name}' eliminato con successo.")
        except exceptions.MilvusException as e:
            logging.error(f"Errore durante l'eliminazione del database '{self.db_name}': {e}")
            raise

    def get_db_name(self):
        """
        Restituisce il nome del database attualmente gestito.

        Returns
        -------
        str
            Nome del database.

        """
        return self.db_name
    
    def drop_collection(self, collection: str):
        """
        Fa la drop della collection
        
        Parameters
        -----------
        collection_name: str
            Nome della Collection da droppare

        """
        self.client.drop_collection(collection_name=collection)
        logging.info(f"Dropped collection: {collection}")

    def list_collections(self):
        """
        Per vedere tutte le collection del Client
        
        Returns:
            List delle collections

        """
        res = self.client.list_collections()
        logging.info("============== COLLECTION MANAGMENT ==============")
        logging.info(f"Collections List: {res}")
        return res

    def drop_all_collection(self):
        """
        Per droppare tutte le collection

        """
        for collection in self.list_collections():
            self.drop_collection(collection)
        
    
    def get_collection_data(self, collection_name: str, output_fields: list = None):
        """
        Visualizza tutti i dati di una collection
        
        Parameters:
        -----------
        collection_name: str
            Nome della collection
        output_fields: list, optional
            Lista dei campi da visualizzare. Se None, mostra tutti i campi
            
        Returns:
        --------
        dict
            Dizionario contenente i dati della collection

        """
        # Query per ottenere tutti i dati
        res = self.client.query(
            collection_name=collection_name,
            output_fields=output_fields,  # Se None, restituisce tutti i campi
            limit=100
        )
        
        logging.info(f"============== COLLECTION DATA ==============")
        logging.info(f"Collection: {collection_name}")
        logging.info(f"Data: {res}")
        
        return res
    
    def get_all_collection_data(self, collection_name: str, output_fields: list = None, batch_size: int = 100):
        """
        Visualizza tutti i dati di una collection usando l'iteratore
        
        Parameters:
        -----------
        collection_name: str
            Nome della collection
        output_fields: list, optional
            Lista dei campi da visualizzare
        batch_size: int, optional
            Dimensione del batch per l'iterazione
            
        Returns:
        --------
        list
            Lista contenente tutti i dati della collection
        """
        results = []
        
        iterator = self.client.query_iterator(
            collection_name=collection_name,
            output_fields=output_fields,
            batch_size=batch_size
        )
        
        while True:
            batch = iterator.next()
            if not batch:
                break
            results.extend(batch)
        
        logging.info(f"============== COLLECTION DATA ==============")
        logging.info(f"Collection: {collection_name}")
        logging.info(f"Record:\n {results}")
        logging.info(f"Total records: {len(results)}")
        
        return results
