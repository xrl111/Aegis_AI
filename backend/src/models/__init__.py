"""Aegis AI — Data Models.

Data classes dùng chung giữa các modules.
Mọi giao tiếp giữa modules đi qua các model này.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional


# ── Enums ──────────────────────────────────────────────────────


class AssessmentType(str, Enum):
    LAB = "lab"
    QUIZ = "quiz"
    ASM = "asm"
    EXAM = "exam"


class AttendanceStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"


class DataSufficiency(str, Enum):
    SUFFICIENT = "sufficient"
    PARTIAL = "partial"          # Đủ tính nhưng confidence thấp
    INSUFFICIENT = "insufficient"


class AlertLevel(str, Enum):
    """4+1 mức trạng thái.

    Không có mức 'nguy hiểm' hay 'sẽ bỏ học' — chỉ phản ánh thay đổi.
    """
    INSUFFICIENT_DATA = "insufficient_data"  # Chưa đủ dữ liệu
    STABLE = "stable"                        # Ổn định
    WATCH = "watch"                          # Theo dõi thay đổi
    REVIEW = "review"                        # Cần giáo viên xem xét
    IMPROVING = "improving"                  # Đang cải thiện


# ── Data Records ───────────────────────────────────────────────


@dataclass(frozen=True)
class GradeRecord:
    student_id: str
    course_id: str
    assessment_type: AssessmentType
    assessment_number: int
    score: float
    max_score: float
    due_date: Optional[date] = None
    submitted_date: Optional[date] = None

    @property
    def normalized_score(self) -> float:
        """Score chuẩn hoá về [0, 1]."""
        return self.score / self.max_score if self.max_score > 0 else 0.0

    @property
    def is_late(self) -> bool:
        if self.due_date is None or self.submitted_date is None:
            return False
        return self.submitted_date > self.due_date

    @property
    def is_missing(self) -> bool:
        return self.submitted_date is None


@dataclass(frozen=True)
class AttendanceRecord:
    student_id: str
    course_id: str
    session_number: int
    session_date: date
    status: AttendanceStatus


# ── Signal Results ─────────────────────────────────────────────


@dataclass
class SignalResult:
    """Kết quả tính toán 1 tín hiệu.

    Attributes:
        signal_type: "grade" | "attendance" | "submission"
        z_score: Robust z-score so với baseline cá nhân (None nếu insufficient)
        is_triggered: True nếu vượt ngưỡng
        data_sufficiency: Mức đủ dữ liệu
        explanation: Giải thích bằng ngôn ngữ tự nhiên (tiếng Việt)
        detail_data: Dữ liệu chi tiết cho expandable view
    """
    signal_type: str
    z_score: Optional[float]
    is_triggered: bool
    data_sufficiency: DataSufficiency
    explanation: str
    detail_data: dict = field(default_factory=dict)


@dataclass
class FusionResult:
    """Kết quả fusion đa tín hiệu.

    Attributes:
        alert_level: Mức cảnh báo tổng hợp
        triggered_signals: Danh sách signals đã trigger
        all_signals: Tất cả signals (kể cả không trigger)
        headline: 1 dòng tóm tắt cho giáo viên
        is_seasonal_suppressed: True nếu bị suppress bởi seasonal filter
    """
    alert_level: AlertLevel
    triggered_signals: list[SignalResult] = field(default_factory=list)
    all_signals: list[SignalResult] = field(default_factory=list)
    headline: str = ""
    is_seasonal_suppressed: bool = False


# ── Baseline ───────────────────────────────────────────────────


@dataclass
class BaselineResult:
    """Kết quả tính baseline cá nhân.

    Attributes:
        anchor_median: Median cố định từ kỳ trước (None nếu chưa có)
        anchor_mad: MAD cố định từ kỳ trước
        rolling_median: Median rolling hiện tại
        rolling_mad: MAD rolling hiện tại (đã áp MAD floor)
        data_points_used: Số data points đã dùng
    """
    anchor_median: Optional[float]
    anchor_mad: Optional[float]
    rolling_median: float
    rolling_mad: float
    data_points_used: int


# ── Alert State ────────────────────────────────────────────────


@dataclass
class AlertState:
    """Trạng thái cảnh báo hiện tại của 1 học sinh.

    Attributes:
        student_id: Mã sinh viên (identifier, KHÔNG phải feature)
        current_level: Mức cảnh báo hiện tại
        previous_level: Mức trước đó (để detect transition)
        fusion_result: Kết quả fusion mới nhất
        last_alert_date: Ngày gửi alert gần nhất
        case_count_this_semester: Số cases đã mở trong kỳ
        updated_at: Thời điểm cập nhật
    """
    student_id: str
    current_level: AlertLevel
    previous_level: Optional[AlertLevel] = None
    fusion_result: Optional[FusionResult] = None
    last_alert_date: Optional[datetime] = None
    case_count_this_semester: int = 0
    updated_at: Optional[datetime] = None
