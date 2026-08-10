from sqlalchemy import select
from uuid import UUID
from app.models.chat_message_record import ChatMessageRecord
from app.repositories.base import BaseRepository


class ChatHistoryRepository(BaseRepository):
    """Repository for chat history persistence."""

    def create(
        self,
        message: ChatMessageRecord,
    ) -> ChatMessageRecord:
        self.session.add(message)
        self.session.flush()
        self.session.refresh(message)
        return message

    def list_by_document(
        self,
        document_id: UUID,
        user_id: UUID,
    ) -> list[ChatMessageRecord]:
        stmt = (
            select(ChatMessageRecord)
            .where(
                ChatMessageRecord.document_id == document_id,
                ChatMessageRecord.user_id == user_id,
            )
            .order_by(ChatMessageRecord.created_at.asc())
        )

        return list(self.session.scalars(stmt))