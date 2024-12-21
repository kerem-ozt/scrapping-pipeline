import csv
import json
import os
from infra.postgresql_connector import PostgresConnector

def export_raw_table_to_csv(csv_filename="jobs_export.csv"):
    """
    PostgreSQL'deki 'raw_table' tablosundan id, slug ve raw_json alanlarını
    çekip bir CSV dosyasına yazar.
    """
    pg = PostgresConnector(
        host='192.168.1.44',
        db='canaria',
        user='postgres',
        password='postgres',
        port=5432
    )
    conn = pg.connect()
    cur = conn.cursor()

    query = """
        SELECT id, slug, raw_json
        FROM raw_table
        ORDER BY id ASC;
    """
    cur.execute(query)
    rows = cur.fetchall() 

    with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "slug", "raw_json"])

        for row in rows:
            _id, slug, raw_data = row
            writer.writerow([_id, slug, raw_data])

    cur.close()
    conn.close()

    print(f"Export completed! File saved as: {csv_filename}")


if __name__ == "__main__":
    export_raw_table_to_csv()
