from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.constants import PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH, MAX_NAME_LENGTH


class UserRegister(BaseModel):
    """Request body for user registration."""

    email: EmailStr
    password: str = Field(
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
        description="User password",
    )
    full_name: str | None = Field(
        default=None,
        max_length=MAX_NAME_LENGTH,
    )


class UserLogin(BaseModel):
    """Request body for user login."""

    email: EmailStr
    password: str

