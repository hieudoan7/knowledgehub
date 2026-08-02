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
            chunk.content
            for chunk in self.chunks
        )

    @property
    def sources(self) -> list[SearchResult]:
        """Return search results with similarity scores."""

        return self.results