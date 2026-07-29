from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.exceptions.auth import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token",
)


def get_user_repository(
    session: Session = Depends(get_db),
) -> UserRepository:
    """Return a UserRepository instance."""
    return UserRepository(session)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    """Return an AuthService instance."""
    return AuthService(user_repository)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    """
    Return the currently authenticated user.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")

        if subject is None:
            raise credentials_exception

        user_id = UUID(subject)

    except (InvalidTokenError, ValueError):
        raise credentials_exception

    user = user_repository.get_by_id(user_id)

    if user is None:
        raise credentials_exception

    return user
