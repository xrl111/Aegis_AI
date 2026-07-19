from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_get_overview_stats():
    response = client.get("/api/overview/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_students" in data
    assert "stable_count" in data
    assert data["total_students"] == 20  # from our generate.py script

def test_list_students():
    response = client.get("/api/students")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 20
    assert "student_id" in data[0]
    assert "alert_level" in data[0]
    # Verify no z_score in output
    assert "z_score" not in data[0]

def test_get_student_detail():
    # Test a specific student ID that exists in sample data (e.g. SV001)
    response = client.get("/api/students/SV001")
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == "SV001"
    assert "signals" in data
    assert "timeline" in data
    
    # Check ethical constraints: No z-score in signals
    for signal in data["signals"]:
        assert "z_score" not in signal
        assert "explanation" in signal

def test_submit_feedback():
    payload = {
        "student_id": "SV001",
        "teacher_id": "GV001",
        "action_taken": "meeting",
        "notes": "Test note"
    }
    response = client.post("/api/feedback", json=payload)
    assert response.status_code == 200
    assert response.json()["success"] is True
