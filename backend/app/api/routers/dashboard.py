from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_dashboard_service
from app.models.user import User
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard import DashboardService


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "",
    response_model=DashboardResponse,
)
def get_dashboard(
    current_user: User = Depends(get_current_user),
    dashboard_service: DashboardService = Depends(
        get_dashboard_service,
    ),
) -> DashboardResponse:
    """Return dashboard data for the current user."""

    return dashboard_service.get_dashboard(
        user_id=current_user.id,
    )