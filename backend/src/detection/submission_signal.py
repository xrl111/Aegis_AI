from typing import TypedDict

SUBMISSION_THRESHOLD = 0.5  # Nếu nộp trễ/thiếu quá nửa số bài thì cảnh báo

class SubmissionSignalResult(TypedDict):
    submission_score: float
    is_triggered: bool
    data_sufficiency: str

def compute_submission_signal(submission_score: float) -> SubmissionSignalResult:
    """Tính tín hiệu hành vi nộp bài (stub)."""
    # Vì là stub, giả định logic cơ bản: < 0.5 là trigger
    is_triggered = submission_score <= SUBMISSION_THRESHOLD
    
    return {
        "submission_score": round(submission_score, 2),
        "is_triggered": is_triggered,
        "data_sufficiency": "sufficient"
    }
