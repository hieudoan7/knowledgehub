from typing import Protocol


class EmbeddingService(Protocol):
    """Interface for embedding providers."""

    def embed(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a piece of text.
        """
        ...
