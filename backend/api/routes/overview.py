from fastapi import APIRouter
from api.schemas import OverviewStats
from api.routes.students import service

router = APIRouter(prefix="/api/overview", tags=["overview"])

@router.get("/stats", response_model=OverviewStats)
def get_overview_stats():
    """Lấy thống kê tổng quan (số lượng học sinh theo từng mức cảnh báo)."""
    return service.get_dashboard_stats()
