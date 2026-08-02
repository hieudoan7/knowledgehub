from typing import Protocol
from app.llm.message import ChatMessage


class LLMService(Protocol):
    """Interface for Large Language Models."""

    def generate(
        self,
        *,
        messages: list[ChatMessage],
    ) -> str:
        """
        Generate a response from a conversation.
        """
        ...