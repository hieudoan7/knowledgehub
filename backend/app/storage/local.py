from pathlib import Path

from app.storage.base import StorageService


class LocalStorageService(StorageService):
    """Store files on the local filesystem."""

    def __init__(self, upload_dir: str) -> None:
        self.upload_dir = Path(upload_dir)

        # Create the directory if it doesn't exist.
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save(
        self,
        *,
        filename: str,
        content: bytes,
    ) -> str:
        """
        Save a file to local storage.

        Returns:
            Relative storage path.
        """
        file_path = self.upload_dir / filename

        file_path.write_bytes(content)

        return filename

    def delete(
        self,
        storage_path: str,
    ) -> None:
        """Delete a file if it exists."""

	file_path = self.upload_dir / storage_path

        if file_path.exists():
            file_path.unlink()

    def exists(
        self,
        storage_path: str,
    ) -> bool:
        """Check whether a file exists."""

	return (self.upload_dir / storage_path).exists()

    def open(
        self,
        storage_path: str,
    ) -> Path:
        """Return the file path."""

	return self.upload_dir / storage_path
