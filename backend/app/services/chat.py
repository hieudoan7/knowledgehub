import logging
from uuid import UUID

from app.llm.base import LLMService
from app.llm.message import ChatMessage
from app.services.search import SearchService
from app.schemas.chat import (
    ChatResponse,
    ChatSource,
)
from app.prompts.rag import build_rag_messages
from app.repositories.chat_history import ChatHistoryRepository
from app.models.chat_message_record import ChatMessageRecord
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class ChatService:
    """Service responsible for answering questions about documents."""

    def __init__(
        self,
        session: Session,
        search_service: SearchService,
        llm_service: LLMService,
        chat_history_repository: ChatHistoryRepository,
    ) -> None:
        self.session = session
        self.search_service = search_service
        self.llm_service = llm_service
        self.chat_history_repository = chat_history_repository

    def chat(
        self,
        *,
        document_id: UUID,
        user_id: UUID,
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
        
        logger.debug(
            "Retrieval context:\n%s",
            context,
        )

        response = ChatResponse(
            answer=answer,
            sources=[
                ChatSource(
                    chunk_index=result.chunk.chunk_index,
                    score=result.score,
                )
                for result in context.sources
            ],
        )
        try:
            _ = self.chat_history_repository.create(
                message=ChatMessageRecord(
                    user_id=user_id,
                    document_id=document_id,
                    question=question,
                    answer=response.answer,
                    sources=[
                        {
                            "chunk_index": source.chunk_index,
                            "score": source.score,
                        }
                        for source in response.sources
                    ],
                )
            ) 
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

        return response