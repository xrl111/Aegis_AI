---
name: backend-fastapi
description: |
  Skill hỗ trợ phát triển backend FastAPI cho Aegis AI.
  Trigger khi làm việc với Python backend, API endpoints, engine modules,
  tests, hoặc bất kỳ file nào trong backend/.
---

# Backend FastAPI — Development Skill

## Kiến trúc Backend

```
backend/
├── main.py              # FastAPI app entry — KHÔNG đặt logic ở đây
├── api/                 # API layer — thin adapter
│   ├── schemas.py       # Pydantic response models (frontend contract)
│   └── routes/          # Endpoint handlers
└── src/                 # Engine — core business logic
    ├── config.py        # Config loader (từ config.yaml)
    ├── exceptions.py    # InsufficientDataError, ValidationError
    ├── models/          # Shared data classes (internal contract)
    ├── input/           # ① CSV loader + validator
    ├── normalize/       # ② Per-course normalization
    ├── merge/           # ③ Cross-course time series merge
    ├── baseline/        # ④ Rolling + Anchor baseline
    ├── detection/       # ⑤ 3 signals + fusion + seasonal
    └── alert/           # ⑥ State machine + cooldown + explainer
```

## Quy tắc khi code backend

### 1. Engine vs API — Tách biệt rõ ràng

```python
# ✅ API route chỉ gọi engine, transform output
@router.get("/{student_id}")
def get_student(student_id: str) -> StudentDetail:
    try:
        result = engine.process_student(student_id)
        return transform_to_api_schema(result)
    except InsufficientDataError as e:
        return StudentDetail(alert_level="insufficient_data", ...)

# ❌ KHÔNG đặt business logic trong route
@router.get("/{student_id}")
def get_student(student_id: str):
    scores = pd.read_csv(...)  # KHÔNG — đây là việc của src/input/
    z_score = (x - median) / mad  # KHÔNG — đây là việc của src/detection/
```

### 2. API Response — KHÔNG trả z-score

```python
# ✅ Đúng — chuyển z-score thành ngôn ngữ tự nhiên
SignalOut(
    signal_type="grade",
    is_triggered=True,
    explanation="Điểm quiz gần đây thấp hơn đáng kể so với mức bình thường của em"
)

# ❌ Sai — trả raw z-score
{"z_score": -2.7, "threshold": -2.0}  # Frontend KHÔNG cần biết con số này
```

### 3. Config — Tập trung, không hardcode

```python
# ✅ Đúng — import từ config
from src.config import WINDOW_SIZE, MAD_FLOOR

# ❌ Sai — magic number
window = 10  # Tại sao 10? Ai quyết định?
```

### 4. Error Handling — Fail fast

```python
# ✅ Đúng — raise InsufficientDataError
if len(scores) < MIN_GRADE_POINTS:
    raise InsufficientDataError(student_id=sid, signal="grade",
                                 available=len(scores), required=MIN_GRADE_POINTS)

# ❌ Sai — nuốt lỗi
if len(scores) < MIN_GRADE_POINTS:
    return SignalResult(z_score=0.0, is_triggered=False)  # Giả vờ đủ data!
```

### 5. Testing pattern

```python
# Dùng httpx TestClient cho API tests
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200

# Dùng pytest fixtures cho engine tests
@pytest.fixture
def declining_student_grades():
    """Kịch bản: HS decline dần qua 6 tuần."""
    return [0.85, 0.80, 0.72, 0.65, 0.55, 0.40]
```

### 6. Chạy server

```bash
cd backend
uvicorn main:app --reload --port 8000
# Swagger: http://localhost:8000/docs
# Test:    pytest tests/ -v
```

## Ràng buộc đạo đức (luôn check)

- [ ] Không so sánh HS với HS khác để tạo cảnh báo
- [ ] Không return z-score trong API response
- [ ] Thiếu data → raise InsufficientDataError, KHÔNG return default
- [ ] Explanation bằng tiếng Việt, phi kỹ thuật
