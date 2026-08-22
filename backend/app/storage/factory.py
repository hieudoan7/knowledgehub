from functools import lru_cache

from app.core.config import settings
from app.storage.base import StorageService
from app.storage.local import LocalStorageService
from app.storage.s3 import S3StorageService


@lru_cache(maxsize=1)
def get_storage_service() -> StorageService:
    """Return the configured storage provider."""

    provider = settings.STORAGE_PROVIDER.lower()

    if provider == "local":
        return LocalStorageService(settings.UPLOAD_DIR)

    if provider == "s3":
        if not settings.S3_BUCKET_NAME:
            raise ValueError(
                "S3_BUCKET_NAME must be configured when "
                "STORAGE_PROVIDER=s3"
            )

        return S3StorageService(
            bucket_name=settings.S3_BUCKET_NAME,
            region_name=settings.S3_REGION,
            prefix=settings.S3_PREFIX,
        )

    raise ValueError(
        f"Unsupported storage provider: {settings.STORAGE_PROVIDER}"
    )