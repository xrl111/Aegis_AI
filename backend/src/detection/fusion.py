from typing import TypedDict
from src.detection.grade_signal import SignalResult
from src.detection.attendance_signal import AttendanceSignalResult
from src.detection.submission_signal import SubmissionSignalResult

class FusionResult(TypedDict):
    triggered_count: int
    is_fused_alert: bool
    details: dict

def evaluate_fusion(
    grade: SignalResult, 
    attendance: AttendanceSignalResult, 
    submission: SubmissionSignalResult
) -> FusionResult:
    """Kết hợp đa tín hiệu (Multi-signal fusion).
    
    Quy tắc:
    - Nếu có >= 2 tín hiệu bị trigger cùng lúc -> is_fused_alert = True
    - Trả về số lượng tín hiệu bị trigger để State Machine quyết định Alert Level.
    """
    triggers = [
        grade["is_triggered"],
        attendance["is_triggered"],
        submission["is_triggered"]
    ]
    
    triggered_count = sum(triggers)
    
    return {
        "triggered_count": triggered_count,
        "is_fused_alert": triggered_count >= 2,
        "details": {
            "grade": grade,
            "attendance": attendance,
            "submission": submission
        }
    }
