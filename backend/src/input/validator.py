import pandas as pd
from typing import List, Dict, Any

class DataValidationError(Exception):
    """Raised when input data fails schema or logic validation."""
    pass

def validate_students(df: pd.DataFrame) -> None:
    required_cols = {"student_id", "name", "major"}
    if not required_cols.issubset(df.columns):
        missing = required_cols - set(df.columns)
        raise DataValidationError(f"Students data missing columns: {missing}")
        
    if df["student_id"].isnull().any():
        raise DataValidationError("student_id cannot be null")
        
def validate_courses(df: pd.DataFrame) -> None:
    required_cols = {"course_id", "course_name", "semester"}
    if not required_cols.issubset(df.columns):
        missing = required_cols - set(df.columns)
        raise DataValidationError(f"Courses data missing columns: {missing}")
        
    if df["course_id"].isnull().any():
        raise DataValidationError("course_id cannot be null")
        
def validate_grades(df: pd.DataFrame) -> None:
    required_cols = {"student_id", "course_id", "assessment", "score"}
    if not required_cols.issubset(df.columns):
        missing = required_cols - set(df.columns)
        raise DataValidationError(f"Grades data missing columns: {missing}")
        
    if df["score"].isnull().any():
        raise DataValidationError("score cannot be null")
        
    if (df["score"] < 0).any() or (df["score"] > 10).any():
        raise DataValidationError("score must be between 0 and 10")
        
def validate_attendance(df: pd.DataFrame) -> None:
    required_cols = {"student_id", "course_id", "session", "status"}
    if not required_cols.issubset(df.columns):
        missing = required_cols - set(df.columns)
        raise DataValidationError(f"Attendance data missing columns: {missing}")
        
    valid_statuses = {"Present", "Absent", "Late"}
    invalid_statuses = set(df["status"].unique()) - valid_statuses
    if invalid_statuses:
        raise DataValidationError(f"Invalid attendance status found: {invalid_statuses}")
