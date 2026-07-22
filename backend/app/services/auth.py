from app.core.security import hash_password, verify_password
from app.exceptions.auth import (
    AuthenticationError,
    EmailAlreadyExistsError,
)
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import UserLogin, UserRegister


class AuthService:
    """Business logic for authentication."""

    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def register(self, request: UserRegister) -> User:
        """Register a new user."""

        existing_user = self.user_repository.get_by_email(request.email)

        if existing_user:
            raise EmailAlreadyExistsError(
                f"User with email '{request.email}' already exists."
            )

        user = User(
            email=request.email,
            hashed_password=hash_password(request.password),
            full_name=request.full_name,
        )

        _ = self.user_repository.create(user)
        self.user_repository.session.commit()
        self.user_repository.session.refresh(user)

        return user

    def authenticate(self, request: UserLogin) -> User:
        """Authenticate a user."""

        user = self.user_repository.get_by_email(request.email)

        if user is None:
            raise AuthenticationError("Invalid email or password.")

        if not verify_password(
            request.password,
            user.hashed_password,
        ):
            raise AuthenticationError("Invalid email or password.")

        return user
