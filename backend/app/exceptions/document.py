class DocumentError(Exception):
    """Base exception for document operations."""


class UnsupportedFileTypeError(DocumentError):
    """Raised when the uploaded file type is not supported."""


class FileTooLargeError(DocumentError):
    """Raised when the uploaded file exceeds the maximum allowed size."""

class DocumentNotFoundError(DocumentError):
    """Raised when document not found."""
    