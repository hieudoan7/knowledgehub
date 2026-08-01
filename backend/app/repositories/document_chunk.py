from uuid import UUID
from sqlalchemy import select, delete

from app.models.document_chunk import DocumentChunk
from app.repositories.base import BaseRepository
from app.services.search_result import SearchResult


class DocumentChunkRepository(BaseRepository):
    """Repository for document chunks."""

    def create(
        self,
        chunk: DocumentChunk,
    ) -> DocumentChunk:
        self.session.add(chunk)
        self.session.flush()
        self.session.refresh(chunk)

        return chunk

    def list_by_document(
        self,
        document_id,
    ) -> list[DocumentChunk]:
        stmt = (
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index)
        )

        return list(self.session.scalars(stmt))

    def delete_by_document(
        self,
        document_id: UUID,
    ) -> None:
        stmt = (
            delete(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
        )

        self.session.execute(stmt)
    
    def similarity_search(
        self,
        *,
        document_id: UUID,
        embedding: list[float],
        limit: int = 5,
    ) -> list[SearchResult]:
        """
        Return the most similar chunks for a document.
        """

        distance = DocumentChunk.embedding.cosine_distance(
            embedding,
        ).label("distance")

        stmt = (
            select(
                DocumentChunk,
                distance,
            )
            .where(
                DocumentChunk.document_id == document_id,
            )
            .order_by(distance)
            .limit(limit)
        )

        rows = self.session.execute(stmt).all()

        return [
            SearchResult(
                chunk=chunk,
                score=1 - distance,
            )
            for chunk, distance in rows
        ]
