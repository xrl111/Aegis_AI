# Aegis AI — Project Rules & Conventions

> Hệ thống Cảnh báo Sớm Học sinh Có Nguy cơ Bỏ học
> Rule-based, Individual Baseline, Privacy-first

---

## 1. Tech Stack

| Layer | Công nghệ | Ghi chú |
|-------|-----------|---------|
| **Backend** | | |
| Language | **Python 3.11+** | Toàn bộ backend |
| API Framework | **FastAPI** | REST API + Swagger auto-docs |
| Data Processing | **Pandas, NumPy, SciPy** | Không dùng ML frameworks (sklearn, xgboost...) cho core engine |
| Testing | **Pytest + httpx** | Unit test engine + API integration test |
| Linting | **Ruff** | Format + lint |
| Type Checking | **Type hints** bắt buộc cho mọi function signature | |
| **Frontend** | | |
| Framework | **Vue 3** + TypeScript | Composition API, `<script setup>` |
| Router | **Vue Router** | SPA routing |
| State | **Pinia** | Store management |
| Build | **Vite** | Dev server port 5173 |
| HTTP Client | **Axios** hoặc **fetch** | Gọi backend API |
| UI Library | **Tự chọn** (PrimeVue, Vuetify, hoặc custom CSS) | Cần thống nhất trước khi code |

---

## 2. Quy tắc code

### 2.1 Backend — Python Naming

```python
# Files & modules: snake_case
baseline_engine.py
detection_engine.py

# Classes: PascalCase
class BaselineEngine:
class StudentTimeline:

# Functions & variables: snake_case
def compute_grade_signal(student_id: str) -> SignalResult:
    rolling_median = ...

# Constants: UPPER_SNAKE_CASE
WINDOW_SIZE = 10
MAD_FLOOR = 0.05
GRADE_THRESHOLD = -2.0
```

### 2.2 Frontend — Vue/TypeScript Naming

```typescript
// Components: PascalCase (file & tag)
StatusBadge.vue
AlertCard.vue
TimelineChart.vue

// Composables: camelCase, prefix "use"
useStudentStore.ts
useAlertLevel.ts

// Types/Interfaces: PascalCase
interface StudentSummary { ... }
interface SignalResult { ... }

// Variables & functions: camelCase
const alertLevel = ref<AlertLevel>('stable')
function fetchStudentDetail(id: string): Promise<StudentDetail> { ... }
```

### 2.3 Docstring (Backend)

Mọi function public **bắt buộc** có docstring theo format:

```python
def compute_grade_signal(student_id: str, semester: int) -> SignalResult:
    """Tính tín hiệu biến động điểm cho một học sinh.

    So sánh điểm gần đây với baseline cá nhân (rolling + anchor).
    Trả về robust z-score và explanation text.

    Args:
        student_id: Mã sinh viên.
        semester: Kỳ học hiện tại (>=2).

    Returns:
        SignalResult với z_score, is_triggered, và explanation.

    Raises:
        InsufficientDataError: Khi chưa đủ data points tối thiểu.
    """
```

### 2.4 Comments

- Comment **tại sao**, không comment **cái gì** (code tự giải thích cái gì)
- Mọi threshold/magic number phải có comment giải thích lý do chọn giá trị đó
- Comment bằng **tiếng Việt** cho logic nghiệp vụ, tiếng Anh cho logic kỹ thuật thuần

```python
# Dùng median thay vì mean vì điểm lab thường lệch phải (skewed)
baseline = np.median(scores)

# MAD floor prevents z-score explosion when student is perfectly consistent
mad = max(compute_mad(scores), MAD_FLOOR)
```

### 2.5 Error Handling (Backend)

- **KHÔNG** dùng bare `except:` hoặc `except Exception:`
- Thiếu dữ liệu → raise `InsufficientDataError` (custom exception) — KHÔNG return giá trị mặc định
- Validation errors → raise sớm, fail fast
- API layer: catch engine exceptions → trả HTTP response phù hợp

