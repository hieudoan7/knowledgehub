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
        system_messages = [
            message.content
            for message in messages
            if message.role == "system"
        ]

        conversation_messages = [
            {
                "role": message.role,
                "content": [{"text": message.content}],
            }
            for message in messages
            if message.role != "system"
        ]

        if system_messages:
            system_instruction = "\n\n".join(system_messages)

            if conversation_messages and conversation_messages[0]["role"] == "user":
                conversation_messages[0]["content"].insert(
                    0,
                    {
                        "text": (
                            "Follow these instructions when answering:\n\n"
                            f"{system_instruction}\n\n"
                        )
                    },
                )

        response = self.client.converse(
            modelId=self.model,
            messages=conversation_messages,
            inferenceConfig={
                "maxTokens": 512,
                "temperature": 0,
                "topP": 0.9,
            },
        )

        return response["output"]["message"]["content"][0]["text"]