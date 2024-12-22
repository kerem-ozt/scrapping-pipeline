import os
from pymongo import MongoClient

class MongoConnector:
    def __init__(self):
        self.host = os.getenv('MONGO_HOST', 'mongo')
        self.port = int(os.getenv('MONGO_PORT', 27017))
        self.db_name = os.getenv('MONGO_DB', 'canaria')
        self.client = None
        self.db = None

    def connect(self):
        if not self.client:
            mongo_uri = f"mongodb://{self.host}:{self.port}"
            self.client = MongoClient(mongo_uri)
            self.db = self.client[self.db_name]
        return self.db

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
