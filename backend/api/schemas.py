"""Aegis AI — API Response Schemas.

Pydantic models cho API responses. Tách biệt với internal data models
(src/models/) để frontend contract không phụ thuộc vào engine internals.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class AlertLevelOut(str, Enum):
    """Mức cảnh báo — trả về cho frontend."""
    INSUFFICIENT_DATA = "insufficient_data"
    STABLE = "stable"
    WATCH = "watch"
    REVIEW = "review"
    IMPROVING = "improving"


class SignalOut(BaseModel):
    """1 tín hiệu — phiên bản frontend-safe (không có z-score)."""
    signal_type: str                    # "grade" | "attendance" | "submission"
    is_triggered: bool
    data_sufficiency: str               # "sufficient" | "partial" | "insufficient"
    explanation: str                    # Ngôn ngữ tự nhiên, tiếng Việt


class StudentSummary(BaseModel):
    """Tóm tắt 1 học sinh cho Overview page."""
    student_id: str
    student_name: str
    major: str
    alert_level: AlertLevelOut
    headline: str                       # 1 dòng tóm tắt
    triggered_signal_count: int         # Số signals đang triggered
    updated_at: Optional[datetime] = None


class ComponentGrade(BaseModel):
    assessment: str
    score: float


class CourseDetail(BaseModel):
    course_id: str
    course_name: str
    semester: int
    grades: List[ComponentGrade]
    attendance_rate: float


class StudentDetail(BaseModel):
    """Chi tiết 1 học sinh cho Detail page."""
    student_id: str
    student_name: str
    major: str
    alert_level: AlertLevelOut
    headline: str
    signals: List[SignalOut]
    timeline: List[TimelinePoint]
    courses: List[CourseDetail] = []
    alert_history: List[dict] = []
    is_seasonal_suppressed: bool = False


class TimelinePoint(BaseModel):
    """1 điểm trên biểu đồ timeline."""
    week: str                           # "2026-W12"
    grade_value: Optional[float] = None         # Normalized [0,1]
    attendance_value: Optional[float] = None    # Rate [0,1]
    submission_value: Optional[float] = None    # Rate [0,1]


class AlertHistoryItem(BaseModel):
    """1 entry trong lịch sử cảnh báo."""
    date: datetime
    level: AlertLevelOut
    headline: str
    details: list[str]


class OverviewStats(BaseModel):
    """Thống kê tổng quan cho Dashboard."""
    total_students: int
    stable_count: int
    watch_count: int
    review_count: int
    insufficient_count: int
    improving_count: int


class FeedbackRequest(BaseModel):
    """Request body khi giáo viên ghi nhận phản hồi."""
    student_id: str
    teacher_id: str
    action_taken: str                   # "contacted" | "meeting" | "dismissed" | "noted"
    notes: str = ""


class FeedbackResponse(BaseModel):
    """Response sau khi ghi nhận phản hồi."""
    success: bool
    message: str


# Cần khai báo TimelinePoint trước StudentDetail vì forward reference
StudentDetail.model_rebuild()
