from src.ai.embeddings import EmbeddingService
from src.ai.vector_search_service import VectorSearchService, VectorSearchResult
from src.utils.pagination_formatter import (
    PaginationParams,
    PaginationResult,
    pagination_formatter,
)

from .ai_knowledges_model import AIKnowledge, KnowledgeType, Language
from .ai_knowledges_schema import (
    AIKnowledgeCreate,
    AIKnowledgeUpdate,
)


class AIKnowledgeService:
    def __init__(self):
        self._embedding_service = EmbeddingService()
        self._vector_search_service = VectorSearchService()
    
    async def create(self, knowledge_data: AIKnowledgeCreate) -> AIKnowledge:
        knowledge_dict = knowledge_data.model_dump()
        
        try:
            embedding = self._embedding_service.generate_embedding(knowledge_dict["content"])
            knowledge_dict["embedding"] = embedding
        except Exception as e:
            raise ValueError(f"Failed to generate embedding: {str(e)}") from e
        
        ai_knowledge = AIKnowledge(**knowledge_dict)
        await ai_knowledge.save()
        return ai_knowledge

    async def get_by_id(self, id: str) -> AIKnowledge | None:
        ai_knowledge = await AIKnowledge.get(id)
        if ai_knowledge and not ai_knowledge.deleted:
            return ai_knowledge
        return None

    async def get_all(
        self,
        page: int = 1,
        limit: int = 10,
        show_all: bool = False,
        disabled: bool = False,
        language: Language | None = None,
        knowledge_type: KnowledgeType | None = None,
    ) -> PaginationResult[AIKnowledge]:
        query_filters = {}
        if disabled:
            query_filters["disabled"] = disabled
        if language:
            query_filters["language"] = language
        if knowledge_type:
            query_filters["type"] = knowledge_type
        query_filters["deleted"] = False

        find_query = AIKnowledge.find(query_filters)
        total_records = await find_query.count()

        if show_all is False:
            skip = (page - 1) * limit
            find_query.skip(skip).limit(limit)
        data = await find_query.sort("-created_at").to_list()

        params = PaginationParams(
            data=data,
            page=page,
            limit=limit,
            total_records=total_records,
            show_all=show_all
        )
        pagination_data = pagination_formatter(params)
        return pagination_data

    async def update(
        self, id: str, update_data: AIKnowledgeUpdate
    ) -> AIKnowledge | None:
        ai_knowledge = await AIKnowledge.get(id)
        if not ai_knowledge or ai_knowledge.deleted:
            return None

        update_fields = update_data.model_dump(exclude_unset=True)
        if not update_fields:
            return ai_knowledge

        if "content" in update_fields:
            try:
                embedding = self._embedding_service.generate_embedding(update_fields["content"])
                update_fields["embedding"] = embedding
            except Exception as e:
                raise ValueError(f"Failed to generate embedding: {str(e)}") from e

        updated_document = ai_knowledge.model_copy(update=update_fields)
        await updated_document.save()
        return updated_document

    async def delete(self, id: str) -> bool:
        ai_knowledge = await AIKnowledge.get(id)
        if ai_knowledge and not ai_knowledge.deleted:
            ai_knowledge.deleted = True
            await ai_knowledge.save()
            return True
        return False

    async def search_by_similarity(
        self,
        query: str,
        limit: int = 5,
        language: Lenguage | None = None,
        min_score: float | None = None,
    ) -> list[VectorSearchResult]:
        return await self._vector_search_service.search(
            query=query,
            limit=limit,
            language=language,
            min_score=min_score,
        )
