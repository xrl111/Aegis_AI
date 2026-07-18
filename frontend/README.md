# Aegis AI — Frontend

> Giao diện Admin Dashboard cho Hệ thống Cảnh báo Sớm Học sinh
> Vue 3 + Composition API + TypeScript + Vite + Pinia + Tailwind CSS v4

---

## Tổng quan

Frontend là SPA Dashboard giúp giáo viên theo dõi tình hình học tập của học sinh. Hệ thống hiển thị cảnh báo dựa trên 3 tín hiệu phi xâm lấn: biến động điểm số, điểm danh, và hành vi nộp bài.

**Triết lý:** AI chỉ hỗ trợ phát hiện sớm — giáo viên đưa ra quyết định cuối cùng.

---

## Cài đặt

```bash
cd frontend
npm install
npm run dev
```

- Dev server: `http://localhost:5173`
- Backend API: `http://localhost:8000` (proxy tự động qua Vite)

### Tài khoản demo

| Email | Mật khẩu |
|-------|-----------|
| `admin@aegis.ai` | `123456` |
| `giao@aegis.ai` | `123456` |

---

## Tech Stack

| Layer | Công nghệ |
|-------|-----------|
| Framework | Vue 3 + TypeScript + Composition API (`<script setup>`) |
| Router | Vue Router 5 |
| State | Pinia 3 |
| Build | Vite 8 |
| CSS | Tailwind CSS v4 |
| HTTP | Axios |
| Charts | Chart.js + vue-chartjs |
| Icons | Lucide Vue Next |
| Font | Be Vietnam Pro + Inter |

---

## Cấu trúc thư mục

```
frontend/src/
├── App.vue                              # Root component
├── main.ts                              # Bootstrap + plugins
│
├── router/
│   └── index.ts                         # Route definitions + auth guards
│
├── stores/                              # Pinia stores
│   ├── authStore.ts                     # Đăng nhập / Đăng ký / Logout
│   ├── overviewStore.ts                 # Dashboard stats + recent changes
│   ├── studentStore.ts                  # Student list + detail + filters
│   └── feedbackStore.ts                 # Teacher feedback submission
│
├── views/                               # Page-level components
│   ├── LoginView.vue                    # Đăng nhập
│   ├── RegisterView.vue                 # Đăng ký
│   ├── DashboardView.vue                # Trang Tổng quan
│   ├── StudentListView.vue              # Danh sách học sinh
│   ├── StudentDetailView.vue            # Chi tiết 1 học sinh
│   └── NotFoundView.vue                 # Trang 404
│
├── components/
│   ├── layout/                          # Layout components
│   │   ├── AppSidebar.vue               # Sidebar navigation
│   │   ├── AppHeader.vue                # Header bar + user info
│   │   └── DashboardLayout.vue          # Layout wrapper
│   │
│   ├── dashboard/                       # Dashboard page components
│   │   ├── AlertDistributionChart.vue   # Donut chart phân bố cảnh báo
│   │   ├── RecentChangesTable.vue       # Bảng thay đổi gần đây
│   │   ├── TrendChart.vue               # Line chart xu hướng theo tuần
│   │   ├── MajorDistributionChart.vue   # Bar chart phân bố theo ngành
│   │   ├── SignalStats.vue              # Thống kê tín hiệu phổ biến
│   │   └── PriorityStudents.vue         # Danh sách HS cần ưu tiên
│   │
│   ├── students/                        # Student list components
│   │   ├── StudentTable.vue             # Data table (desktop)
│   │   ├── StudentCard.vue              # Card layout (tablet/mobile)
│   │   └── StudentFilters.vue           # Search + filter toolbar
│   │
│   ├── student-detail/                  # Student detail components
│   │   ├── HeroCard.vue                 # Hero section thông tin HS
│   │   ├── SignalCard.vue               # Card hiển thị 1 tín hiệu
│   │   ├── SignalSection.vue            # Container 3 SignalCard
│   │   ├── TimelineChart.vue            # Multi-line Chart.js
│   │   └── AlertHistoryTimeline.vue     # Lịch sử cảnh báo
│   │
│   ├── feedback/
│   │   └── ActionForm.vue               # Form phản hồi giáo viên
│   │
│   └── ui/                              # Reusable UI primitives
│       ├── StatusBadge.vue              # Badge màu theo alert level
│       ├── SummaryCard.vue              # Card thống kê tổng quan
│       ├── EmptyState.vue               # Trạng thái rỗng
│       ├── LoadingSkeleton.vue          # Skeleton loading
│       ├── ToastNotification.vue        # Toast notification
│       ├── Modal.vue                    # Dialog modal
│       ├── PageTitle.vue                # Tiêu đề trang
│       ├── SearchBar.vue                # Ô tìm kiếm
│       ├── NotificationDropdown.vue     # Dropdown thông báo
│       └── WarningBanner.vue            # Banner cảnh báo cố định
│
├── composables/                         # Vue composables
│   ├── useAlertLevel.ts                 # Mapping alert_level → color/label
│   ├── useTheme.ts                      # Dark/Light mode toggle
│   └── useDebounce.ts                   # Debounce cho search input
│
├── services/
│   ├── api.ts                           # Axios client + API calls
│   └── mock.ts                          # Mock data (48 học sinh)
│
├── types/
│   └── index.ts                         # TypeScript interfaces
│
└── utils/
    ├── constants.ts                     # Alert colors, labels, icons
    └── format.ts                        # Date formatting, initials, avatar
```

