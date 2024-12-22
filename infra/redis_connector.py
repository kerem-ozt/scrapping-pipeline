import redis
import os

class RedisConnector:
    def __init__(self, host='redis', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.client = None

    def connect(self):
        if not self.client:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db
            )
        return self.client

    def set_item(self, key, value):
        self.client.set(key, value)

    def get_item(self, key):
        return self.client.get(key)
