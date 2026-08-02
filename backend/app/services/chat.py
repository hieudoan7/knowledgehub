from uuid import UUID

from app.llm.base import LLMService
from app.llm.message import ChatMessage
from app.services.search import SearchService
from app.schemas.chat import (
    ChatResponse,
    ChatSource,
)
from app.prompts.rag import build_rag_messages


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

        messages = build_rag_messages(
            question=question,
            context=context.text,
        )

        answer = self.llm_service.generate(
            messages=messages,
        )
        print("=" * 80, flush=True)
        print(context.text, flush=True)
        print("=" * 80, flush=True)

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
