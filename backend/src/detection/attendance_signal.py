from typing import TypedDict

ATTENDANCE_THRESHOLD = 0.75  # Cảnh báo nếu tỷ lệ đi học giảm dưới 75%

class AttendanceSignalResult(TypedDict):
    current_rate: float
    is_triggered: bool
    data_sufficiency: str

def compute_attendance_signal(current_rate: float) -> AttendanceSignalResult:
    """Tính tín hiệu chuyên cần.
    
    Khác với điểm số (cần tính rolling median), điểm danh có thể dùng 
    ngưỡng cứng (ví dụ: < 75%) vì nó là tỷ lệ tuyệt đối.
    """
    is_triggered = current_rate <= ATTENDANCE_THRESHOLD
    
    return {
        "current_rate": round(current_rate, 2),
        "is_triggered": is_triggered,
        "data_sufficiency": "sufficient"
    }
