from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_auth_service
from app.exceptions.auth import (
    AuthenticationError,
    EmailAlreadyExistsError,
)
from app.schemas.auth import UserLogin, UserRegister
from app.schemas.user import UserResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: UserRegister,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    """Register a new user."""

    try:
        user = auth_service.register(request)
    except EmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return UserResponse.model_validate(user)


@router.post("/login")
def login(
    request: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
):
    """Authenticate a user."""

    try:
        user = auth_service.authenticate(request)
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        ) from exc

    return {
        "message": "Login successful",
        "user": UserResponse.model_validate(user),
    }
