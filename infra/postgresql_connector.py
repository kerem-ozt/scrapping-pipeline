import psycopg2

class PostgresConnector:
    def __init__(self, host='postgres', db='postgres', password='postgres', user='postgres', port=5432):
        self.host = host
        self.db = db
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connect(self):
        if not self.connection:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.db,
                user=self.user,
                password=self.password,
                port=self.port
            )
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
