from datetime import datetime
from enum import Enum

from beanie import Document, Insert, Replace, before_event
from pydantic import Field


class KnowledgeType(str, Enum):
    FAQ = "FAQ"
    DOC = "DOC"
    BUSINESS_RULE = "BUSINESS_RULE"


class Language(str, Enum):
    ENGLISH = "en"
    SPANISH = "es"


class AIKnowledge(Document):
    content: str
    embedding: list[float] | None = None
    type: KnowledgeType = Field(default=KnowledgeType.FAQ)
    tags: list[str] = Field(default_factory=list)
    language: Language = Field(default=Language.SPANISH)
    disabled: bool = Field(default=False)
    deleted: bool = Field(default=False)
    embedding: list[float] | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "ai_knowledges"
        use_cache = True
        cache_expiration_time = 3600

    @before_event(Insert)
    def set_created_at(self):
        self.created_at = self.created_at or datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @before_event(Insert, Replace)
    def set_updated_at(self):
        self.updated_at = datetime.utcnow()

    @before_event(Replace, Insert)
    def validate_embedding_for_active_documents(self):
        if not self.disabled and not self.deleted and self.embedding is None:
            raise ValueError(
                "Active knowledge documents must have an embedding. "
                "Generate embedding before saving."
            )
