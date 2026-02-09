import logging
from sentence_transformers import SentenceTransformer

logger = logging.getLogger("ai-embeddings")


class EmbeddingService:
    _instance = None
    _model: SentenceTransformer | None = None
    _model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    _embedding_dimension: int = 384

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self) -> None:
        if self._model is None:
            self._model = SentenceTransformer(self._model_name)
        logger.info(f"Embedding model {self._model_name} loaded")

    def is_initialized(self) -> bool:
        """Verify if the model is initialized."""
        return self._model is not None

    def generate_embedding(self, text: str) -> list[float]:
        if not self.is_initialized():
            raise RuntimeError(
                "Embedding model not initialized. Call initialize() first."
            )

        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        embedding = self._model.encode(text, convert_to_numpy=True)  # type: ignore
        return embedding.tolist()  # type: ignore

    @property
    def embedding_dimension(self) -> int:
        """Retorna la dimensión esperada de los embeddings."""
        return self._embedding_dimension
