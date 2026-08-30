from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.oauth_account import OAuthAccount
from app.repositories.base import BaseRepository


class OAuthAccountRepository(BaseRepository):
    """Repository for OAuth account database operations."""

    session: Session

    def get_by_provider_identity(
        self,
        provider: str,
        provider_user_id: str,
    ) -> OAuthAccount | None:
        """Retrieve an OAuth account by provider and provider user ID."""

        stmt = select(OAuthAccount).where(
            OAuthAccount.provider == provider,
            OAuthAccount.provider_user_id == provider_user_id,
        )

        return self.session.scalar(stmt)

    def get_by_user_id(self, user_id: UUID) -> list[OAuthAccount]:
        """Retrieve all OAuth accounts belonging to a user."""

        stmt = select(OAuthAccount).where(
            OAuthAccount.user_id == user_id
        )

        return list(self.session.scalars(stmt).all())

    def create(self, oauth_account: OAuthAccount) -> OAuthAccount:
        """Add a new OAuth account to the current session."""

        self.session.add(oauth_account)
        self.session.flush()
        self.session.refresh(oauth_account)

        return oauth_account
