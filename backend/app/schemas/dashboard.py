from pydantic import BaseModel

from app.schemas.chat import ChatHistoryItem
from app.schemas.document import DocumentResponse


class DashboardStats(BaseModel):
    total_documents: int
    ready_documents: int
    total_chats: int
    chats_this_week: int


class DashboardResponse(BaseModel):
    stats: DashboardStats
    recent_documents: list[DocumentResponse]
    recent_chats: list[ChatHistoryItem]