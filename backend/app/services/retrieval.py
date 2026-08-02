from dataclasses import dataclass

from app.services.search_result import SearchResult


@dataclass(slots=True)
class RetrievalContext:
    """Context retrieved from semantic search."""

    results: list[SearchResult]

    @property
    def chunks(self):
        """Return retrieved document chunks."""

        return [
            result.chunk
            for result in self.results
        ]

    @property
    def text(self) -> str:
        """Concatenate retrieved chunk text."""

        return "\n\n".join(
            (
                f"[Chunk {result.chunk.chunk_index}]\n"
                f"{result.chunk.content}"
            )
            for result in self.results
        )

    @property
    def sources(self) -> list[SearchResult]:
        """Return search results with similarity scores."""

        return self.results