```python
# ✅ Đúng
if len(scores) < MIN_GRADE_POINTS:
    raise InsufficientDataError(
        student_id=student_id,
        signal="grade",
        available=len(scores),
        required=MIN_GRADE_POINTS,
    )

# ❌ Sai — nuốt lỗi, giả vờ đủ data
if len(scores) < MIN_GRADE_POINTS:
    return SignalResult(z_score=0.0, is_triggered=False)
```

### 2.6 Frontend — Component Structure

```vue
<!-- Template: mỗi component 1 responsibility -->
<template>
  <div class="alert-card" :class="levelClass">
    <h3>{{ headline }}</h3>
    <div v-if="expanded">{{ details }}</div>
  </div>
</template>

<script setup lang="ts">
// Props → computed → methods → lifecycle
// Mọi API call đi qua Pinia store, component KHÔNG gọi API trực tiếp
</script>
```

---

## 3. Git Workflow

### 3.1 Branch Strategy

```
main                    ← Chỉ merge từ develop, luôn chạy được
├── develop             ← Branch tích hợp, merge feature vào đây
│   ├── feat/be-module-name     ← Backend feature
│   ├── feat/fe-component-name  ← Frontend feature
│   ├── fix/be-bug-description  ← Backend bug fix
│   ├── fix/fe-bug-description  ← Frontend bug fix
│   └── refactor/scope          ← Refactor
```

### 3.2 Branch Naming

```
feat/be-baseline-engine     # Backend module
feat/be-api-students        # Backend API endpoint
feat/fe-overview-page       # Frontend page
feat/fe-timeline-chart      # Frontend component
fix/be-mad-floor-zero       # Backend bug fix
fix/fe-badge-color           # Frontend bug fix
```

### 3.3 Commit Message

Format: `<type>(<scope>): <mô tả ngắn>`

```
feat(be/baseline): implement rolling median + MAD with floor
feat(be/api): add GET /api/students endpoint
feat(fe/overview): implement student list with status badges
feat(fe/chart): add timeline chart component
fix(be/detection): handle MAD=0 edge case
fix(fe/badge): correct color mapping for improving state
test(be/fusion): add multi-signal fusion test cases
chore(fe): update vite config for proxy
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`
Scopes: `be/...` cho backend, `fe/...` cho frontend

### 3.4 Pull Request

- Mỗi PR phải có **ít nhất 1 reviewer** approve
- PR description phải nêu: thay đổi gì, tại sao, test thế nào
- Không merge PR nếu tests fail
- Backend PR: phải kèm pytest results
- Frontend PR: phải kèm screenshot UI nếu có visual change

---

## 4. Quy tắc kiến trúc

### 4.1 Tách biệt Backend & Frontend

```
backend/     ← Python, FastAPI, engine logic
frontend/    ← Vue 3, TypeScript, UI
```

- Frontend **CHỈ** giao tiếp với Backend qua **REST API** (`/api/...`)
- Frontend **KHÔNG** import bất kỳ Python module nào
- Backend **KHÔNG** chứa HTML/CSS/JS
- API contract được định nghĩa trong `backend/api/schemas.py`

### 4.2 Backend Module Boundaries

- Mỗi module là **1 folder** với `__init__.py` export public API
- Module **KHÔNG** import trực tiếp internal functions của module khác
- Giao tiếp giữa modules qua **data classes** định nghĩa trong `src/models/`

```python
# ✅ Đúng — import từ public API
from src.baseline import BaselineEngine

# ❌ Sai — import internal
from src.baseline.rolling import _compute_rolling_mad
```

### 4.3 Data Flow Direction

```
[CSV] → input → normalize → merge → baseline → detection → alert → [API] → [Frontend]
```

- Data chảy **MỘT CHIỀU** từ trái sang phải
- Module sau có thể đọc output module trước, KHÔNG được gọi ngược lại
- API layer là **adapter mỏng** giữa engine và frontend
- Frontend KHÔNG biết engine internals

### 4.4 Configuration

- Tất cả thresholds, constants, window sizes → tập trung trong `backend/config.yaml`
- **KHÔNG** hardcode magic numbers trong logic code
- Config load qua `backend/src/config.py`
- Frontend config (API URL, etc.) trong `frontend/.env`

