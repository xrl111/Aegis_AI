"""API routes — Students endpoints.

GET /api/students          → Danh sách tất cả HS + trạng thái
GET /api/students/{id}     → Chi tiết 1 HS + signals + timeline
"""

from fastapi import APIRouter, HTTPException

from api.schemas import StudentSummary, StudentDetail

router = APIRouter()


@router.get("", response_model=list[StudentSummary])
def list_students() -> list[StudentSummary]:
    """Lấy danh sách tất cả học sinh với trạng thái hiện tại."""
    # TODO: Kết nối với engine pipeline
    raise HTTPException(status_code=501, detail="Chưa implement")


@router.get("/{student_id}", response_model=StudentDetail)
def get_student_detail(student_id: str) -> StudentDetail:
    """Lấy chi tiết 1 học sinh: signals, timeline, alert history."""
    # TODO: Kết nối với engine pipeline
    raise HTTPException(status_code=501, detail="Chưa implement")
