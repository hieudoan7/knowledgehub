from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserResponse(BaseModel):
    """User information returned by the API."""

    id: UUID
    email: EmailStr
    full_name: str | None

    is_active: bool
    is_superuser: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
