import pandas as pd
import os
from .validator import (
    validate_students,
    validate_courses,
    validate_grades,
    validate_attendance,
    DataValidationError
)

class DataLoader:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def load_students(self) -> pd.DataFrame:
        path = os.path.join(self.data_dir, "students.csv")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing {path}")
        df = pd.read_csv(path)
        validate_students(df)
        return df

    def load_courses(self) -> pd.DataFrame:
        path = os.path.join(self.data_dir, "courses.csv")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing {path}")
        df = pd.read_csv(path)
        validate_courses(df)
        return df

    def load_grades(self) -> pd.DataFrame:
        path = os.path.join(self.data_dir, "grades.csv")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing {path}")
        df = pd.read_csv(path)
        validate_grades(df)
        return df

    def load_attendance(self) -> pd.DataFrame:
        path = os.path.join(self.data_dir, "attendance.csv")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing {path}")
        df = pd.read_csv(path)
        validate_attendance(df)
        return df
