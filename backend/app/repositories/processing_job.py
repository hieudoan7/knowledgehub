from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import ProcessingJobStatus
from app.models.processing_job import ProcessingJob
from app.repositories.base import BaseRepository


class ProcessingJobRepository(BaseRepository):
    """Repository for document processing jobs."""

    session: Session

    def create(self, job: ProcessingJob) -> ProcessingJob:
        self.session.add(job)
        self.session.flush()
        self.session.refresh(job)

        return job

    def get_by_document_id(
        self,
        document_id: UUID,
    ) -> ProcessingJob | None:
        stmt = select(ProcessingJob).where(
            ProcessingJob.document_id == document_id,
        )

        return self.session.scalar(stmt)

    def get_by_id(
        self,
        job_id: UUID,
    ) -> ProcessingJob | None:
        stmt = select(ProcessingJob).where(
            ProcessingJob.id == job_id,
        )

        return self.session.scalar(stmt)

    def mark_processing(
        self,
        job: ProcessingJob,
        *,
        started_at: datetime,
    ) -> ProcessingJob:
        job.status = ProcessingJobStatus.PROCESSING
        job.attempts += 1
        job.started_at = started_at
        job.error = None

        self.session.flush()

        return job

    def mark_completed(
        self,
        job: ProcessingJob,
        *,
        completed_at: datetime,
    ) -> ProcessingJob:
        job.status = ProcessingJobStatus.COMPLETED
        job.completed_at = completed_at

        self.session.flush()

        return job

    def mark_failed(
        self,
        job: ProcessingJob,
        *,
        failed_at: datetime,
        error: str,
    ) -> ProcessingJob:
        job.status = ProcessingJobStatus.FAILED
        job.failed_at = failed_at
        job.error = error

        self.session.flush()

        return job