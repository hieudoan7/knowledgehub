from uuid import UUID

from sqlalchemy.orm import Session

from fastapi import BackgroundTasks
from app.storage.base import StorageService
from app.models.document import Document
from app.models.enums import DocumentStatus
from app.repositories.document import DocumentRepository
from app.schemas.document import DocumentCreate
from app.exceptions.document import (
    FileTooLargeError,
    UnsupportedFileTypeError,
)
from app.utils.file import (
    ALLOWED_MIME_TYPES,
    MAX_FILE_SIZE,
    generate_stored_filename,
)
from app.services.background_tasks import BackgroundTaskService

class DocumentService:
    """Business logic for document management."""

    def __init__(
        self,
        session: Session,
        document_repository: DocumentRepository,
        storage_service: StorageService,
    ) -> None:
        self.session = session
        self.document_repository = document_repository
        self.storage_service = storage_service

    def create(
        self,
        request: DocumentCreate,
        owner_id: UUID,
    ) -> Document:
        """Create a new document."""

        document = Document(
            owner_id=owner_id,
            original_filename=request.original_filename,
            stored_filename=request.stored_filename,
            mime_type=request.mime_type,
            file_size=request.file_size,
            storage_path=request.storage_path,
            status=DocumentStatus.UPLOADED,
        )

        try:
            document = self.document_repository.create(document)
            self.session.commit()
            self.session.refresh(document)

            return document

        except Exception:
            self.session.rollback()
            raise
    
    def upload(
        self,
        *,
        owner_id: UUID,
        original_filename: str,
        mime_type: str,
        content: bytes,
        background_tasks: BackgroundTasks,
    ) -> Document:
        """
        Upload a new document.
        """

        if mime_type not in ALLOWED_MIME_TYPES:
            raise UnsupportedFileTypeError()

        if len(content) > MAX_FILE_SIZE:
            raise FileTooLargeError()

        stored_filename = generate_stored_filename(
            original_filename,
        )

        storage_path = self.storage_service.save(
            filename=stored_filename,
            content=content,
        )

        document = Document(
            owner_id=owner_id,
            original_filename=original_filename,
            stored_filename=stored_filename,
            mime_type=mime_type,
            file_size=len(content),
            storage_path=storage_path,
            status=DocumentStatus.UPLOADED,
        )

        try:
            document = self.document_repository.create(document)
            self.session.commit()
            self.session.refresh(document)
            background_tasks.add_task(
                BackgroundTaskService.process_document,
                document.id,
            )

            return document

        except Exception:
            self.session.rollback()

            # Remove uploaded file if DB transaction fails
            if self.storage_service.exists(storage_path):
                self.storage_service.delete(storage_path)

            raise

    def get_user_document(
        self,
        document_id: UUID,
        owner_id: UUID,
    ) -> Document | None:
        """Retrieve a document by its ID and owner."""

        return self.document_repository.get_by_id_and_owner(document_id, owner_id)

    def list_by_owner(
        self,
        owner_id: UUID,
    ) -> list[Document]:
        """Retrieve all documents belonging to a user."""

        return self.document_repository.list_by_owner(owner_id)

    def delete(
        self,
        document: Document,
    ) -> None:
        """Delete a document."""

        try:
            self.document_repository.delete(document)
            self.session.commit()

        except Exception:
            self.session.rollback()
            raise
    
    def process_document(
        self,
        document: Document,
    ) -> Document:
        try:
            document.status = DocumentStatus.PROCESSING
            self.document_repository.update(document)
            self.session.commit()

            document.status = DocumentStatus.READY
            self.document_repository.update(document)
            self.session.commit()

            self.session.refresh(document)

            return document

        except Exception:
            self.session.rollback()

            document.status = DocumentStatus.FAILED
            self.document_repository.update(document)
            self.session.commit()

            self.session.refresh(document)

            raise
