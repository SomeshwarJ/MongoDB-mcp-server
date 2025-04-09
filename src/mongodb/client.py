# File: mongodb/client.py

from pymongo import MongoClient
from pymongo.database import Database
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

client: MongoClient = None
db: Database = None

def connect_to_mongodb(database_url: str):
    global client, db
    try:
        client = MongoClient(database_url)
        parsed_url = urlparse(database_url)
        db_name = parsed_url.path.strip("/") or "test"
        logger.info(f"Connecting to database: {db_name}")
        db = client[db_name]
    except Exception as error:
        logger.error(f"MongoDB connection error: {str(error)}")
        raise

def close_mongodb():
    if client:
        client.close()