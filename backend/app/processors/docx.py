from io import BytesIO

from docx import Document as DocxDocument

from app.processors.base import DocumentProcessor


class DocxProcessor(DocumentProcessor):
    """Extract text from DOCX documents."""

    def extract(
        self,
        content: bytes,
    ) -> str:
        document = DocxDocument(BytesIO(content))

        return "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

