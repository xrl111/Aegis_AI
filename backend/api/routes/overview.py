"""API routes — Overview/Dashboard statistics.

GET /api/overview/stats    → Thống kê tổng quan
"""

from fastapi import APIRouter, HTTPException

from api.schemas import OverviewStats

router = APIRouter()


@router.get("/stats", response_model=OverviewStats)
def get_overview_stats() -> OverviewStats:
    """Thống kê tổng quan: bao nhiêu HS mỗi mức cảnh báo."""
    # TODO: Kết nối với engine pipeline
    raise HTTPException(status_code=501, detail="Chưa implement")
