import logging
import time
from datetime import datetime, timezone
from app.embeddings.factory import get_embedding_service
from app.repositories.document import DocumentRepository
from app.repositories.document_chunk import DocumentChunkRepository
from app.repositories.processing_job import ProcessingJobRepository
from app.services.document_processing import DocumentProcessingService
from app.storage.factory import get_storage_service
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)


def run() -> None:
    """Run the document-processing worker."""

    logger.info("Document processing worker started.")

    while True:
        try:
            process_next_job()
        except Exception:
            logger.exception("Worker iteration failed.")

        time.sleep(2)


def process_next_job() -> None:
    db = SessionLocal()

    try:
        job_repository = ProcessingJobRepository(db)

        job = job_repository.claim_next()

        if job is None:
            return

        document_id = job.document_id

        # Commit the claim before doing expensive work.
        db.commit()

        logger.info(
            "Processing job %s for document %s (attempt %s)",
            job.id,
            document_id,
            job.attempts,
        )

        processing_service = DocumentProcessingService(
            document_repository=DocumentRepository(db),
            document_chunk_repository=DocumentChunkRepository(db),
            embedding_service=get_embedding_service(),
            storage_service=get_storage_service(),
        )

        processing_service.process(document_id)

        job = job_repository.get_by_id(job.id)

        if job is not None:
            _ = job_repository.mark_completed(
                job,
                completed_at=datetime.now(timezone.utc),
            )
            db.commit()

    except Exception:
        db.rollback()

        logger.exception(
            "Processing job failed.",
        )

        # We'll add proper retry handling next.
        raise

    finally:
        db.close()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    run()
