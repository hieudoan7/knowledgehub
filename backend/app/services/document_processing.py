from uuid import uuid4
from app.models.document import Document
from app.processors.factory import ProcessorFactory
from app.repositories.document import DocumentRepository
from app.repositories.document_chunk import DocumentChunkRepository
from app.storage.base import StorageService
from app.models.document_chunk import DocumentChunk
from app.utils.text import split_text
from app.embeddings.base import EmbeddingService

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
        self.document_chunk_repository.delete_by_document(
            document.id,
        )
        chunks = split_text(text)

        for index, chunk_text in enumerate(chunks):
            embedding = self.embedding_service.embed(chunk_text)
            chunk = DocumentChunk(
                id=uuid4(),
	            document_id=document.id,
                chunk_index=index,
                content=chunk_text,
                embedding=embedding,
            )

            self.document_chunk_repository.create(chunk)
