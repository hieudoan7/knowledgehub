import fitz

from app.processors.base import DocumentProcessor


class PdfProcessor(DocumentProcessor):
    """Extract text from PDF documents."""

    def extract(
        self,
        content: bytes,
    ) -> str:
        text = []

        with fitz.open(stream=content, filetype="pdf") as pdf:
            for page in pdf:
                text.append(page.get_text())

        return "\n".join(text)

