import boto3

from app.core.config import settings
from app.llm.base import LLMService
from app.llm.message import ChatMessage


class BedrockService(LLMService):
    """LLM implementation backed by Amazon Bedrock."""

    def __init__(self) -> None:
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=settings.AWS_REGION,
        )
        self.model = settings.LLM_MODEL

    def generate(
        self,
        *,
        messages: list[ChatMessage],
    ) -> str:
        response = self.client.converse(
            modelId=self.model,
            messages=[
                {
                    "role": message.role,
                    "content": [{"text": message.content}],
                }
                for message in messages
            ],
            inferenceConfig={
                "maxTokens": 512,
                "temperature": 0,
                "topP": 0.9,
            },
        )

        return response["output"]["message"]["content"][0]["text"]