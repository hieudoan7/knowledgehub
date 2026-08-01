from ollama import Client

from app.llm.base import LLMService
from app.llm.message import ChatMessage
from app.core.config import settings


class OllamaService(LLMService):
    """LLM implementation backed by Ollama."""

    def __init__(self) -> None:
        self.client = Client(host=settings.OLLAMA_HOST)
        self.model = settings.LLM_MODEL

    def generate(
        self,
        *,
        messages: list[ChatMessage],
    ) -> str:
        """
        Generate a response from Ollama.
        """

        response = self.client.chat(
            model=self.model,
            messages=[message.model_dump() for message in messages],
        )

        return response["message"]["content"]
