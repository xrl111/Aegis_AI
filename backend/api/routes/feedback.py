from fastapi import APIRouter
from api.schemas import FeedbackRequest, FeedbackResponse

router = APIRouter(prefix="/api/feedback", tags=["feedback"])

@router.post("", response_model=FeedbackResponse)
def submit_feedback(request: FeedbackRequest):
    """Ghi nhận phản hồi của giáo viên về cảnh báo của học sinh.
    
    Trong hệ thống thực tế, action này sẽ lưu vào DB và reset
    hoặc cập nhật trạng thái cảnh báo của học sinh đó.
    """
    # Demo: print to console and return success
    print(f"Feedback received for {request.student_id} by {request.teacher_id}: {request.action_taken}")
    if request.notes:
        print(f"Notes: {request.notes}")
        
    return FeedbackResponse(
        success=True,
        message="Đã ghi nhận phản hồi thành công."
    )
