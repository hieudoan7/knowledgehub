from pathlib import Path
from uuid import uuid4
from app.core.config import settings


MAX_FILE_SIZE = settings.MAX_UPLOAD_SIZE
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "text/plain",
    "text/markdown",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def generate_stored_filename(original_filename: str) -> str:
    """
    Generate a unique filename while preserving the extension.
    """

    extension = Path(original_filename).suffix

    return f"{uuid4()}{extension}"

