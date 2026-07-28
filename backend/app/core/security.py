from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from jwt import InvalidTokenError as JWTInvalidTokenError

from app.exceptions.auth import InvalidTokenError

from pwdlib import PasswordHash

from app.core.config import settings


# Configure the application's password hasher.
# By default, PasswordHash.recommended() uses Argon2id.
password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a plain-text password."""

    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against its hash."""

    return password_hasher.verify(password, hashed_password)


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a signed JWT access token.

    Args:
        subject: User ID (UUID as string).
        expires_delta: Optional custom expiration.

    Returns:
        Encoded JWT string.
    """

    if expires_delta is None:
        expires_delta = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    expire = datetime.now(timezone.utc) + expires_delta

    payload = {
        "sub": subject,
        "exp": expire,
    }

    encoded_jwt = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTInvalidTokenError as exc:
        raise InvalidTokenError("Invalid or expired access token.") from exc
