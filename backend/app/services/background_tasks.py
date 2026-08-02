from typing import ClassVar
from uuid import UUID

from app.core.config import settings
from sqlalchemy.orm import Session, sessionmaker

from app.db.session import SessionLocal
from app.repositories.document import DocumentRepository
from app.repositories.document_chunk import DocumentChunkRepository
from app.services.document_processing import DocumentProcessingService
from app.embeddings.local import LocalEmbeddingService
from app.storage.local import LocalStorageService


class BackgroundTaskService:
    """Execute long-running background tasks."""

    session_factory: ClassVar[sessionmaker[Session]] = SessionLocal

    @classmethod
    def process_document(
        cls,
        document_id: UUID,
    ) -> None:
        db = cls.session_factory()

        try:
            processing_service = DocumentProcessingService(
                document_repository=DocumentRepository(db),
                document_chunk_repository=DocumentChunkRepository(db),
                embedding_service=LocalEmbeddingService(),
                storage_service=LocalStorageService(upload_dir=settings.UPLOAD_DIR),
            )
            print(">>> Background task started", flush=True)
            processing_service.process(document_id)

        finally:
            db.close()
