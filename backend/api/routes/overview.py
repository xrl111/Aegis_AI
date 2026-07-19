from fastapi import APIRouter
from api.schemas import OverviewStats
from api.routes.students import service

router = APIRouter(prefix="/api/overview", tags=["overview"])

@router.get("/stats", response_model=OverviewStats)
def get_overview_stats():
    """Lấy thống kê tổng quan (số lượng học sinh theo từng mức cảnh báo)."""
    summaries = service.get_all_students()
    
    stats = {
        "total_students": len(summaries),
        "stable_count": sum(1 for s in summaries if s.alert_level == "stable"),
        "watch_count": sum(1 for s in summaries if s.alert_level == "watch"),
        "review_count": sum(1 for s in summaries if s.alert_level == "review"),
        "insufficient_count": sum(1 for s in summaries if s.alert_level == "insufficient_data"),
        "improving_count": sum(1 for s in summaries if s.alert_level == "improving"),
    }
    
    return OverviewStats(**stats)
