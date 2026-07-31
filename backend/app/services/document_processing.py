from app.models.document import Document
from app.processors.factory import ProcessorFactory
from app.repositories.document import DocumentRepository
from app.storage.base import StorageService


class DocumentProcessingService:
    """Handle document processing."""

    def __init__(
        self,
        storage_service: StorageService,
        document_repository: DocumentRepository,
    ) -> None:
        self.storage_service = storage_service
        self.document_repository = document_repository

    def process(
        self,
        document: Document,
    ) -> None:
        """
        Process a document.

        Current pipeline:
            1. Read file
            2. Extract text

        Future pipeline:
            3. Chunk
            4. Embedding
            5. Summary
        """

        content = self.storage_service.read(
            document.storage_path,
        )

        processor = ProcessorFactory.get(
            document.mime_type,
        )

        text = processor.extract(content)

        document.extracted_text = text

        self.document_repository.update(document)

