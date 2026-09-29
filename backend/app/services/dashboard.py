from uuid import UUID
from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import Session
from app.repositories.document import DocumentRepository
from app.repositories.chat_history import ChatHistoryRepository
from app.schemas.dashboard import DashboardResponse, DashboardStats



class DashboardService:
    """Service responsible for dashboard data."""

    def __init__(
        self,
        document_repository: DocumentRepository,
        chat_history_repository: ChatHistoryRepository
    ) -> None:
        self.document_repository = document_repository
        self.chat_history_repository = chat_history_repository

    def get_dashboard(self, user_id: UUID) -> DashboardResponse:
        total_documents = self.document_repository.count_by_owner(user_id)
        ready_documents = self.document_repository.count_ready_by_owner(user_id)
        total_chats = self.chat_history_repository.count_by_user(user_id)
        now = datetime.now(timezone.utc)

        start_of_week = now.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        start_of_week = start_of_week -timedelta(days=start_of_week.weekday())
        chats_this_week = self.chat_history_repository.count_by_user_since(
            user_id,
            start_of_week,
        )
        recent_documents = self.document_repository.list_recent_by_owner(
            user_id,
            limit=5,
        )
        recent_chats = self.chat_history_repository.list_recent_by_user(
            user_id,
            limit=5,
        )
        return DashboardResponse(
            stats=DashboardStats(
                total_documents=total_documents,
                ready_documents=ready_documents,
                total_chats=total_chats,
                chats_this_week=chats_this_week,
            ),
            recent_documents=recent_documents,
            recent_chats=recent_chats,
        )
