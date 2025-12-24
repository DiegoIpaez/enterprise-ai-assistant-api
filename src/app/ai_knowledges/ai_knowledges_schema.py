from pydantic import BaseModel, Field

from .ai_knowledges_model import KnowledgeType, Lenguage


class AIKnowledgeBase(BaseModel):
    content: str
    type: KnowledgeType
    tags: list[str] = Field(default_factory=list)
    language: str
    disabled: bool = Field(default=False)


class AIKnowledgeCreate(AIKnowledgeBase):
    pass


class AIKnowledgeUpdate(BaseModel):
    content: str | None = None
    type: KnowledgeType | None = None
    tags: list[str] | None = None
    language: Lenguage | None = None
    disabled: bool | None = None
