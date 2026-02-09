from src.ai.llm.tiny_llama_client import TinyLlamaClient
from src.ai.context_builder import ContextBuilder
from src.ai.prompt_builder import PromptBuilder
from src.ai.vector_search_service import VectorSearchService
from src.app.ai_knowledges.ai_knowledges_model import Language


class RAGOrchestrator:
    def __init__(
        self,
        vector_search_service: VectorSearchService | None = None,
        context_builder: ContextBuilder | None = None,
        prompt_builder: PromptBuilder | None = None,
        tiny_llama_client: TinyLlamaClient | None = None,
    ):
        self._vector_search_service = vector_search_service or VectorSearchService()
        self._context_builder = context_builder or ContextBuilder()
        self._prompt_builder = prompt_builder or PromptBuilder()
        self._phi3_client = tiny_llama_client or TinyLlamaClient()

    async def ask(self, question: str, language: Language | None = None) -> str:
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        search_results = await self._vector_search_service.search(
            query=question,
            language=language,
        )

        prompt_language = "inglés" if language == Language.ENGLISH else "español"
        prompt_builder = PromptBuilder(language=prompt_language)

        context = self._context_builder.build(search_results)
        prompt = prompt_builder.build_for_tinyllama(context=context, question=question)
        answer = self._phi3_client.generate(prompt)
        return answer
