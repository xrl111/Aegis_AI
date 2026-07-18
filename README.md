# Aegis AI — Hệ thống Cảnh báo Sớm Học sinh Có Nguy cơ Bỏ học

> Rule-based Early Warning System using Individual Baselines
> FastAPI Backend + Vue 3 Frontend

---

## Mô tả

Hệ thống phát hiện sớm học sinh có nguy cơ bỏ học dựa trên 3 tín hiệu phi xâm lấn:
1. **Biến động điểm** — so với baseline cá nhân
2. **Điểm danh** — pattern vắng gần đây
3. **Hành vi nộp bài** — nộp trễ / không nộp

Hệ thống **KHÔNG** phân loại, **KHÔNG** gắn nhãn, **KHÔNG** so với đám đông.

**Triết lý:** AI chỉ hỗ trợ phát hiện sớm — giáo viên đưa ra quyết định cuối cùng.

---

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# Swagger UI: http://localhost:8000/docs
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# Dev server: http://localhost:5173
```

### Tài khoản demo

| Email | Mật khẩu |
|-------|-----------|
| `admin@aegis.ai` | `123456` |
| `giao@aegis.ai` | `123456` |

---

## Tech Stack

| Layer | Công nghệ | Ghi chú |
|-------|-----------|---------|
| **Backend** | | |
| Language | **Python 3.11+** | Toàn bộ backend |
| API Framework | **FastAPI** | REST API + Swagger auto-docs |
| Data Processing | **Pandas, NumPy, SciPy** | Không dùng ML frameworks cho core engine |
| Testing | **Pytest + httpx** | Unit test engine + API integration test |
| **Frontend** | | |
| Framework | **Vue 3 + TypeScript** | Composition API, `<script setup>` |
| Router | **Vue Router 5** | SPA routing + auth guards |
| State | **Pinia 3** | Store management |
| Build | **Vite 8** | Dev server port 5173 |
| CSS | **Tailwind CSS v4** | Utility-first + custom theme |
| HTTP Client | **Axios** | Gọi backend API |
| Charts | **Chart.js + vue-chartjs** | Doughnut, Line, Bar charts |
| Icons | **Lucide Vue Next** | 200+ icons |
| Font | **Be Vietnam Pro** | Font tiếng Việt chuyên dụng |

---

## Cấu trúc thư mục

```
Aegis_AI/
├── AGENTS.md                          # Quy chuẩn team
├── README.md                          # File này
├── api_contract.md                    # API contract cho Frontend
├── .gitignore
│
├── backend/                           # ── Python FastAPI ──
│   ├── main.py                        # FastAPI entry point
│   ├── requirements.txt
│   ├── config.yaml                    # Thresholds & constants
│   │
│   ├── api/                           # API layer (thin adapter)
│   │   ├── schemas.py                 # Pydantic response models
│   │   └── routes/
│   │       ├── students.py            # GET /api/students, /api/students/{id}
│   │       ├── overview.py            # GET /api/overview/stats
│   │       └── feedback.py            # POST /api/feedback
│   │
│   ├── src/                           # Engine (core logic)
│   │   ├── config.py                  # Config loader
│   │   ├── exceptions.py              # Custom exceptions
│   │   ├── models/                    # Shared data classes
│   │   ├── input/                     # ① Data Input & Validation
│   │   ├── normalize/                 # ② Per-Course Normalization
│   │   ├── merge/                     # ③ Cross-Course Merge
│   │   ├── baseline/                  # ④ Baseline Engine
│   │   ├── detection/                 # ⑤ Detection Engine
│   │   └── alert/                     # ⑥ Alert Management
│   │
│   └── data/
│       └── sample/                    # Sample CSV cho demo
│
├── frontend/                          # ── Vue 3 + TypeScript ──
│   ├── package.json
│   ├── vite.config.ts
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.ts
│   │   ├── router/index.ts            # Routes + auth guards
│   │   │
│   │   ├── stores/                    # Pinia stores
│   │   │   ├── authStore.ts           # Login / Register / Logout
│   │   │   ├── overviewStore.ts       # Dashboard stats
│   │   │   ├── studentStore.ts        # Student list + detail
│   │   │   └── feedbackStore.ts       # Teacher feedback
│   │   │
│   │   ├── views/                     # Page components
│   │   │   ├── LoginView.vue
│   │   │   ├── RegisterView.vue
│   │   │   ├── DashboardView.vue
│   │   │   ├── StudentListView.vue
│   │   │   ├── StudentDetailView.vue
│   │   │   └── NotFoundView.vue
│   │   │
│   │   ├── components/
│   │   │   ├── layout/                # AppSidebar, AppHeader, DashboardLayout
│   │   │   ├── dashboard/             # Charts + stats + priority list
│   │   │   ├── students/              # Table + card + filters
│   │   │   ├── student-detail/        # Hero + signals + timeline + history
│   │   │   ├── feedback/              # Action form
│   │   │   └── ui/                    # 10 reusable primitives
│   │   │
│   │   ├── composables/               # useAlertLevel, useTheme, useDebounce
│   │   ├── services/                  # api.ts + mock.ts (48 HS)
│   │   ├── types/index.ts             # TypeScript interfaces
│   │   └── utils/                     # constants + format
│   │
│   └── ...
│
├── .agents/skills/                    # Skills cho AI assistant
│   ├── frontend-vue/
│   ├── frontend-ui-engineering/
│   ├── backend-fastapi/
│   └── ...
│
└── docs/
    └── ethical_guidelines.md
