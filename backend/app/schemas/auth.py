from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegister(BaseModel):
    """Request body for user registration."""

    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
        description="User password",
    )
    full_name: str | None = Field(
        default=None,
        max_length=255,
    )


class UserLogin(BaseModel):
    """Request body for user login."""

    email: EmailStr
    password: str

