from uuid import UUID

from app.llm.base import LLMService
from app.llm.message import ChatMessage
from app.services.search import SearchService
from app.schemas.chat import (
    ChatResponse,
    ChatSource,
)


class ChatService:
    """Service responsible for answering questions about documents."""

    def __init__(
        self,
        search_service: SearchService,
        llm_service: LLMService,
    ) -> None:
        self.search_service = search_service
        self.llm_service = llm_service

    def chat(
        self,
        *,
        document_id: UUID,
        question: str,
    ) -> ChatResponse:
        """
        Answer a question about a document.
        """

        context = self.search_service.retrieve(
            document_id=document_id,
            query=question,
        )

        messages = self._build_messages(
            question=question,
            context=context.text,
        )

        answer = self.llm_service.generate(
            messages=messages,
        )

        return ChatResponse(
            answer=answer,
            sources=[
                ChatSource(
                    chunk_index=result.chunk.chunk_index,
                    score=result.score,
                )
                for result in context.sources
            ],
        )

    @staticmethod
    def _build_messages(
        *,
        question: str,
        context: str,
    ) -> list[ChatMessage]:
        """
        Build messages sent to the LLM.
        """

        return [
            ChatMessage(
                role="system",
                content=(
                    "You are a helpful AI assistant.\n\n"
                    "Answer ONLY using the supplied context.\n"
                    "If the answer cannot be found in the context, "
                    "reply with 'I don't know.'\n"
                    "Do not make up information."
                ),
            ),
            ChatMessage(
                role="user",
                content=(
                    f"Context:\n{context}\n\n"
                    f"Question:\n{question}"
                ),
            ),
        ]
