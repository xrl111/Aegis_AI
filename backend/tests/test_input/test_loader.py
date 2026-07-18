import pytest
import pandas as pd
import os
from src.input.loader import DataLoader

def test_loader_missing_file(tmp_path):
    loader = DataLoader(data_dir=str(tmp_path))
    with pytest.raises(FileNotFoundError):
        loader.load_students()

def test_loader_success(tmp_path):
    # Create valid sample file in tmp_path
    df = pd.DataFrame({
        "student_id": ["SV001"],
        "name": ["Nguyen Van A"],
        "major": ["IT"]
    })
    df.to_csv(os.path.join(tmp_path, "students.csv"), index=False)
    
    loader = DataLoader(data_dir=str(tmp_path))
    loaded_df = loader.load_students()
    
    assert len(loaded_df) == 1
    assert loaded_df.iloc[0]["student_id"] == "SV001"
