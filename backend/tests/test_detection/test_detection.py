import pytest
import pandas as pd
from src.detection import (
    compute_grade_signal, 
    compute_attendance_signal, 
    compute_submission_signal,
    evaluate_fusion,
    check_seasonal_suppression
)

def test_grade_signal_triggers():
    # 5 history points around 8.0, then current score is 2.0
    # Median ~8.0, MAD = max(MAD, MAD_FLOOR)
    scores = pd.Series([8.0, 8.0, 8.0, 8.0, 8.0, 2.0])
    res = compute_grade_signal(scores)
    assert res["is_triggered"] is True
    assert res["z_score"] < -2.0

def test_grade_signal_not_triggered():
    scores = pd.Series([8.0, 8.0, 8.0, 8.0, 8.0, 7.95])
    res = compute_grade_signal(scores)
    assert res["is_triggered"] is False

def test_attendance_signal():
    assert compute_attendance_signal(0.70)["is_triggered"] is True
    assert compute_attendance_signal(0.80)["is_triggered"] is False

def test_fusion_requires_two_signals():
    grade = compute_grade_signal(pd.Series([8.0, 8.0, 8.0, 8.0, 8.0, 2.0])) # Triggered
    att = compute_attendance_signal(0.80) # Not triggered
    sub = compute_submission_signal(0.90) # Not triggered
    
    res = evaluate_fusion(grade, att, sub)
    assert res["triggered_count"] == 1
    assert res["is_fused_alert"] is False

    # Make attendance trigger too
    att = compute_attendance_signal(0.50)
    res = evaluate_fusion(grade, att, sub)
    assert res["triggered_count"] == 2
    assert res["is_fused_alert"] is True

def test_seasonal_filter_suppresses_not_creates_alerts():
    # Test rules: should return True to suppress if drop is >= 30%
    df = pd.DataFrame({
        "assessment": ["Lab1", "Lab1", "Lab2", "Lab2"],
        "normalized_score": [1.0, 1.0, 0.6, 0.6] # dropped 40% from 1.0 to 0.6
    })
    
    suppress = check_seasonal_suppression(df, "Lab2")
    assert bool(suppress) is True

    # If drop is small, do not suppress
    df2 = pd.DataFrame({
        "assessment": ["Lab1", "Lab1", "Lab2", "Lab2"],
        "normalized_score": [1.0, 1.0, 0.9, 0.9] # dropped 10%
    })
    assert check_seasonal_suppression(df2, "Lab2") is False
