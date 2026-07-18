import pandas as pd
from typing import Dict

def normalize_grades(df_grades: pd.DataFrame, max_score: float = 10.0) -> pd.DataFrame:
    """Chuẩn hóa điểm số về thang [0, 1].
    
    Args:
        df_grades: DataFrame chứa dữ liệu điểm (đã qua input validator).
        max_score: Điểm tối đa có thể đạt được (mặc định 10.0 ở Việt Nam).
        
    Returns:
        DataFrame mới với cột 'normalized_score' được thêm vào.
    """
    df = df_grades.copy()
    
    # Đảm bảo điểm không vượt quá thang đo
    df["normalized_score"] = df["score"] / max_score
    df["normalized_score"] = df["normalized_score"].clip(lower=0.0, upper=1.0)
    
    return df
