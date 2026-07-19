from typing import Literal

AlertLevel = Literal["stable", "watch", "review", "improving", "insufficient_data"]

def determine_alert_level(
    triggered_count: int, 
    is_seasonal_suppressed: bool, 
    previous_level: AlertLevel = "stable"
) -> AlertLevel:
    """Xác định mức cảnh báo dựa trên số lượng tín hiệu.
    
    Args:
        triggered_count: Số lượng tín hiệu bị kích hoạt (từ module fusion).
        is_seasonal_suppressed: True nếu lớp cũng rớt điểm chung đợt này.
        previous_level: Mức cảnh báo tuần trước (để xét trạng thái improving).
        
    Returns:
        Mức cảnh báo mới.
    """
    if triggered_count >= 2:
        if is_seasonal_suppressed:
            # Rớt chung cả lớp, không phạt nặng
            return "watch"
        return "review"
        
    if triggered_count == 1:
        return "watch"
        
    # triggered_count == 0
    if previous_level in ["review", "watch"]:
        return "improving"
        
    return "stable"
