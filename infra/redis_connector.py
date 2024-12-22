import redis
import os

class RedisConnector:
    def __init__(self):
        self.host = os.getenv('REDIS_HOST', 'redis')
        self.port = int(os.getenv('REDIS_PORT', 6379))
        self.db = int(os.getenv('REDIS_DB', 0))
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
