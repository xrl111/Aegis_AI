# Aegis AI — Hệ thống Cảnh báo Sớm Học sinh Có Nguy cơ Bỏ học

> Rule-based Early Warning System using Individual Baselines
> FastAPI Backend + Vue 3 Frontend

## Mô tả

Hệ thống phát hiện sớm học sinh có nguy cơ bỏ học dựa trên 3 tín hiệu phi xâm lấn:
1. **Biến động điểm** — so với baseline cá nhân
2. **Điểm danh** — pattern vắng gần đây
3. **Hành vi nộp bài** — nộp trễ / không nộp

Hệ thống **KHÔNG** phân loại, **KHÔNG** gắn nhãn, **KHÔNG** so với đám đông.

## Cấu trúc thư mục

```
Aegis_AI/
├── AGENTS.md                          # Quy chuẩn team
├── README.md                          # File này
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
│   ├── tests/                         # Pytest test suite
│   │   ├── fixtures/                  # Synthetic test data
│   │   └── ...
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
│   │   ├── router/                    # Vue Router
│   │   ├── stores/                    # Pinia stores
│   │   ├── views/                     # Page components
│   │   │   ├── OverviewView.vue       # Tổng quan HS
│   │   │   ├── StudentDetailView.vue  # Chi tiết 1 HS
│   │   │   └── FeedbackView.vue       # GV phản hồi
│   │   ├── components/                # Reusable components
│   │   │   ├── StatusBadge.vue
│   │   │   ├── AlertCard.vue
│   │   │   └── TimelineChart.vue
│   │   ├── types/                     # TypeScript interfaces
│   │   └── services/                  # API client
│   └── ...
│
├── .agents/                           # Skills cho AI assistant
│   └── skills/
│       ├── backend-fastapi/
│       │   └── SKILL.md
│       └── frontend-vue/
│           └── SKILL.md
│
└── docs/
    ├── architecture.md
    └── ethical_guidelines.md
```

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

## API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|--------|
| GET | `/api/health` | Health check |
| GET | `/api/students` | Danh sách HS + trạng thái |
| GET | `/api/students/{id}` | Chi tiết 1 HS |
| GET | `/api/overview/stats` | Thống kê tổng quan |
| POST | `/api/feedback` | GV ghi nhận phản hồi |
| GET | `/api/feedback/{id}` | Lịch sử feedback 1 HS |

## Team Workflow

Đọc [AGENTS.md](./AGENTS.md) trước khi code. Đặc biệt:
- Branch: `feat/be-<module>` hoặc `feat/fe-<component>` → `develop` → `main`
- Commit: `feat(be/baseline): ...` hoặc `feat(fe/overview): ...`
- Ràng buộc đạo đức: Mục 5 trong AGENTS.md — **KHÔNG ĐƯỢC VI PHẠM**
