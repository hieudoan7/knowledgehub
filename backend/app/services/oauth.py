from app.models.oauth_account import OAuthAccount
from app.models.user import User
from app.repositories.oauth_account import OAuthAccountRepository
from app.repositories.user import UserRepository


class OAuthService:
    """Business logic for OAuth authentication."""

    def __init__(
        self,
        user_repository: UserRepository,
        oauth_account_repository: OAuthAccountRepository,
    ) -> None:
        self.user_repository = user_repository
        self.oauth_account_repository = oauth_account_repository

    def authenticate(
        self,
        provider: str,
        provider_user_id: str,
        email: str,
        full_name: str | None,
    ) -> User:
        """Find or create a KnowledgeHub user from a Google identity."""

        oauth_account = self.oauth_account_repository.get_by_provider_identity(
            provider=provider,
            provider_user_id=provider_user_id,
        )

        if oauth_account is not None:
            user = self.user_repository.get_by_id(
                oauth_account.user_id,
            )

            if user is None:
                raise ValueError(
                    "OAuth account references a missing user."
                )

            return user

        user = self.user_repository.get_by_email(email)

        if user is None:
            user = User(
                email=email,
                hashed_password=None,
                full_name=full_name,
            )

            user = self.user_repository.create(user)

        oauth_account = OAuthAccount(
            user_id=user.id,
            provider=provider,
            provider_user_id=provider_user_id,
        )

        self.oauth_account_repository.create(oauth_account)

        self.oauth_account_repository.session.commit()

        return user
