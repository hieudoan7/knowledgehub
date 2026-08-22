import json

import boto3

from app.core.config import settings
from app.embeddings.base import EmbeddingService


class BedrockEmbeddingService(EmbeddingService):
    """Embedding service using Amazon Titan Text Embeddings V2."""

    def __init__(
        self,
        *,
        model_id: str = settings.EMBEDDING_MODEL,
        region_name: str = settings.AWS_REGION,
    ) -> None:
        self.model_id = model_id

        self.client = boto3.client(
            "bedrock-runtime",
            region_name=region_name,
        )

    def embed(
        self,
        text: str,
    ) -> list[float]:
        body = json.dumps(
            {
                "inputText": text,
                "dimensions": 512,
                "normalize": True,
            }
        )

        response = self.client.invoke_model(
            modelId=self.model_id,
            body=body,
            contentType="application/json",
            accept="application/json",
        )

        result = json.loads(response["body"].read())

        return result["embedding"]