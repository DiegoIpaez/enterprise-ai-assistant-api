import logging

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.config.settings import settings

logger = logging.getLogger("database")


class MongoDBClient:
    def __init__(self):
        self.client: MongoClient | None = None
        self.db: Database | None = None
        self.collection: Collection | None = None

    def connect(self):
        try:
            database = settings.MONGODB_DATABASE
            self.client = MongoClient(settings.MONGODB_URI)
            self.db = self.client[database]
            logger.info(f"Conectado a MongoDB: {database}")
        except Exception as error:
            logger.error(f"Error al conectar a MongoDB: {error!s}")

    def disconnect(self):
        try:
            if self.client is not None:
                self.client.close()
            logger.info("Desconectado de MongoDB")
        except Exception as error:
            logger.error(f"Error al desconectar de MongoDB: {error!s}")


db_client = MongoDBClient()
