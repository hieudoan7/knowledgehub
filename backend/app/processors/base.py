from typing import Protocol


class DocumentProcessor(Protocol):
    """Extract plain text from a document."""

    def extract(
        self,
        content: bytes,
    ) -> str:
        """
        Extract plain text from file bytes.
        """
        ...

