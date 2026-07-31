from pathlib import Path

from app.processors.base import DocumentProcessor


class TextProcessor(DocumentProcessor):
    """Extract text from plain text files."""

    def extract(
        self,
        content: bytes,
    ) -> str:
        return content.decode("utf-8")
