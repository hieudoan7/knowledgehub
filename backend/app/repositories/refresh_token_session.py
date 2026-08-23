from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.refresh_token_session import RefreshTokenSession
from app.repositories.base import BaseRepository


class RefreshTokenSessionRepository(BaseRepository):
    """Repository for refresh-token session operations."""

    session: Session

    def create(
        self,
        refresh_token_session: RefreshTokenSession,
    ) -> RefreshTokenSession:
        """Create a refresh-token session."""

        self.session.add(refresh_token_session)
        self.session.flush()
        self.session.refresh(refresh_token_session)

        return refresh_token_session

    def get_active_by_hash(
        self,
        token_hash: str,
        *,
        now: datetime,
    ) -> RefreshTokenSession | None:
        """Return a non-revoked, non-expired refresh-token session."""

        stmt = select(RefreshTokenSession).where(
            RefreshTokenSession.token_hash == token_hash,
            RefreshTokenSession.revoked_at.is_(None),
            RefreshTokenSession.expires_at > now,
        )

        return self.session.scalar(stmt)

    def revoke(
        self,
        refresh_token_session: RefreshTokenSession,
        *,
        revoked_at: datetime,
    ) -> RefreshTokenSession:
        """Revoke a refresh-token session."""

        refresh_token_session.revoked_at = revoked_at
        self.session.flush()

        return refresh_token_session

    def set_replaced_by(
        self,
        refresh_token_session: RefreshTokenSession,
        *,
        replacement_id: UUID,
    ) -> RefreshTokenSession:
        """Link a rotated token session to its replacement."""

        refresh_token_session.replaced_by = replacement_id
        self.session.flush()

        return refresh_token_session