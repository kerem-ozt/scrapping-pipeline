# Scrapy Pipeline Project

This project is designed to collect data using **Scrapy** and simultaneously store it in **PostgreSQL**, **Redis**, and **MongoDB** while performing **duplicate checks**. Docker Compose is used to launch all services (Scrapy, PostgreSQL, Redis, MongoDB) within containers. Additionally, the project includes a `query.py` file to export data from the databases (PostgreSQL and MongoDB) into **CSV** format.

## Project Overview

- **Scrapy**: Reads JSON sources (e.g., `s01.json`, `s02.json`), captures each “job” record through a spider like `job_spider`, and yields them as **Item** objects.
- **PostgreSQL**: Stores data in a table named `raw_table`.
- **Redis**: Performs duplicate checks based on the `slug` field by setting/getting Redis keys.
- **MongoDB**: Optionally stores data in a collection named `raw_collection`.
- **`query.py`**: Provides a script to export data from PostgreSQL and MongoDB into CSV files.

## Directory Structure

```plaintext
scrapping-pipeline/
├── data/
│   ├── s01.json
│   └── s02.json
├── infra/
│   ├── mongo_connector.py
│   ├── postgresql_connector.py
│   └── redis_connector.py
├── jobs_project
│   ├── jobs_project
│   │   ├── __init__.py
│   │   ├── items.py
│   │   ├── middlewares.py
│   │   ├── pipelines.py
│   │   ├── settings.py
│   │   └── spiders
│   │   	├── __init__.py
│   │   	└── json_spider.py
│   └── scrapy.cfg
├── query.py
├── docker-compose.yml
├── dockerfile
├── requirements.txt
├── .gitignore
├── .dockerignore
├── LICENSE
├── README.md
└── .env
```

- **data/**: Your JSON data files (e.g., `s01.json`, `s02.json`).
- **infra/**: PostgreSQL, Redis, MongoDB connection files (`mongo_connector.py`, `postgresql_connector.py`, `redis_connector.py`).
- **jobs_project/**: Scrapy project (spiders, pipelines, items, settings, etc.).
- **query.py**: Script for exporting data from databases to CSV.
- **docker-compose.yml**: Docker Compose configurations (Scrapy, PostgreSQL, Redis, MongoDB services).
- **dockerfile**: Docker setup for the Scrapy service.
- **requirements.txt**: Python packages and versions.
- **.env (optional)**: Manage host, port, db, etc., through environment variables.

## Installation and Setup

### 1. Clone the Repository or Obtain the Files

```bash
git clone <REPO_URL>
cd scrapping-pipeline
```

Or copy the project files into a directory.

### 2. (Optional) .env File

Create a `.env` file in the root directory with the following example content:

```bash
# .env file content

# PostgreSQL
POSTGRES_HOST=postgres
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# MongoDB
MONGO_HOST=mongo
MONGO_PORT=27017
MONGO_DB=canaria
```

Docker Compose will pass these environment variables to the containers.

### 3. Build and Launch with Docker Compose

From the project root directory:

```bash
docker-compose build
docker-compose up -d
```

- The `-d` flag runs the services in the background.
- The following services will be started:
  - **scrapy_container** (Scrapy service)
  - **postgres_container** (PostgreSQL)
  - **redis_container** (Redis)
  - **mongo_container** (MongoDB)

### 4. Run the Scrapy Crawler

#### 4.1 Enter the Container and Run

```bash
docker exec -it scrapy_container bash
cd jobs_project
scrapy crawl job_spider
```

This will allow the spider to parse sources like `data/s01.json` and `data/s02.json`. Then:

- **PostgreSQL**: Data is inserted into the `raw_table`.
- **Redis**: Performs duplicate checks based on the `slug`.
- **MongoDB**: Data is inserted into the “raw_collection” collection.

### 5. Check the Databases

- **PostgreSQL**:
  ```bash
  docker exec -it postgres_container bash
  su postgres
  psql
  \c postgres
  \dt
  select * from raw_table limit 5;
  ```
- **Redis**:
  ```bash
  docker exec -it redis_container redis-cli
  KEYS *
  ```
- **MongoDB**:
  ```bash
  docker exec -it mongo_container bash
  mongosh
  show dbs
  use my_mongo_db
  show collections
  db.raw_collection.find()
  ```

### 7. Using `query.py` (CSV Export)

**query.py** facilitates exporting data stored in the databases to CSV files.

For example:

```bash
docker exec -it scrapy_container bash
python query.py
```

- `export_raw_table_to_csv()`: Exports the `raw_table` from PostgreSQL to `jobs_export.csv`.
- `export_mongo_to_csv()`: Exports the `raw_collection` from MongoDB to `mongo_export.csv`.

Upon completion, `jobs_export.csv` and `mongo_export.csv` files will be created.

## Pipeline Structure

### JobsPipeline

1. **open_spider**:  
   - Establishes a connection to PostgreSQL, creates the `raw_table` if it does not exist.
   - Connects to Redis.
2. **process_item**:  
   - Performs duplicate checks based on the `slug` field using Redis.
   - If not a duplicate, inserts the data into PostgreSQL (stores the entire item in the JSONB column).
3. **close_spider**:  
   - Closes the database connections.

### MongoPipeline

1. **open_spider**:  
   - Establishes a connection to MongoDB and accesses the `my_mongo_db.raw_collection` collection.
2. **process_item**:  
   - Inserts the item into the `raw_collection`.
3. **close_spider**:  
   - Closes the MongoDB connection.

These two pipelines are defined in **settings.py** under `ITEM_PIPELINES`, and Scrapy routes the items sequentially to these pipelines.