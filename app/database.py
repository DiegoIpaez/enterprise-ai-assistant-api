import logging
from typing import Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.config.settings import settings

logger = logging.getLogger("database")


class MongoDBClient:
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self.collection: Optional[Collection] = None

    def connect(self):
        try:
            database = settings.MONGODB_DATABASE
            self.client = MongoClient(settings.MONGODB_URI)
            self.db = self.client[database]
            logger.info(f"Conectado a MongoDB: {database}")
        except Exception as e:
            logger.error(f"Error al conectar a MongoDB: {str(e)}", exc_info=True)

    def disconnect(self):
        try:
            if self.client is not None:
                self.client.close()
            logger.info(f"Desconectado de MongoDB")
        except Exception as e:
            logger.error(f"Error al desconectar de MongoDB: {str(e)}", exc_info=True)


db_client = MongoDBClient()
