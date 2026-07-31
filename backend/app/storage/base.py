from pathlib import Path
from typing import Protocol


class StorageService(Protocol):
    """Interface for file storage providers."""

    def save(
        self,
        *,
        filename: str,
        content: bytes,
    ) -> str:
        """
        Save a file.

        Returns:
            The storage path (or storage key).
        """
        ...

    def delete(
        self,
        storage_path: str,
    ) -> None:
        """
        Delete a file.
        """
        ...

    def exists(
        self,
        storage_path: str,
    ) -> bool:
        """
        Check whether a file exists.
        """
        ...

    def read(
        self,
        storage_path: str,
    ) -> bytes:
        """
        Read a file from storage.
        """
        ...