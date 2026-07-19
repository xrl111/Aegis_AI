import pytest
import pandas as pd
from src.baseline import compute_rolling_baseline, check_data_sufficiency, MAD_FLOOR
from src.exceptions import InsufficientDataError

def test_data_gate_sufficient():
    df = pd.DataFrame({"score": [1, 2, 3]})
    # should not raise
    check_data_sufficiency(df, "SV1", "grade", min_points=3)

def test_data_gate_insufficient():
    df = pd.DataFrame({"score": [1, 2]})
    with pytest.raises(InsufficientDataError) as exc:
        check_data_sufficiency(df, "SV1", "grade", min_points=3)
    assert "hiện có 2." in str(exc.value)
    assert "cần ít nhất 3" in str(exc.value)

def test_compute_rolling_baseline_normal():
    # 5 points: 6, 7, 8, 9, 10
    scores = pd.Series([6.0, 7.0, 8.0, 9.0, 10.0])
    median, mad = compute_rolling_baseline(scores)
    
    assert median == 8.0
    # deviations from 8: |6-8|=2, |7-8|=1, |8-8|=0, |9-8|=1, |10-8|=2
    # deviations: [0, 1, 1, 2, 2] -> median is 1.0
    assert mad == 1.0

def test_compute_rolling_baseline_consistent_triggers_mad_floor():
    # 5 points of identical scores
    scores = pd.Series([8.0, 8.0, 8.0, 8.0, 8.0])
    median, mad = compute_rolling_baseline(scores)
    
    assert median == 8.0
    # True MAD is 0.0, but we expect MAD_FLOOR
    assert mad == MAD_FLOOR
