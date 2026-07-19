import numpy as np
import pandas as pd

MAD_FLOOR = 0.05  # Prevent division by zero and explosion of z-score for consistent students
WINDOW_SIZE = 5   # Look at the last 5 data points for rolling baseline

def compute_rolling_baseline(scores: pd.Series) -> tuple[float, float]:
    """Tính toán Baseline (Median) và MAD (Median Absolute Deviation) trượt.
    
    Args:
        scores: Series chứa các điểm số đã chuẩn hoá theo thứ tự thời gian.
        
    Returns:
        tuple (baseline_median, baseline_mad).
    """
    # Dùng WINDOW_SIZE điểm gần nhất (không tính điểm hiện tại đang xét, 
    # nhưng ở logic gọi hàm chúng ta sẽ truyền window history tương ứng)
    
    if len(scores) == 0:
        return 0.0, MAD_FLOOR
        
    window = scores.tail(WINDOW_SIZE)
    
    baseline_median = float(np.median(window))
    
    # Tính MAD: median(|x_i - median|)
    deviations = np.abs(window - baseline_median)
    mad = float(np.median(deviations))
    
    # Apply MAD_FLOOR to prevent z-score explosion
    baseline_mad = max(mad, MAD_FLOOR)
    
    return baseline_median, baseline_mad
