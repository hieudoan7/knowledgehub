from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.user import UserRepository
from app.services.auth import AuthService


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

