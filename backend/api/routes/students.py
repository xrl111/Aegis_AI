from fastapi import APIRouter, HTTPException
from typing import List
from api.schemas import StudentSummary, StudentDetail
from src.service.student_service import StudentService

router = APIRouter(prefix="/api/students", tags=["students"])

# Khởi tạo service 1 lần để cache data sample cho demo (trong thực tế sẽ lấy DB theo request)
service = StudentService()

@router.get("", response_model=List[StudentSummary])
def list_students():
    """Lấy danh sách tóm tắt toàn bộ học sinh cho Overview Table."""
    return service.get_all_students()

@router.get("/{student_id}", response_model=StudentDetail)
def get_student_detail(student_id: str):
    """Lấy chi tiết 1 học sinh, bao gồm timeline và signals."""
    try:
        return service.get_student_detail(student_id)
    except Exception as e:
        # Nếu student_id không tồn tại trong sample data
        raise HTTPException(status_code=404, detail=f"Student not found or error: {str(e)}")
