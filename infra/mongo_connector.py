import os
from pymongo import MongoClient

class MongoConnector:
    def __init__(self, 
                 host='mongodb', 
                 port=27017,
                 db_name='my_mongo_db', 
                #  username='admin',
                #  password='adminpassword'

                #  db_name='my_mongo_db', 
                #  username=None, 
                #  password=None
                 ):
        self.host = 'mongodb'
        self.port = 27017
        self.db_name = 'my_mongo_db'
        # self.username = 'admin'
        # self.password = 'adminpassword'
        self.client = None
        self.db = None

    def connect(self):
        if not self.client:
            # if self.username and self.password:
            #     mongo_uri = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}"
            #     self.client = MongoClient(mongo_uri)
            # else:
                # username/password yoksa
                # mongo_uri = f"mongodb://{self.host}:{self.port}"
                # self.client = MongoClient(mongo_uri)
            mongo_uri = f"mongodb://{self.host}:{self.port}"
            self.client = MongoClient(mongo_uri)
            self.db = self.client[self.db_name]
        return self.db

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
