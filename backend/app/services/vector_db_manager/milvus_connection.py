"""
Pattern Singleton per avere una gestione singola (unica instanza) della connessione al server di Milvus

Authors: Gianmarco Mottola
Date: 03/2025

"""

from pymilvus import (
    connections,
    utility
)
import logging

logging.basicConfig(level=logging.INFO)

class MilvusConnectionManager:
    _instance = None

    def __new__(cls, alias="default", host='localhost', port='19530'):
        if cls._instance is None:
            cls._instance = super(MilvusConnectionManager, cls).__new__(cls)
            cls._instance.alias = alias
            cls._instance.host = host
            cls._instance.port = port
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        """
        Crea la connessione
        """
        connections.connect(alias=self.alias, host=self.host, port=self.port)
        #self.conn=connections.connect(alias=self.alias, host=self.host, port=self.port)
        logging.info(f"Connesso a Milvus come alias: '{self.alias}'")

    def _disconnect(self):
        """
        Si disconnette dal Milvus Standalone
        """
        try:
            connections.remove_connection(alias=self.alias)
            logging.info("Correttamente disconnesso dal server")
        except Exception as e:
            logging.info(f"Disconnessione dal server non riuscita: {e}")

    def get_alias(self):
        """
        Ritorna l'alias della connessione

        Author: Gianmarco Mottola
        """
        return self.alias