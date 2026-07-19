import pandas as pd
from typing import TypedDict
from src.baseline.rolling import compute_rolling_baseline

GRADE_THRESHOLD = -2.0  # Ngưỡng z-score để cảnh báo (rớt > 2 MAD)

class SignalResult(TypedDict):
    z_score: float
    is_triggered: bool
    data_sufficiency: str

def compute_grade_signal(scores: pd.Series) -> SignalResult:
    """Tính tín hiệu biến động điểm dựa trên Robust Z-score.
    
    Args:
        scores: Series điểm số đã chuẩn hoá theo thời gian. Phần tử cuối 
                cùng là điểm hiện tại, các phần tử trước là lịch sử.
                Đã qua Data Gate để đảm bảo len(scores) >= 3.
                
    Returns:
        SignalResult chứa z_score, is_triggered, và trạng thái data.
    """
    history = scores.iloc[:-1]
    current_score = float(scores.iloc[-1])
    
    median, mad = compute_rolling_baseline(history)
    
    # Tính Robust Z-score
    z_score = (current_score - median) / mad
    
    is_triggered = z_score <= GRADE_THRESHOLD
    
    return {
        "z_score": round(z_score, 2),
        "is_triggered": is_triggered,
        "data_sufficiency": "sufficient"
    }
