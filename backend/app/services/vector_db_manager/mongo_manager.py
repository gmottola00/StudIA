from pymongo import MongoClient

MONGO_URI = "mongodb+srv://gianmarcomottola:fhAUmTdvZJ3pD0KH@tendertest.m8pybsm.mongodb.net/"


class MongoManager():
    def __init__(self):
        self._connect("vector_db", "tender_test_molise")

    def _connect(self, db_name, collection_name):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]




    
