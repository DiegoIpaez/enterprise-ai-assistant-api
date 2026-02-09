class PromptBuilder:
    def __init__(
        self,
        system_message: str | None = None,
        language: str = "español",
    ):
        self._language = language
        self._system_message = system_message or self._get_default_system_message()

    def _get_default_system_message(self) -> str:
        return f"""Sos un asistente de IA especializado en responder preguntas usando únicamente la información proporcionada en el CONTEXTO.

REGLAS ESTRICTAS:
- Respondé ÚNICAMENTE usando la información del CONTEXTO.
- NO inventes información que no esté en el CONTEXTO.
- Si la respuesta no está en el CONTEXTO, debés responder: "No tengo información suficiente para responder esta pregunta".
- Si el CONTEXTO está vacío, debés responder: "No tengo información disponible para responder esta pregunta".
- Mantené tus respuestas claras, concisas y basadas exclusivamente en el CONTEXTO.
- Respondé en {self._language}."""

    def build(
        self,
        context: str,
        question: str,
    ) -> str:
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        prompt_parts = []

        prompt_parts.append("SYSTEM:")
        prompt_parts.append(self._system_message)
        prompt_parts.append("")

        prompt_parts.append("CONTEXTO:")
        if not context or not context.strip():
            prompt_parts.append("(No hay información disponible)")
        else:
            prompt_parts.append(context)
        prompt_parts.append("")

        prompt_parts.append("PREGUNTA:")
        prompt_parts.append(question.strip())

        prompt = "\n".join(prompt_parts)
        return prompt

    def build_for_tinyllama(
        self,
        context: str,
        question: str,
    ) -> str:
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        user_message_parts = []
        user_message_parts.append("CONTEXTO:")

        if not context or not context.strip():
            user_message_parts.append("(No hay información disponible)")
        else:
            user_message_parts.append(context)

        user_message_parts.append("")
        user_message_parts.append("PREGUNTA:")
        user_message_parts.append(question.strip())
        user_message = "\n".join(user_message_parts)

        prompt = f"""<|system|>
{self._system_message}</s>
<|user|>
{user_message}</s>
<|assistant|>
"""
        return prompt
