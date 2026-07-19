from src.detection.grade_signal import SignalResult
from src.detection.attendance_signal import AttendanceSignalResult
from src.detection.submission_signal import SubmissionSignalResult

def explain_grade_signal(result: SignalResult) -> str:
    """Tạo giải thích bằng tiếng Việt cho biến động điểm số."""
    if not result["is_triggered"]:
        return "Kết quả học tập duy trì ở mức bình thường."
    return "Điểm số gần đây thấp hơn đáng kể so với năng lực thường thấy của học sinh này."

def explain_attendance_signal(result: AttendanceSignalResult) -> str:
    if not result["is_triggered"]:
        return "Tỷ lệ chuyên cần duy trì tốt."
    return "Học sinh vắng mặt quá mức cho phép trong thời gian gần đây."

def explain_submission_signal(result: SubmissionSignalResult) -> str:
    if not result["is_triggered"]:
        return "Nộp bài đầy đủ và đúng hạn."
    return "Có dấu hiệu nộp trễ hoặc bỏ bài tập."
