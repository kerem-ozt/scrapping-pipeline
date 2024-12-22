# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from infra.postgresql_connector import PostgresConnector
from infra.redis_connector import RedisConnector
from infra.mongo_connector import MongoConnector 

class JobsPipeline:
    def __init__(self):
        self.postgres = None
        self.redis_connector = None
        self.conn = None
        self.cur = None

    def open_spider(self, spider):
        self.postgres = PostgresConnector(
            host='192.168.1.44',
            db='postgres',
            user='postgres',
            password='postgres',
            port=5432
        )
        self.conn = self.postgres.connect()
        self.cur = self.conn.cursor()

        self.redis_connector = RedisConnector()  # Varsayılan 127.0.0.1:6379/db=0
        self.redis_connector.connect()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS raw_table (
            id SERIAL PRIMARY KEY,
            slug TEXT,
            title TEXT,
            description TEXT,
            raw_json JSONB
        );
        """
        self.cur.execute(create_table_query)
        self.conn.commit()

    def process_item(self, item, spider):
        # Not: Duplicate kontrolü için diger kolonlari incele
        slug = item.get('slug')
        if slug:
            existing = self.redis_connector.get_item(slug)

            if existing:
                spider.logger.info(f"Duplicate item found: {slug}")
                return item

            else:
                self.redis_connector.set_item(slug, "True")

        insert_query = """
        INSERT INTO raw_table (slug, title, description, raw_json)
        VALUES (%s, %s, %s, %s)
        """
        raw_json_str = json.dumps(dict(item), ensure_ascii=False)

        self.cur.execute(insert_query, (
            item.get('slug'),
            item.get('title'),
            item.get('description'),
            raw_json_str
        ))
        self.conn.commit()

        return item

    def close_spider(self, spider):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

class MongoPipeline:
    def __init__(self):
        self.mongo_connector = None
    
    def open_spider(self, spider):
        self.mongo_connector = MongoConnector(host='mongo', db_name='my_mongo_db')
        self.mongo_connector.connect()

    def process_item(self, item, spider):
        self.mongo_connector.db["raw_collection"].insert_one(dict(item))
        spider.logger.info(f"Inserted into Mongo raw_collection.")
        return item
    
    def close_spider(self, spider):
        if self.mongo_connector:
            self.mongo_connector.close()
