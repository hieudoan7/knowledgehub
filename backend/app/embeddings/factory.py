from functools import lru_cache

from app.embeddings.base import EmbeddingService
from app.embeddings.local import LocalEmbeddingService


@lru_cache(maxsize=1)
def get_embedding_service() -> EmbeddingService:
    """
    Return the configured embedding service.

    The model is loaded only once.
    """

    return LocalEmbeddingService()
