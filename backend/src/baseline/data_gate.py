import pandas as pd
from src.exceptions import InsufficientDataError

def check_data_sufficiency(df: pd.DataFrame, student_id: str, signal_name: str, min_points: int = 3):
    """Kiểm tra số lượng data points tối thiểu trước khi tính toán.
    
    Raises:
        InsufficientDataError nếu không đủ số lượng mẫu yêu cầu.
    """
    if len(df) < min_points:
        raise InsufficientDataError(
            student_id=student_id,
            signal=signal_name,
            available=len(df),
            required=min_points
        )
