import pytest
import pandas as pd
from src.input.validator import (
    validate_students,
    validate_courses,
    validate_grades,
    validate_attendance,
    DataValidationError
)

def test_validate_students_missing_columns():
    df = pd.DataFrame({"student_id": ["SV001"]})
    with pytest.raises(DataValidationError, match="missing columns"):
        validate_students(df)

def test_validate_students_null_id():
    df = pd.DataFrame({
        "student_id": [None, "SV001"],
        "name": ["A", "B"],
        "major": ["IT", "IT"]
    })
    with pytest.raises(DataValidationError, match="student_id cannot be null"):
        validate_students(df)

def test_validate_grades_invalid_score():
    df = pd.DataFrame({
        "student_id": ["SV001"],
        "course_id": ["PRJ301"],
        "assessment": ["Lab_1"],
        "score": [11.5]  # Invalid score > 10
    })
    with pytest.raises(DataValidationError, match="score must be between 0 and 10"):
        validate_grades(df)

def test_validate_attendance_invalid_status():
    df = pd.DataFrame({
        "student_id": ["SV001"],
        "course_id": ["PRJ301"],
        "session": [1],
        "status": ["Sleeping"]  # Invalid status
    })
    with pytest.raises(DataValidationError, match="Invalid attendance status"):
        validate_attendance(df)

def test_validate_attendance_valid():
    df = pd.DataFrame({
        "student_id": ["SV001"],
        "course_id": ["PRJ301"],
        "session": [1],
        "status": ["Present"] 
    })
    # Should not raise exception
    validate_attendance(df)
