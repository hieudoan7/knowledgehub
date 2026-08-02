import logging
from uuid import UUID, uuid4
from app.models.document import Document
from app.processors.factory import ProcessorFactory
from app.repositories.document import DocumentRepository
from app.repositories.document_chunk import DocumentChunkRepository
from app.storage.base import StorageService
from app.models.document_chunk import DocumentChunk
from app.utils.text import split_text
from app.embeddings.base import EmbeddingService
from app.models.enums import DocumentStatus
from app.core.config import settings


logger = logging.getLogger(__name__)

class DocumentProcessingService:
    """Handle document processing."""

    def __init__(
        self,
        storage_service: StorageService,
        document_repository: DocumentRepository,
	    document_chunk_repository: DocumentChunkRepository,
        embedding_service: EmbeddingService,
    ) -> None:
        self.storage_service = storage_service
        self.document_repository = document_repository
        self.document_chunk_repository = document_chunk_repository
        self.embedding_service = embedding_service

    def process(
        self,
        document_id: UUID,
    ) -> None:
        """
        Process a document.

        Pipeline:
            1. Load document
            2. Mark as processing
            3. Read file
            4. Extract text
            5. Split into chunks
            6. Generate embeddings
            7. Save chunks
            8. Mark document as ready
        """

        session = self.document_repository.session

        document = self.document_repository.get_by_id(document_id)
        if document is None:
            raise ValueError(f"Document '{document_id}' not found.")

        try:
            # Update status
            document.status = DocumentStatus.PROCESSING
            self.document_repository.update(document)

            # Read file
            content = self.storage_service.read(
                document.storage_path,
            )
            # Extract text
            processor = ProcessorFactory.get(
                document.mime_type,
            )
            text = processor.extract(content)
            # Save extracted text
            document.extracted_text = text
            self.document_repository.update(document)

            # Rebuild chunks
            self.document_chunk_repository.delete_by_document(
                document.id,
            )

            chunks = split_text(
                text,
                chunk_size=settings.CHUNK_SIZE,
                overlap_sentences=settings.CHUNK_OVERLAP_SENTENCES,
            )

            for index, chunk_text in enumerate(chunks):
                embedding = self.embedding_service.embed(chunk_text)
                self.document_chunk_repository.create(
                    DocumentChunk(
                        id=uuid4(),
                        document_id=document.id,
                        chunk_index=index,
                        content=chunk_text,
                        embedding=embedding,
                    )
                )

            # Finished successfully
            document.status = DocumentStatus.READY
            self.document_repository.update(document)

            session.commit()

        except Exception as e:
            session.rollback()
            logger.error("Error %s", repr(e))

            # Use a new transaction to record the failure.
            document = self.document_repository.get_by_id(document_id)
            if document is not None:
                document.status = DocumentStatus.FAILED
                self.document_repository.update(document)
                session.commit()

            raise
        