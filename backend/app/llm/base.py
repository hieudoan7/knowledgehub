from typing import Protocol


class LLMService(Protocol):
    """Interface for Large Language Models."""

    def generate(
        self,
        *,
        messages: list[dict[str, str]],
    ) -> str:
        """
        Generate a response from a conversation.
        """
        ...