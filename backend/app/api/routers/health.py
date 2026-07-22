from fastapi import APIRouter, status

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Health check",
)
def health_check() -> dict[str, str]:
    """Health check endpoint."""

    return {
        "status": "ok",
    }