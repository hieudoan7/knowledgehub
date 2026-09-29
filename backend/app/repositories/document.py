from uuid import UUID

from sqlalchemy import select, func

from app.models.document import Document
from app.repositories.base import BaseRepository
from app.models.enums import DocumentStatus


class DocumentRepository(BaseRepository):
    """Repository for document persistence."""

    def create(self, document: Document) -> Document:
        self.session.add(document)
        self.session.flush()
        self.session.refresh(document)
        return document

    def get_by_id(self, document_id: UUID) -> Document | None:
        stmt = select(Document).where(Document.id == document_id)
        return self.session.scalar(stmt)

    def get_by_id_and_owner(
        self,
        document_id: UUID,
        owner_id: UUID,
    ) -> Document | None:
        stmt = select(Document).where(
            Document.id == document_id,
            Document.owner_id == owner_id,
        )
        return self.session.scalar(stmt)

    def list_by_owner(self, owner_id: UUID) -> list[Document]:
        stmt = (
            select(Document)
            .where(Document.owner_id == owner_id)
            .order_by(Document.created_at.desc())
        )

        return list(self.session.scalars(stmt))
    
    def count_by_owner(self, owner_id: UUID) -> int:
        stmt = select(func.count()).select_from(Document).where(
            Document.owner_id == owner_id
        )
        return self.session.scalar(stmt) or 0
    
    def count_ready_by_owner(self, owner_id: UUID) -> int:
        stmt = select(func.count()).select_from(Document).where(
            Document.owner_id == owner_id,
            Document.status == DocumentStatus.READY,
        )
        return self.session.scalar(stmt) or 0
    
    def list_recent_by_owner(self, owner_id: UUID, limit: int = 5) -> list[Document]:
        stmt = (
            select(Document)
            .where(Document.owner_id == owner_id)
            .order_by(Document.created_at.desc())
            .limit(limit)
        )
        return list(self.session.scalars(stmt))
    
    def update(self, document: Document) -> Document:
        self.session.add(document)
        self.session.flush()
        self.session.refresh(document)
        return document

    def delete(self, document: Document) -> None:
        self.session.delete(document)

