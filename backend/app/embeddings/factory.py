from functools import lru_cache

from app.core.config import settings
from app.embeddings.base import EmbeddingService


@lru_cache(maxsize=1)
def get_embedding_service() -> EmbeddingService:
    """Return the configured embedding service."""

    provider = settings.EMBEDDING_PROVIDER.lower()

    if provider == "local":
        from app.embeddings.local import LocalEmbeddingService
        return LocalEmbeddingService()

    if provider == "bedrock":
        from app.embeddings.bedrock import BedrockEmbeddingService
        return BedrockEmbeddingService()

    raise ValueError(
        f"Unsupported embedding provider: {settings.EMBEDDING_PROVIDER}"
    )