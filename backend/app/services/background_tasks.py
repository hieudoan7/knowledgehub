from uuid import UUID
from app.core.config import settings

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.repositories.document import DocumentRepository
from app.repositories.document_chunk import DocumentChunkRepository
from app.services.document_processing import DocumentProcessingService
from app.embeddings.local import LocalEmbeddingService
from app.storage.local import LocalStorageService


class BackgroundTaskService:
    """Execute long-running background tasks."""

    @staticmethod
    def process_document(document_id: UUID) -> None:
        """
        Process a document in a fresh database session.
        """

        db: Session = SessionLocal()

        try:
            processing_service = DocumentProcessingService(
                document_repository=DocumentRepository(db),
                document_chunk_repository=DocumentChunkRepository(db),
                embedding_service=LocalEmbeddingService(),
                storage_service=LocalStorageService(upload_dir=settings.UPLOAD_DIR),
            )

            processing_service.process(document_id)

        finally:
            db.close()
