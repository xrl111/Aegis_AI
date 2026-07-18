"""API routes — Teacher Feedback.

POST /api/feedback         → Ghi nhận phản hồi của giáo viên
GET  /api/feedback/{id}    → Lấy lịch sử feedback cho 1 HS
"""

from fastapi import APIRouter, HTTPException

from api.schemas import FeedbackRequest, FeedbackResponse

router = APIRouter()


@router.post("", response_model=FeedbackResponse)
def submit_feedback(request: FeedbackRequest) -> FeedbackResponse:
    """Ghi nhận phản hồi của giáo viên.

    Hệ thống CHỈ LOG, không tự động điều chỉnh ngưỡng hay hành vi.
    """
    # TODO: Lưu vào storage (JSON file hoặc SQLite cho demo)
    raise HTTPException(status_code=501, detail="Chưa implement")


@router.get("/{student_id}")
def get_feedback_history(student_id: str) -> list[dict]:
    """Lấy lịch sử phản hồi cho 1 học sinh."""
    # TODO: Đọc từ storage
    raise HTTPException(status_code=501, detail="Chưa implement")
