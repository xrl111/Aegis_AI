import pandas as pd

def normalize_submissions(df_submissions: pd.DataFrame) -> pd.DataFrame:
    """Tính toán hành vi nộp bài (stub).
    
    Trong hệ thống thực tế, module này sẽ tính on_time_rate và missing_rate.
    Hiện tại, dữ liệu sample chưa có bảng submissions nên hàm này đóng vai
    trò stub cho kiến trúc.
    
    Args:
        df_submissions: DataFrame chứa dữ liệu nộp bài.
        
    Returns:
        DataFrame với cột 'submission_score' [0, 1].
    """
    df = df_submissions.copy()
    if df.empty:
        df["submission_score"] = pd.Series(dtype=float)
        return df
        
    # Logic giả định: submission_score = 1 nếu nộp, 0 nếu missing, 0.5 nếu trễ
    df["submission_score"] = df["status"].apply(
        lambda x: 1.0 if x == "OnTime" else (0.5 if x == "Late" else 0.0)
    )
    return df