### 4.5 API Design Rules

- Tất cả endpoints prefix `/api/`
- Response **KHÔNG chứa z-score** — chuyển thành ngôn ngữ tự nhiên trước khi trả
- Error responses dùng HTTP status codes chuẩn
- Mọi response trả JSON, kèm field `explanation` bằng tiếng Việt khi cần

---

## 5. Ràng buộc đạo đức — KHÔNG ĐƯỢC VI PHẠM

Đây là **hard rules**, không có ngoại lệ:

### 🔴 KHÔNG BAO GIỜ

1. **Không phân tích cảm xúc** — không sentiment analysis, không đọc nội dung cá nhân
2. **Không so sánh với đám đông để TẠO cảnh báo** — không Isolation Forest, không clustering, không class ranking
3. **Không gắn nhãn kết quả** — không có "sẽ bỏ học", "nguy hiểm", "yếu kém"
4. **Không tự động kỷ luật** — hệ thống KHÔNG trigger hành động, chỉ hiển thị thông tin
5. **Không tự điều chỉnh ngưỡng** — ngưỡng chỉ được admin thay đổi thủ công
6. **API KHÔNG trả z-score cho frontend** — chuyển thành ngôn ngữ tự nhiên

### ✅ LUÔN LUÔN

1. **Tên/MSSV là identifier** — chỉ dùng để join data và hiển thị, không đưa vào computation
2. **Thiếu dữ liệu → nói thiếu** — trả về "Chưa đủ dữ liệu", không suy đoán
3. **Mỗi cảnh báo phải tự giải thích** — tín hiệu nào, từ khi nào, so với gì
4. **Giáo viên quyết định cuối cùng** — hệ thống chỉ gợi ý, giáo viên hành động

### ⚠️ NGOẠI LỆ DUY NHẤT cho class-level comparison

Seasonal filter được dùng class-level statistics **CHỈ ĐỂ SUPPRESS** (loại bỏ) cảnh báo khi cả lớp cùng xấu đi, **KHÔNG BAO GIỜ** dùng để tạo cảnh báo.

---

## 6. Testing Rules

### Backend
- Mỗi module engine (normalize, baseline, detection, fusion) **bắt buộc** có unit tests
- API endpoints **bắt buộc** có integration tests (dùng httpx + TestClient)
- Test phải cover: happy path, edge cases (MAD=0, empty data, 1 data point), boundary conditions
- Test data dùng fixtures trong `backend/tests/fixtures/` — KHÔNG dùng production data
- Tên test: `test_<function>_<scenario>`

```python
def test_compute_mad_with_constant_scores_returns_floor():
    """MAD of identical scores should return MAD_FLOOR, not 0."""

def test_fusion_requires_minimum_two_signals():
    """Fusion should return INSUFFICIENT when < 2 signals available."""

def test_seasonal_filter_suppresses_not_creates_alerts():
    """Seasonal flag should only suppress, never create alerts."""

def test_api_students_returns_no_zscore():
    """API response must NOT contain raw z-score values."""
```

### Frontend
- Component tests nếu có thời gian (optional cho demo)
- **Bắt buộc**: test manual flow overview → detail → feedback

---

## 7. Quy tắc Dashboard / UI

- Ngôn ngữ hiển thị: **Tiếng Việt**
- Trạng thái dùng **màu sắc** rõ ràng:

| Mức | Màu | Label |
|-----|-----|-------|
| Ổn định | 🟢 Xanh lá | Ổn định |
| Theo dõi | 🟡 Vàng | Theo dõi thay đổi |
| Cần xem xét | 🟠 Cam | Cần giáo viên xem xét |
| Chưa đủ DL | ⬜ Xám | Chưa đủ dữ liệu |
| Đang cải thiện | 🔵 Xanh dương | Đang cải thiện |

- **KHÔNG** hiển thị z-score trực tiếp cho giáo viên — chuyển thành ngôn ngữ tự nhiên
- Mỗi cảnh báo có 2 tầng: headline (1 dòng) + chi tiết (expandable)
- Mọi API call đi qua Pinia store, component KHÔNG gọi API trực tiếp
