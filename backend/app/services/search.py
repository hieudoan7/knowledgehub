from uuid import UUID

from app.embeddings.base import EmbeddingService
from app.models.document_chunk import DocumentChunk
from app.repositories.document_chunk import DocumentChunkRepository
from app.services.search_result import SearchResult


class SearchService:
    """Service responsible for semantic search."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        document_chunk_repository: DocumentChunkRepository,
    ) -> None:
        self.embedding_service = embedding_service
        self.document_chunk_repository = document_chunk_repository

    def search(
        self,
        *,
        document_id: UUID,
        query: str,
        limit: int = 5,
    ) -> list[SearchResult]:
        """
        Search for the most relevant chunks in a document.

        Args:
            document_id: ID of the document to search.
            query: User search query.
            limit: Maximum number of chunks to return.

        Returns:
            List of document chunks ordered by semantic similarity.
        """

        query_embedding = self.embedding_service.embed(query)

        return self.document_chunk_repository.similarity_search(
            document_id=document_id,
            embedding=query_embedding,
            limit=limit,
        )
