from sentence_transformers import SentenceTransformer

from app.embeddings.base import EmbeddingService


class LocalEmbeddingService(EmbeddingService):
    """Embedding service using a local SentenceTransformer model."""

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
    ) -> None:
        self.model = SentenceTransformer(model_name)

    def embed(
        self,
        text: str,
    ) -> list[float]:
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()
