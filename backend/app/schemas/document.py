from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import DocumentStatus


class DocumentCreate(BaseModel):
    """Request schema for creating a document."""

    original_filename: str
    stored_filename: str
    mime_type: str
    file_size: int
    storage_path: str


class DocumentUpdate(BaseModel):
    """Request schema for updating document status."""

    status: DocumentStatus


class DocumentResponse(BaseModel):
    """Response schema for a document."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_id: UUID

    original_filename: str
    stored_filename: str

    mime_type: str
    file_size: int
    storage_path: str

    status: DocumentStatus

    created_at: datetime
    updated_at: datetime
