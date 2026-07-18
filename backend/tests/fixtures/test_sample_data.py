import pytest
import os
from src.input.loader import DataLoader

def test_load_sample_data():
    """Verify that the generated sample data can be loaded and passes all validations."""
    sample_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "sample")
    
    loader = DataLoader(data_dir=sample_dir)
    
    df_students = loader.load_students()
    df_courses = loader.load_courses()
    df_grades = loader.load_grades()
    df_attendance = loader.load_attendance()
    
    assert not df_students.empty
    assert not df_courses.empty
    assert not df_grades.empty
    assert not df_attendance.empty
    
    # Check if the specific scenarios exist
    assert "SV016" in df_students["student_id"].values # One of the edge cases
