from contextlib import asynccontextmanager
from logging.config import dictConfig
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src.app.routes as api_v1
from src.ai.embeddings import EmbeddingService
from src.ai.llm.phi3_client import Phi3Client
from src.config.logger import LOGGING_CONFIG
from src.config.settings import settings
from src.database import db_client

dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing embedding model...")
    embedding_service = EmbeddingService()
    embedding_service.initialize()
    logger.info("Embedding model initialized successfully")

    logger.info("Initializing Phi-3 model...")
    phi3_client = Phi3Client()
    phi3_client.initialize()
    logger.info("Phi-3 model initialized successfully")

    await db_client.connect()

    yield
    await db_client.disconnect()


app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    lifespan=lifespan,
    redirect_slashes=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"], description="Health check")
def health():
    return {
        "status": "ok",
        "version": settings.API_VERSION,
    }


app.include_router(api_v1.router)
