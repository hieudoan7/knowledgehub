from dataclasses import dataclass

from app.models.document_chunk import DocumentChunk


@dataclass(slots=True)
class SearchResult:
    """Represents a semantic search result."""

    chunk: DocumentChunk
    score: float
