from app.processors.base import DocumentProcessor
from app.processors.docx import DocxProcessor
from app.processors.pdf import PdfProcessor
from app.processors.text import TextProcessor


class ProcessorFactory:
    """Create document processors."""

    _processors: dict[str, DocumentProcessor] = {
        "application/pdf": PdfProcessor(),
        "text/plain": TextProcessor(),
        "text/markdown": TextProcessor(),
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": DocxProcessor(),
    }

    @classmethod
    def get(
        cls,
        mime_type: str,
    ) -> DocumentProcessor:
        try:
            return cls._processors[mime_type]
        except KeyError:
            raise ValueError(
                f"No processor registered for '{mime_type}'."
            )

