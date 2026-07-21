from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """Repository for user-related database operations."""

    session: Session

    def get_by_email(self, email: str) -> User | None:
        """Return a user by email, or None if not found."""

        stmt = select(User).where(User.email == email)

        return self.session.scalar(stmt)

    def create(self, user: User) -> User:
        """Persist a new user."""

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user
