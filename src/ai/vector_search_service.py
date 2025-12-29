
from src.ai.embeddings import EmbeddingService
from src.app.ai_knowledges.ai_knowledges_model import AIKnowledge, Language
from src.config.settings import settings
from src.database import db_client


class VectorSearchResult:
    def __init__(self, document: AIKnowledge, score: float):
        self.document = document
        self.score = score


class VectorSearchService:
    _instance = None
    _index_name: str = "ai_knowledge_embedding_index"
    _embedding_dimension: int = 384

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._embedding_service = EmbeddingService()

    async def search(
        self,
        query: str,
        limit: int = 5,
        num_candidates: int = 100,
        language: Language | None = None,
        min_score: float | None = None,
    ) -> list[VectorSearchResult]:
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        if not self._embedding_service.is_initialized():
            raise RuntimeError(
                "Embedding model not initialized. Call initialize() first."
            )

        if db_client.client is None:
            raise RuntimeError("MongoDB client not connected")

        query_embedding = self._embedding_service.generate_embedding(query)

        filter_conditions = {
            "disabled": False,
            "deleted": False,
        }

        if language:
            filter_conditions["language"] = language  # type: ignore

        vector_search_stage = {
            "index": self._index_name,
            "path": "embedding",
            "queryVector": query_embedding,
            "numCandidates": num_candidates,
            "limit": limit,
        }

        if filter_conditions:
            vector_search_stage["filter"] = filter_conditions

        pipeline = [
            {
                "$vectorSearch": vector_search_stage,
            },
            {
                "$addFields": {
                    "score": {"$meta": "vectorSearchScore"},
                },
            },
        ]

        database = db_client.client[settings.MONGODB_DATABASE]
        collection = database[AIKnowledge.Settings.name]

        results = []
        async for doc in collection.aggregate(pipeline):
            score = doc.get("score", 0.0)

            if min_score is not None and score < min_score:
                continue

            doc_without_score = {k: v for k, v in doc.items() if k != "score"}

            knowledge = AIKnowledge(**doc_without_score)
            results.append(VectorSearchResult(document=knowledge, score=score))

        return results

    async def search_by_embedding(
        self,
        query_embedding: list[float],
        limit: int = 5,
        num_candidates: int = 100,
        language: Language | None = None,
        min_score: float | None = None,
    ) -> list[VectorSearchResult]:
        if not query_embedding:
            raise ValueError("Query embedding cannot be empty")

        if len(query_embedding) != self._embedding_dimension:
            raise ValueError(
                f"Query embedding must have {self._embedding_dimension} dimensions"
            )

        if db_client.client is None:
            raise RuntimeError("MongoDB client not connected")

        filter_conditions = {
            "disabled": False,
            "deleted": False,
        }

        if language:
            filter_conditions["language"] = language  # type: ignore

        vector_search_stage = {
            "index": self._index_name,
            "path": "embedding",
            "queryVector": query_embedding,
            "numCandidates": num_candidates,
            "limit": limit,
        }

        if filter_conditions:
            vector_search_stage["filter"] = filter_conditions

        pipeline = [
            {
                "$vectorSearch": vector_search_stage,
            },
            {
                "$addFields": {
                    "score": {"$meta": "vectorSearchScore"},
                },
            },
        ]

        database = db_client.client[settings.MONGODB_DATABASE]
        collection = database[AIKnowledge.Settings.name]

        results = []
        async for doc in collection.aggregate(pipeline):
            score = doc.get("score", 0.0)

            if min_score is not None and score < min_score:
                continue

            doc_without_score = {k: v for k, v in doc.items() if k != "score"}

            knowledge = AIKnowledge(**doc_without_score)

            results.append(VectorSearchResult(document=knowledge, score=score))

        return results
