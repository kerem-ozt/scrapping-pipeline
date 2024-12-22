import psycopg2
import os

class PostgresConnector:
    def __init__(self):
        self.host = os.getenv('POSTGRES_HOST', 'postgres')
        self.db = os.getenv('POSTGRES_DB', 'postgres')
        self.user = os.getenv('POSTGRES_USER', 'postgres')
        self.port = int(os.getenv('POSTGRES_PORT', 5432))
        self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.db,
                user=self.user,
                port=self.port
            )
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
