import pandas as pd

def check_seasonal_suppression(df_course_grades: pd.DataFrame, current_assessment: str) -> bool:
    """Kiểm tra xem đợt kiểm tra hiện tại có phải là 'mùa vụ' khó bất thường không.
    
    Chỉ dùng data lớp (class-level) để MUTE (suppress) cảnh báo, 
    KHÔNG BAO GIỜ dùng để tạo cảnh báo. Đây là ràng buộc đạo đức quan trọng.
    
    Quy tắc giả định: Nếu điểm median của cả lớp rớt >= 30% so với bài trước,
    thì đây là đợt thi khó chung.
    """
    if df_course_grades.empty:
        return False
        
    # Tính median của từng assessment
    medians = df_course_grades.groupby("assessment")["normalized_score"].median()
    
    if len(medians) < 2 or current_assessment not in medians:
        return False
        
    # Lấy median hiện tại và median bài trước
    # Note: Trong thực tế cần sort assessment theo thời gian
    current_med = medians[current_assessment]
    
    # Giả định bài trước là bài có index trước đó
    idx = medians.index.get_loc(current_assessment)
    if idx == 0:
        return False
        
    prev_med = medians.iloc[idx - 1]
    
    if prev_med == 0:
        return False
        
    drop_ratio = (prev_med - current_med) / prev_med
    
    return bool(drop_ratio >= 0.3)
