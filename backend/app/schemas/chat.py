from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        min_length=1,
    )


class ChatSource(BaseModel):
    chunk_index: int
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[ChatSource]


class ChatHistoryItem(BaseModel):
    id: UUID
    question: str
    answer: str
    sources: list[ChatSource]
    created_at: datetime