---

## Trang chính

### Đăng nhập / Đăng ký
- Form đăng nhập với email + mật khẩu
- Form đăng ký với họ tên, email, mật khẩu
- Auth state lưu localStorage
- Route guards: chưa đăng nhập → redirect `/login`

### Dashboard (Tổng quan)
- 6 Summary Cards: Tổng HS, Ổn định, Theo dõi, Cần xem xét, Đang cải thiện, Chưa đủ dữ liệu
- Alert Distribution Chart (Donut): Phân bố HS theo mức cảnh báo
- Trend Chart (Line): Xu hướng 7 tuần theo từng mức
- Signal Stats: Thống kê tín hiệu được kích hoạt phổ biến nhất
- Major Distribution (Bar): Phân bố HS theo ngành
- Priority Students: Danh sách HS cần ưu tiên
- Recent Changes Table: Thay đổi gần đây
- Warning Banner: Cảnh báo cố định khi có HS cần theo dõi
- Notification Dropdown: Click chuông hiện danh sách HS cảnh báo

### Danh sách học sinh
- Data Table (desktop) + Card layout (tablet/mobile)
- STT (số thứ tự)
- Tìm kiếm theo tên/MSSV
- Filter theo Alert Level, Ngành
- Sort theo thời gian cập nhật
- Click → chuyển trang chi tiết

### Chi tiết học sinh
- Hero Card: Thông tin tổng quan
- 3 Signal Cards: Điểm học tập, Điểm danh, Nộp bài (chỉ giải thích, không hiển thị số liệu thô)
- Timeline Chart: Biểu đồ xu hướng theo tuần
- Alert History: Lịch sử cảnh báo
- Action Form: Giáo viên ghi nhận phản hồi

---

## Alert Levels

| Level | Màu | Label | Icon |
|-------|-----|-------|------|
| `stable` | 🟢 Xanh lá | Ổn định | CheckCircle |
| `watch` | 🟡 Vàng | Theo dõi thay đổi | Eye |
| `review` | 🟠 Cam | Cần giáo viên xem xét | AlertTriangle |
| `improving` | 🔵 Xanh dương | Đang cải thiện | TrendingUp |
| `insufficient_data` | ⬜ Xám | Chưa đủ dữ liệu | HelpCircle |

---

## API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/overview/stats` | Thống kê tổng quan |
| GET | `/api/students` | Danh sách HS |
| GET | `/api/students/:id` | Chi tiết 1 HS |
| POST | `/api/feedback` | GV ghi nhận phản hồi |
| GET | `/api/feedback/:id` | Lịch sử feedback |

Hiện tại đang dùng mock data. Khi backend sẵn sàng, tắt `USE_MOCK = true` trong stores.

---

## Scripts

```bash
npm run dev          # Dev server
npm run build        # Production build
npm run type-check   # TypeScript check
```

---

## Quy tắc quan trọng

- **KHÔNG** hiển thị z-score hay thuật toán thống kê
- **KHÔNG** dùng từ ngữ "dự đoán bỏ học", "nguy hiểm", "classification"
- Mọi cảnh báo phải có **giải thích bằng tiếng Việt** tự nhiên
- Giáo viên là người đưa ra quyết định cuối cùng
- Ngôn ngữ giao diện: **Tiếng Việt**
