import pytest
import pandas as pd
from src.normalize import normalize_grades, normalize_attendance, normalize_submissions

def test_normalize_grades():
    df = pd.DataFrame({
        "score": [0.0, 5.0, 10.0, 12.0]  # Note: 12.0 should be clipped
    })
    
    res = normalize_grades(df)
    
    assert "normalized_score" in res.columns
    assert res["normalized_score"].tolist() == [0.0, 0.5, 1.0, 1.0]

def test_normalize_attendance():
    df = pd.DataFrame({
        "student_id": ["S1", "S1", "S1", "S2"],
        "course_id": ["C1", "C1", "C1", "C1"],
        "session": [1, 2, 3, 1],
        "status": ["Present", "Late", "Absent", "Present"]
    })
    
    res = normalize_attendance(df)
    
    assert "attendance_rate" in res.columns
    # S1 session 1: 1/1 = 1.0
    # S1 session 2: 2/2 = 1.0
    # S1 session 3: 2/3 = 0.666...
    # S2 session 1: 1/1 = 1.0
    
    rates = res["attendance_rate"].round(3).tolist()
    assert rates == [1.0, 1.0, 0.667, 1.0]

def test_normalize_submissions_empty():
    df = pd.DataFrame()
    res = normalize_submissions(df)
    assert "submission_score" in res.columns
    assert res.empty

def test_normalize_submissions():
    df = pd.DataFrame({
        "status": ["OnTime", "Late", "Missing"]
    })
    res = normalize_submissions(df)
    assert "submission_score" in res.columns
    assert res["submission_score"].tolist() == [1.0, 0.5, 0.0]
