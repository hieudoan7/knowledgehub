from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select

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
    
    def count_by_user(self, user_id: UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(ChatMessageRecord)
            .where(ChatMessageRecord.user_id == user_id)
        )
        return self.session.scalar(stmt) or 0

    def count_by_user_since(self, user_id: UUID, since: datetime) -> int:
        stmt = (
            select(func.count())
            .select_from(ChatMessageRecord)
            .where(
                ChatMessageRecord.user_id == user_id,
                ChatMessageRecord.created_at >= since,
            )
        )
        return self.session.scalar(stmt) or 0

    def list_recent_by_user(
        self,
        user_id: UUID,
        limit: int = 5,
    ) -> list[ChatMessageRecord]:
        stmt = (
            select(ChatMessageRecord)
            .where(ChatMessageRecord.user_id == user_id)
            .order_by(ChatMessageRecord.created_at.desc())
            .limit(limit)
        )
        return list(self.session.scalars(stmt))
