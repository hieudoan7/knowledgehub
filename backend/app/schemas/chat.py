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