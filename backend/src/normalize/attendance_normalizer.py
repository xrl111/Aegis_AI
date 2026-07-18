import pandas as pd

def normalize_attendance(df_attendance: pd.DataFrame) -> pd.DataFrame:
    """Tính toán tỷ lệ đi học (rolling attendance rate).
    
    Args:
        df_attendance: DataFrame chứa dữ liệu điểm danh.
        
    Returns:
        DataFrame mới với cột 'attendance_rate' đại diện cho tỷ lệ đi học
        tích lũy tính đến buổi học hiện tại (session).
    """
    df = df_attendance.copy()
    
    # Sort to ensure chronological order
    df = df.sort_values(by=["student_id", "course_id", "session"])
    
    # Tính điểm chuyên cần (Present/Late = 1, Absent = 0)
    # Trong một số trường hợp Late có thể tính 0.5, tạm thời tính 1.0
    df["is_present"] = df["status"].apply(lambda x: 1.0 if x in ["Present", "Late"] else 0.0)
    
    # Tính cumulative sum của số buổi có mặt và số buổi đã diễn ra
    df["cumulative_present"] = df.groupby(["student_id", "course_id"])["is_present"].cumsum()
    df["cumulative_sessions"] = df.groupby(["student_id", "course_id"]).cumcount() + 1
    
    # Tỷ lệ đi học (attendance_rate) = [0, 1]
    df["attendance_rate"] = df["cumulative_present"] / df["cumulative_sessions"]
    
    return df
