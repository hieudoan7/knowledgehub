class UnsupportedFileTypeError(Exception):
    """Raised when an uploaded file type is not supported."""


class FileTooLargeError(Exception):
    """Raised when an uploaded file exceeds the size limit."""

