from pymongo import MongoClient

class MongoDBConfig:
    def __init__(self, uri: str, database_name: str):
        self.client = MongoClient(uri)
        self.database = self.client[database_name]

    def get_collection(self, collection_name: str):
        return self.database[collection_name]