```

---

## API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/health` | Health check |
| GET | `/api/overview/stats` | Thống kê tổng quan |
| GET | `/api/students` | Danh sách HS + trạng thái |
| GET | `/api/students/{id}` | Chi tiết 1 HS |
| POST | `/api/feedback` | GV ghi nhận phản hồi |
| GET | `/api/feedback/{id}` | Lịch sử feedback 1 HS |

---

## Frontend Features

### Trang Đăng nhập / Đăng ký
- Form đăng nhập / đăng ký với validation
- Auth state lưu localStorage
- Route guards: chưa login → redirect `/login`

### Trang Dashboard (Tổng quan)
- **6 Summary Cards** với icon, màu sắc, click để lọc
- **Alert Distribution Chart** (Donut): phân bố HS theo mức
- **Trend Chart** (Line): xu hướng 7 tuần theo từng mức
- **Signal Stats**: thống kê tín hiệu phổ biến nhất
- **Major Distribution** (Bar): phân bố theo ngành
- **Priority Students**: danh sách HS cần ưu tiên
- **Recent Changes Table**: thay đổi gần đây
- **Warning Banner**: cảnh báo cố định khi có HS cần theo dõi
- **Notification Dropdown**: click chuông hiện danh sách HS cảnh báo

### Trang Danh sách Học sinh
- Data Table (desktop) + Card layout (tablet/mobile)
- STT (số thứ tự)
- Tìm kiếm theo tên/MSSV
- Filter theo Alert Level, Ngành
- Sort theo thời gian cập nhật

### Trang Chi tiết Học sinh
- Hero Card: thông tin tổng quan
- 3 Signal Cards: Điểm học tập, Điểm danh, Nộp bài
- Timeline Chart: biểu đồ xu hướng theo tuần
- Alert History: lịch sử cảnh báo
- Action Form: giáo viên ghi nhận phản hồi

### Alert Levels

| Level | Màu | Label |
|-------|-----|-------|
| `stable` | 🟢 Xanh lá | Ổn định |
| `watch` | 🟡 Vàng | Theo dõi thay đổi |
| `review` | 🟠 Cam | Cần giáo viên xem xét |
| `improving` | 🔵 Xanh dương | Đang cải thiện |
| `insufficient_data` | ⬜ Xám | Chưa đủ dữ liệu |

### Reusable UI Components (10 components)

StatusBadge · SummaryCard · EmptyState · LoadingSkeleton · ToastNotification · Modal · PageTitle · SearchBar · NotificationDropdown · WarningBanner

---

## Frontend Scripts

```bash
cd frontend
npm run dev          # Dev server localhost:5173
npm run build        # Production build
npm run type-check   # TypeScript check
```

---

## Mock Data

Hiện tại frontend đang dùng mock data (48 học sinh, 3 ngành, 5 alert levels) để phát triển song song với backend.

Khi backend sẵn sàng, tắt mock trong stores:
```typescript
// stores/overviewStore.ts, studentStore.ts, feedbackStore.ts
const USE_MOCK = false  // Chuyển từ true sang false
```

---

## Git Workflow

### Branch Strategy
```
main                    ← Chỉ merge từ develop
├── develop             ← Branch tích hợp
│   ├── feat/be-*       ← Backend feature
│   ├── feat/fe-*       ← Frontend feature
│   ├── fix/be-*        ← Backend fix
│   └── fix/fe-*        ← Frontend fix
```

### Commit Message
```
feat(be/baseline): implement rolling median + MAD with floor
feat(fe/dashboard): add trend chart and signal stats
fix(fe/badge): correct color mapping for improving state
test(be/fusion): add multi-signal fusion test cases
```

---

## Ràng buộc Đạo đức

### KHÔNG BAO GIỜ
1. Không phân tích cảm xúc
2. Không so sánh với đám đông để TẠO cảnh báo
3. Không gắn nhãn kết quả ("sẽ bỏ học", "nguy hiểm")
4. Không tự động kỷ luật
5. API KHÔNG trả z-score cho frontend

### LUÔN LUÔN
1. Thiếu dữ liệu → nói thiếu ("Chưa đủ dữ liệu")
2. Mỗi cảnh báo phải tự giải thích bằng tiếng Việt
3. Giáo viên quyết định cuối cùng

---

## Team Workflow

Đọc [AGENTS.md](./AGENTS.md) trước khi code.
