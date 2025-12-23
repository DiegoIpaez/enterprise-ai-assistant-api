import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.config.settings import settings

logger = logging.getLogger("database")


class MongoDBClient:
    def __init__(self):
        self.client: AsyncIOMotorClient | None = None

    async def connect(self):
        try:
            database = settings.MONGODB_DATABASE
            self.client = AsyncIOMotorClient(settings.MONGODB_URI)

            await init_beanie(
                database=self.client[database],
                document_models=[],
            )
            logger.info(f"Connected to MongoDB: {database}")
        except Exception as error:
            logger.error(f"Error connecting to MongoDB: {error!s}")
            raise

    async def disconnect(self):
        try:
            if self.client is not None:
                self.client.close()
            logger.info("Disconnected from MongoDB")
        except Exception as error:
            logger.error(f"Error disconnecting from MongoDB: {error!s}")


db_client = MongoDBClient()
