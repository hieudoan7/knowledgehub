import logging
from typing import ClassVar
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session, sessionmaker

from app.models.enums import ProcessingJobStatus
from app.repositories.processing_job import ProcessingJobRepository
from app.core.config import settings
from app.db.session import SessionLocal
from app.repositories.document import DocumentRepository
from app.repositories.document_chunk import DocumentChunkRepository
from app.services.document_processing import DocumentProcessingService
from app.embeddings.factory import get_embedding_service
from app.storage.factory import get_storage_service


logger = logging.getLogger(__name__)

class BackgroundTaskService:
    """Execute long-running background tasks."""

    session_factory: ClassVar[sessionmaker[Session]] = SessionLocal

    @classmethod
    def process_document(
        cls,
        document_id: UUID,
    ) -> None:
        db = cls.session_factory()
        job_repository = ProcessingJobRepository(db)

        try:
            job = job_repository.get_by_document_id(document_id)

            if job is None:
                logger.error(
                    "Processing job not found for document %s",
                    document_id,
                )
                return

            now = datetime.now(timezone.utc)

            job_repository.mark_processing(job, started_at=now)
            db.commit()

            processing_service = DocumentProcessingService(
                document_repository=DocumentRepository(db),
                document_chunk_repository=DocumentChunkRepository(db),
                embedding_service=get_embedding_service(),
                storage_service=get_storage_service(),
            )

            logger.info(
                "Processing document %s, attempt %s",
                document_id,
                job.attempts,
            )

            processing_service.process(document_id)

            job_repository.mark_completed(
                job,
                completed_at=datetime.now(timezone.utc),
            )
            db.commit()

        except Exception as exc:
            db.rollback()

            logger.exception(
                "Background processing failed for document %s",
                document_id,
            )

            job = job_repository.get_by_document_id(document_id)

            if job is not None:
                job_repository.mark_failed(
                    job,
                    failed_at=datetime.now(timezone.utc),
                    error=str(exc),
                )
                db.commit()

            raise

        finally:
            db.close()
