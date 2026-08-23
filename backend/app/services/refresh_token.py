from datetime import datetime, timedelta, timezone
from uuid import UUID

from app.core.config import settings
from app.core.security import (
    create_refresh_token,
    hash_refresh_token,
)
from app.exceptions.auth import InvalidTokenError
from app.models.refresh_token_session import RefreshTokenSession
from app.repositories.refresh_token_session import (
    RefreshTokenSessionRepository,
)


class RefreshTokenService:
    """Service responsible for refresh-token lifecycle management."""

    def __init__(
        self,
        repository: RefreshTokenSessionRepository,
    ) -> None:
        self.repository = repository

    def create(self, user_id: UUID) -> str:
        """Create and persist a refresh-token session."""

        token = create_refresh_token()

        session = RefreshTokenSession(
            user_id=user_id,
            token_hash=hash_refresh_token(token),
            expires_at=self._expiration(),
        )

        self.repository.create(session)
        self.repository.session.commit()

        return token

    def rotate(self, token: str) -> tuple[str, UUID]:
        """Rotate a valid refresh token."""

        now = datetime.now(timezone.utc)

        current = self.repository.get_active_by_hash(
            hash_refresh_token(token),
            now=now,
        )

        if current is None:
            raise InvalidTokenError(
                "Invalid or expired refresh token."
            )

        new_token = create_refresh_token()

        replacement = RefreshTokenSession(
            user_id=current.user_id,
            token_hash=hash_refresh_token(new_token),
            expires_at=self._expiration(),
        )
        try:
            self.repository.create(replacement)

            self.repository.revoke(
                current,
                revoked_at=now,
            )

            self.repository.set_replaced_by(
                current,
                replacement_id=replacement.id,
            )

            self.repository.session.commit()
        except Exception:
            self.repository.session.rollback()
            raise

        return new_token, current.user_id

    def revoke(self, token: str) -> None:
        """Revoke a refresh token."""

        now = datetime.now(timezone.utc)

        session = self.repository.get_active_by_hash(
            hash_refresh_token(token),
            now=now,
        )

        if session is None:
            return

        self.repository.revoke(
            session,
            revoked_at=now,
        )

        self.repository.session.commit()

    @staticmethod
    def _expiration() -> datetime:
        return datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
        )