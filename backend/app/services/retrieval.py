from dataclasses import dataclass

from app.models.document_chunk import DocumentChunk


@dataclass(slots=True)
class RetrievalContext:
    """
    Context returned by semantic search.
    """

    chunks: list[DocumentChunk]

    @property
    def text(self) -> str:
        return "\n\n".join(
            chunk.content
            for chunk in self.chunks
        )
