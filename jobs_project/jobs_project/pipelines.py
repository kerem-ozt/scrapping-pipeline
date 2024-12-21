# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from infra.postgresql_connector import PostgresConnector

class JobsPipeline:
    def __init__(self):
        self.postgres = None
        self.conn = None
        self.cur = None

    def open_spider(self, spider):
        self.postgres = PostgresConnector(
            host='192.168.1.44',
            db='canaria',
            user='postgres',
            password='postgres',
            port=5432
        )
        self.conn = self.postgres.connect()
        self.cur = self.conn.cursor()

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
