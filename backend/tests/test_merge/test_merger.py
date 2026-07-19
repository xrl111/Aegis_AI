import pytest
import pandas as pd
from src.merge import merge_cross_course_grades, merge_cross_course_attendance

def test_merge_grades():
    df = pd.DataFrame({
        "student_id": ["SV1", "SV1", "SV1"],
        "course_id": ["C1", "C2", "C3"],
        "assessment": ["Lab_1", "Lab_1", "Lab_1"],
        "normalized_score": [0.6, 0.8, 1.0]
    })
    
    res = merge_cross_course_grades(df)
    
    assert len(res) == 1
    assert res.iloc[0]["merged_score"] == 0.8  # median of [0.6, 0.8, 1.0]

def test_merge_attendance():
    df = pd.DataFrame({
        "student_id": ["SV1", "SV1", "SV1"],
        "course_id": ["C1", "C2", "C3"],
        "session": [1, 1, 1],
        "attendance_rate": [1.0, 1.0, 0.0]
    })
    
    res = merge_cross_course_attendance(df)
    
    assert len(res) == 1
    assert round(res.iloc[0]["merged_rate"], 3) == 0.667 # mean of [1.0, 1.0, 0.0]
