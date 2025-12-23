from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from src.utils.pagination_formatter import PaginationResult

from .ai_knowledge_model import AIKnowledge, KnowledgeType, Lenguage
from .ai_knowledge_schema import (
    AIKnowledgeCreate,
    AIKnowledgeUpdate,
)
from .ai_knowledge_service import AIKnowledgeService

router = APIRouter(prefix="/ai-knowledge", tags=["AI Knowledge"])

service = AIKnowledgeService()


@router.post("/", response_model=AIKnowledge, status_code=status.HTTP_201_CREATED)
async def create_knowledge(knowledge_data: AIKnowledgeCreate) -> AIKnowledge:
    return await service.create(knowledge_data)


@router.get("/{id}", response_model=AIKnowledge)
async def get_knowledge(id: str) -> AIKnowledge:
    knowledge = await service.get_by_id(id)
    if not knowledge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Knowledge not found"
        )
    return knowledge


@router.get("/", response_model=PaginationResult[AIKnowledge])
async def get_all_knowledge(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    disabled: bool = Query(False),
    language: Annotated[Lenguage | None, Query(alias="language")] = None,
    knowledge_type: Annotated[KnowledgeType | None, Query(alias="type")] = None,
):
    return await service.get_all(
        page=page,
        limit=limit,
        disabled=disabled,
        language=language,
        knowledge_type=knowledge_type,
    )


@router.put("/{id}", response_model=AIKnowledge)
async def update_knowledge(id: str, update_data: AIKnowledgeUpdate) -> AIKnowledge:
    knowledge = await service.update(id, update_data)
    if not knowledge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Knowledge not found"
        )
    return knowledge


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_knowledge(id: str) -> None:
    await service.delete(id)
