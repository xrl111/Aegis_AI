import pandas as pd

def merge_cross_course_grades(df_norm_grades: pd.DataFrame) -> pd.DataFrame:
    """Gộp điểm số của nhiều môn học song song.
    
    Lấy trung vị (median) của normalized_score tại mỗi bước đánh giá 
    (theo thứ tự assessment) để ra 1 con số chung đại diện cho năng lực.
    """
    df = df_norm_grades.copy()
    
    if df.empty:
        return pd.DataFrame(columns=["student_id", "assessment", "merged_score"])
        
    # Gom nhóm theo student_id và assessment
    df_merged = df.groupby(["student_id", "assessment"], as_index=False)["normalized_score"].median()
    df_merged = df_merged.rename(columns={"normalized_score": "merged_score"})
    
    return df_merged

def merge_cross_course_attendance(df_norm_attendance: pd.DataFrame) -> pd.DataFrame:
    """Gộp điểm danh của nhiều môn học song song.
    
    Lấy trung bình (mean) của attendance_rate tại mỗi session
    để ra tỷ lệ chuyên cần chung của học sinh.
    Dùng mean thay vì median để phản ánh đúng % vắng mặt tổng hợp.
    """
    df = df_norm_attendance.copy()
    
    if df.empty:
        return pd.DataFrame(columns=["student_id", "session", "merged_rate"])
        
    df_merged = df.groupby(["student_id", "session"], as_index=False)["attendance_rate"].mean()
    df_merged = df_merged.rename(columns={"attendance_rate": "merged_rate"})
    
    return df_merged
