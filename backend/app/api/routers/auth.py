from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Cookie, Response
from app.api.deps import get_refresh_token_service
from app.core.config import settings
from app.core.oauth import oauth
from app.exceptions.auth import InvalidTokenError
from app.services.refresh_token import RefreshTokenService

from app.api.deps import get_auth_service
from app.core.security import create_access_token
from app.exceptions.auth import (
    AuthenticationError,
    EmailAlreadyExistsError,
)
from app.schemas.auth import UserLogin, UserRegister, TokenResponse
from app.schemas.user import UserResponse
from app.services.auth import AuthService
from app.services.oauth import OAuthService
from app.api.deps import get_oauth_service

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


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: UserLogin,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
    refresh_token_service: RefreshTokenService = Depends(
        get_refresh_token_service,
    ),
) -> TokenResponse:
    try:
        user = auth_service.authenticate(request)
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        ) from exc

    access_token = create_access_token(
        subject=str(user.id),
    )

    refresh_token = refresh_token_service.create(
        user_id=user.id,
    )

    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=settings.REFRESH_TOKEN_COOKIE_SECURE,
        samesite=settings.REFRESH_TOKEN_COOKIE_SAMESITE,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/api/v1/auth",
    )

    return TokenResponse(
        access_token=access_token,
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    refresh_token_service: RefreshTokenService = Depends(
        get_refresh_token_service,
    ),
) -> TokenResponse:
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token.",
        )

    try:
        new_refresh_token, user_id = refresh_token_service.rotate(
            refresh_token,
        )
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token.",
        ) from exc

    access_token = create_access_token(
        subject=str(user_id),
    )

    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        value=new_refresh_token,
        httponly=True,
        secure=settings.REFRESH_TOKEN_COOKIE_SECURE,
        samesite=settings.REFRESH_TOKEN_COOKIE_SAMESITE,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/api/v1/auth",
    )

    return TokenResponse(
        access_token=access_token,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    refresh_token_service: RefreshTokenService = Depends(
        get_refresh_token_service,
    ),
) -> None:
    if refresh_token is not None:
        refresh_token_service.revoke(refresh_token)

    response.delete_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        path="/api/v1/auth",
    )


@router.post(
    "/token",
    response_model=TokenResponse,
)
def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    try:
        user = auth_service.authenticate(
            UserLogin(
                email=form_data.username,
                password=form_data.password,
            )
        )
    except AuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        ) from exc

    access_token = create_access_token(
        subject=str(user.id),
    )

    return TokenResponse(
        access_token=access_token,
    )


@router.get("/google")
async def google_login(request: Request):
    """Redirect the user to Google's OAuth consent screen."""

    redirect_uri = request.url_for("google_callback")

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri,
    )


@router.get("/google/callback")
async def google_callback(
    request: Request,
    oauth_service: OAuthService = Depends(get_oauth_service),
    refresh_token_service: RefreshTokenService = Depends(
        get_refresh_token_service,
    ),
):
    """Handle Google's OAuth callback."""

    token = await oauth.google.authorize_access_token(request)

    userinfo = token["userinfo"]
    if not userinfo.get("email_verified"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google email address is not verified.",
        )

    google_user_id = userinfo["sub"]
    email = userinfo["email"]
    full_name = userinfo.get("name")

    user = oauth_service.authenticate(
        provider="google",
        provider_user_id=google_user_id,
        email=email,
        full_name=full_name,
    )

    refresh_token = refresh_token_service.create(
        user_id=user.id,
    )
    redirect_response = RedirectResponse(
        url=f"{settings.FRONTEND_URL}/oauth/callback"
    )

    redirect_response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=settings.REFRESH_TOKEN_COOKIE_SECURE,
        samesite=settings.REFRESH_TOKEN_COOKIE_SAMESITE,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/api/v1/auth",
    )

    return redirect_response
