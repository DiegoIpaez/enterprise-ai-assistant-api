
from src.ai.vector_search_service import VectorSearchResult
from src.config.settings import settings


class ContextBuilder:
    def __init__(self, max_documents: int | None = None):
        self._max_documents = max_documents or settings.AI_MAX_RESULTS

    def build(self, search_results: list[VectorSearchResult]) -> str:
        if not search_results:
            return ""

        limited_results = search_results[: self._max_documents]

        context_parts = []
        for index, result in enumerate(limited_results, start=1):
            document = result.document
            knowledge_type = document.type.value

            context_entry = f"[{index}] ({knowledge_type})\n{document.content}"

            context_parts.append(context_entry)

        context = "\n\n".join(context_parts)

        return context

    def build_with_metadata(
        self, search_results: list[VectorSearchResult], include_scores: bool = False
    ) -> str:
        if not search_results:
            return ""

        limited_results = search_results[: self._max_documents]

        context_parts = []
        for index, result in enumerate(limited_results, start=1):
            document = result.document
            knowledge_type = document.type.value

            context_entry = f"[{index}] ({knowledge_type})"

            if include_scores:
                context_entry += f" [score: {result.score:.4f}]"

            context_entry += f"\n{document.content}"
            context_parts.append(context_entry)

        context = "\n\n".join(context_parts)

        return context
