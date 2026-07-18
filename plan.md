# Aegis AI — Frontend Implementation Plan

> Giao diện Admin Dashboard cho Hệ thống Cảnh báo Sớm Học sinh Có Nguy cơ Bỏ học
> Vue 3 + Composition API + Vite + Pinia + Tailwind CSS + Chart.js

---

## 1. Hiện trạng dự án

### 1.1 Đã hoàn thành

| Layer | Trạng thái | Chi tiết |
|-------|-----------|----------|
| **Backend API** | Skeleton | FastAPI + CORS configured, routes defined (501 Not Implemented) |
| **API Schemas** | Hoàn thành | Pydantic models trong `backend/api/schemas.py` — là contract cho frontend |
| **Frontend Scaffold** | Default Vue template | Chưa có component/dashboard nào — cần rebuild toàn bộ |
| **Config** | Có | `backend/config.yaml` (thresholds), `vite.config.ts`, `tsconfig` |
| **Skills/Rules** | Hoàn thành | `AGENTS.md`, Vue skill, UI engineering skill |

### 1.2 Cần xây dựng trong plan này

- Xóa toàn bộ default template (HelloWorld, TheWelcome, HomeView, AboutView, counter store)
- Triển khai Layout System (Sidebar + Header + Content Area)
- 3 trang chính: Dashboard, Danh sách Học sinh, Chi tiết Học sinh
- Hệ thống component tái sử dụng (17 components)
- Pinia stores kết nối backend API
- TypeScript types mirror backend schemas
- Tailwind CSS config với design tokens
- Dark/Light mode toggle
- Responsive layout (Desktop + Tablet)

---

## 2. Kiến trúc Frontend

### 2.1 Cấu trúc thư mục mục tiêu

```
frontend/src/
├── App.vue                              # Root — Dashboard layout wrapper
├── main.ts                              # Bootstrap + plugin registration
├── assets/
│   ├── main.css                         # Tailwind directives + global styles
│   └── styles/
│       └── variables.css                # CSS custom properties (theme tokens)
│
├── router/
│   └── index.ts                         # Route definitions
│
├── stores/
│   ├── overviewStore.ts                 # Dashboard stats + recent changes
│   ├── studentStore.ts                  # Student list + detail + filters
│   └── feedbackStore.ts                 # Teacher feedback submission
│
├── views/
│   ├── DashboardView.vue                # Trang Dashboard (Overview)
│   ├── StudentListView.vue              # Danh sách học sinh
│   └── StudentDetailView.vue            # Chi tiết 1 học sinh
│
├── components/
│   ├── layout/
│   │   ├── AppSidebar.vue               # Sidebar navigation
│   │   ├── AppHeader.vue                # Top header bar
│   │   └── DashboardLayout.vue          # Layout wrapper (Sidebar + Header + slot)
│   │
│   ├── dashboard/
│   │   ├── SummaryCard.vue              # Card thống kê tổng quan
│   │   ├── AlertDistributionChart.vue   # Donut chart phân bố cảnh báo
│   │   └── RecentChangesTable.vue       # Bảng thay đổi gần đây
│   │
│   ├── students/
│   │   ├── StudentTable.vue             # Data table danh sách HS
│   │   ├── StudentCard.vue              # Card layout cho tablet
│   │   └── StudentFilters.vue           # Search + filter toolbar
│   │
│   ├── student-detail/
│   │   ├── HeroCard.vue                 # Hero section chi tiết HS
│   │   ├── SignalCard.vue               # Card hiển thị 1 tín hiệu
│   │   ├── SignalSection.vue            # Container 3 SignalCard
│   │   ├── TimelineChart.vue            # Multi-line Chart.js
│   │   └── AlertHistoryTimeline.vue     # Lịch sử cảnh báo dạng timeline
│   │
│   ├── feedback/
│   │   └── ActionForm.vue               # Form phản hồi giáo viên
│   │
│   └── ui/
│       ├── StatusBadge.vue              # Badge màu theo alert_level
│       ├── EmptyState.vue               # Trạng thái rỗng
│       ├── LoadingSkeleton.vue          # Skeleton loading
│       ├── ToastNotification.vue        # Thông báo toast
│       ├── Modal.vue                    # Dialog modal
│       ├── PageTitle.vue                # Tiêu đề trang
│       └── SearchBar.vue                # Ô tìm kiếm
│
├── composables/
│   ├── useAlertLevel.ts                 # Mapping alert_level → color/label/icon
│   ├── useTheme.ts                      # Dark/Light mode toggle
│   └── useDebounce.ts                   # Debounce cho search input
│
├── services/
│   └── api.ts                           # Axios instance + interceptors
│
├── types/
│   └── index.ts                         # TypeScript interfaces (mirror backend schemas)
│
└── utils/
    ├── format.ts                        # Date formatting, number formatting
    └── constants.ts                     # Alert colors, labels, icons mapping
```

### 2.2 Flow dữ liệu

```
[Backend API] → [services/api.ts] → [Pinia Store] → [View/Page Component] → [Child Components]
```

**Quy tắc vàng:**
- Component KHÔNG gọi API trực tiếp — luôn qua Pinia Store
- Store KHÔNG render UI — chỉ quản lý state + business logic
- View Component orchestrate: gọi store, render child components
- Child components nhận data qua props, emit events lên trên

### 2.3 Routing

```typescript
// router/index.ts
const routes = [
  {
    path: '/',
    component: DashboardLayout,        // Layout wrapper
    children: [
      {
        path: '',
        name: 'dashboard',
        component: DashboardView,
        meta: { title: 'Tổng quan' },
      },
      {
        path: 'students',
        name: 'student-list',
        component: StudentListView,
        meta: { title: 'Danh sách học sinh' },
      },
      {
        path: 'students/:id',
        name: 'student-detail',
        component: StudentDetailView,
        meta: { title: 'Chi tiết học sinh' },
      },
    ],
  },
]
```

**Navigation flow:**

```
Dashboard ──────────┬── Click card ──→ Student List (filter by level)
                    ├── Click row ────→ Student Detail
                    │
Student List ───────┼── Click row ────→ Student Detail
                    ├── Search/Filter ─→ Filtered list
                    │
Student Detail ─────┼── "Quay lại" ──→ Student List
                    ├── Submit feedback → Toast success
                    └── Sidebar nav ──→ Dashboard / Student List
```

---

## 3. API Contract (Frontend ← Backend)

### 3.1 Endpoints

| Method | Endpoint | Response Type | Mô tả |
|--------|----------|--------------|-------|
| GET | `/api/health` | `{ status: string }` | Health check |
| GET | `/api/overview/stats` | `OverviewStats` | Thống kê tổng quan |
| GET | `/api/students` | `StudentSummary[]` | Danh sách HS + trạng thái |
| GET | `/api/students/:id` | `StudentDetail` | Chi tiết 1 HS |
| POST | `/api/feedback` | `FeedbackResponse` | GV ghi nhận phản hồi |
| GET | `/api/feedback/:id` | `FeedbackEntry[]` | Lịch sử feedback 1 HS |

### 3.2 TypeScript Types

```typescript
// types/index.ts — Mirror hoàn toàn backend/api/schemas.py

export type AlertLevel =
  | 'insufficient_data'
  | 'stable'
  | 'watch'
  | 'review'
  | 'improving'

export type SignalType = 'grade' | 'attendance' | 'submission'

export type DataSufficiency = 'sufficient' | 'partial' | 'insufficient'

export type ActionTaken = 'contacted' | 'meeting' | 'noted' | 'dismissed'

// --- API Response Types ---

export interface OverviewStats {
  total_students: number
  stable_count: number
  watch_count: number
  review_count: number
  insufficient_count: number
  improving_count: number
}

export interface StudentSummary {
  student_id: string
  student_name: string
  major: string
  alert_level: AlertLevel
  headline: string
  triggered_signal_count: number
  updated_at: string | null
}

export interface SignalOut {
  signal_type: SignalType
  is_triggered: boolean
  data_sufficiency: DataSufficiency
  explanation: string
}

export interface TimelinePoint {
  week: string
  grade_value: number | null
  attendance_value: number | null
  submission_value: number | null
}

export interface AlertHistoryItem {
  date: string
  level: AlertLevel
  headline: string
  details: string[]
}

export interface StudentDetail {
  student_id: string
  student_name: string
  major: string
  alert_level: AlertLevel
  headline: string
  signals: SignalOut[]
  timeline: TimelinePoint[]
  alert_history: AlertHistoryItem[]
  is_seasonal_suppressed: boolean
}

export interface FeedbackRequest {
  student_id: string
  teacher_id: string
  action_taken: ActionTaken
  notes: string
}

export interface FeedbackResponse {
  success: boolean
  message: string
}
```

---

## 4. Thiết kế từng trang

### 4.1 Trang Dashboard (`DashboardView.vue`)

**Layout tổng thể:**

```
┌─────────────────────────────────────────────────────────┐
│  [Sidebar]  │  Header: "Tổng quan"        [🔔] [🌙]   │
│             │────────────────────────────────────────── │
│  Dashboard  │                                           │
│  Học sinh   │  ┌──────┐ ┌──────┐ ┌──────┐             │
│             │  │ Tổng │ │ Ổn   │ │Theo  │             │
│             │  │  HS  │ │ định │ │dõi   │             │
│             │  └──────┘ └──────┘ └──────┘             │
│             │  ┌──────┐ ┌──────┐ ┌──────┐             │
│             │  │Cần   │ │Đang  │ │Chưa  │             │
│             │  │xem   │ │cải   │ │đủ DL │             │
│             │  │xét   │ │thiện │ │      │             │
│             │  └──────┘ └──────┘ └──────┘             │
│             │                                           │
│             │  ┌─────────────────┐ ┌─────────────────┐ │
│             │  │   Donut Chart   │ │  Recent Changes │ │
│             │  │   Phân bố HS    │ │  Table          │ │
│             │  │   theo Level    │ │                 │ │
│             │  └─────────────────┘ └─────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**Summary Cards (6 cards):**

| Card | Icon (Lucide) | Màu | Dữ liệu |
|------|--------------|-----|----------|
| Tổng số học sinh | Users | Gray-700 | `total_students` |
| Ổn định | CheckCircle | Green-500 | `stable_count` |
| Theo dõi thay đổi | Eye | Yellow-500 | `watch_count` |
| Cần giáo viên xem xét | AlertTriangle | Orange-500 | `review_count` |
| Đang cải thiện | TrendingUp | Blue-500 | `improving_count` |
| Chưa đủ dữ liệu | HelpCircle | Gray-400 | `insufficient_count` |

**Interaction:**
- Hover card: translateY(-2px) + shadow tăng nhẹ
- Click card "Cần xem xét" → navigate to `/students?level=review`
- Click card "Theo dõi" → navigate to `/students?level=watch`

**Donut Chart:**
- Chart.js Doughnut
- 5 segment màu theo AlertLevel
- Center text hiển thị tổng số HS
- Legend bên phải
- Tooltip khi hover

**Recent Changes Table:**
- Hiển thị 10 thay đổi gần nhất (sort by `updated_at` desc)
- Cột: Tên HS, Ngành, Alert Badge, Headline, Signals count, Thời gian, Button "Xem chi tiết"
- Click row → navigate to `/students/:id`

### 4.2 Trang Danh sách Học sinh (`StudentListView.vue`)

**Layout:**

```
┌─────────────────────────────────────────────────────────┐
│  [Sidebar]  │  Header: "Học sinh"                       │
│             │────────────────────────────────────────── │
│             │  🔍 Tìm kiếm    [Level ▼] [Ngành ▼] [↕ Sắp xếp] │
│             │────────────────────────────────────────── │
│             │  ┌─────────────────────────────────────┐ │
│             │  │  Avatar │ Tên │ MSSV │ Ngành │ Badge │ │
│             │  │  ───────┼──────┼──────┼──────┼───── │ │
│             │  │  HS 1   │ ...  │ ...  │ ...  │ 🟢   │ │
│             │  │  HS 2   │ ...  │ ...  │ ...  │ 🟡   │ │
│             │  │  HS 3   │ ...  │ ...  │ ...  │ 🟠   │ │
│             │  └─────────────────────────────────────┘ │
│             │           (Desktop: Table)                │
│             │                                           │
│             │  ┌──────┐ ┌──────┐                       │
│             │  │Card 1│ │Card 2│                       │
│             │  └──────┘ └──────┘                       │
│             │           (Tablet: Card Grid)             │
└─────────────────────────────────────────────────────────┘
```

**Toolbar:**
- SearchBar: Tìm kiếm theo tên (debounce 300ms)
- FilterDropdown: Alert Level (multi-select)
- FilterDropdown: Ngành (single-select, derive từ data)
- SortButton: Theo thời gian cập nhật (asc/desc)

**Desktop Table:**
| Cột | Chi tiết | Width |
|-----|---------|-------|
| Avatar | Initials circle + màu random | 48px |
| Họ tên | Text, bold | auto |
| MSSV | Mono font, gray | 120px |
| Ngành | Text | auto |
| Status | StatusBadge component | 160px |
| Headline | Text, truncate 1 dòng | auto |
| Signals | Badge count | 80px |
| Cập nhật | Relative time (VD: "2 giờ trước") | 120px |
| Thao tác | Button "Xem chi tiết" | 120px |

**Tablet Card Grid:**
- 2 cột, mỗi card hiển thị: Avatar + Tên + MSSV + Badge + Headline + Button
- Responsive breakpoint: `md:` (768px)

**Empty State:**
- Khi không có kết quả: icon + "Không tìm thấy học sinh" + description
- Khi loading: LoadingSkeleton (10 rows shimmer)

### 4.3 Trang Chi tiết Học sinh (`StudentDetailView.vue`)

Đây là trang quan trọng nhất. Layout:

```
┌─────────────────────────────────────────────────────────┐
│  [Sidebar]  │  Header: "Chi tiết học sinh"  [← Quay lại]│
│             │────────────────────────────────────────── │
│             │                                           │
│             │  ┌─────────────────────────────────────┐ │
│             │  │  🟢  Nguyễn Văn A  │ 2200001       │ │
│             │  │      Khoa CNTT    │ Cần theo dõi   │ │
│             │  │      "Điểm quiz gần đây giảm so    │ │
│             │  │       với mức bình thường"          │ │
│             │  └─────────────────────────────────────┘ │
│             │           HERO CARD                      │
│             │                                           │
│             │  ── Các tín hiệu ──                      │
│             │  ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│             │  │ 📊 Điểm  │ │ 📋 Điểm  │ │ 📝 Nộp  │ │
│             │  │ học tập  │ │  danh    │ │  bài     │ │
│             │  │          │ │          │ │          │ │
│             │  │ Stable   │ │ Watch    │ │ Stable   │ │
│             │  │          │ │          │ │          │ │
│             │  │"Điểm     │ │"Vắng 2   │ │"Nộp bài │ │
│             │  │ gần đây  │ │ buổi     │ │ đúng     │ │
│             │  │ ổn định" │ │ liên     │ │ hạn"     │ │
│             │  │          │ │ tiếp"    │ │          │ │
│             │  └──────────┘ └──────────┘ └──────────┘ │
│             │         SIGNAL CARDS                     │
│             │                                           │
│             │  ── Biểu đồ theo thời gian ──           │
│             │  ┌─────────────────────────────────────┐ │
│             │  │  ╱╲     ╱╲                          │ │
│             │  │ ╱  ╲___╱  ╲___   ── Grade           │ │
│             │  │╱            ╲   ── Attendance       │ │
│             │  │───────────────── ── Submission      │ │
│             │  │  W1  W2  W3  W4  W5  W6            │ │
│             │  └─────────────────────────────────────┘ │
│             │         TIMELINE CHART                   │
│             │                                           │
│             │  ── Lịch sử cảnh báo ──                  │
│             │  ┌─────────────────────────────────────┐ │
│             │  │ ● 15/03/2026 — 🟡 Theo dõi          │ │
│             │  │   "Điểm quiz giảm"                  │ │
│             │  │   • Chi tiết 1                      │ │
│             │  │   • Chi tiết 2                      │ │
│             │  │                                     │ │
│             │  │ ● 10/03/2026 — 🟢 Ổn định          │ │
│             │  │   "Trở lại bình thường"             │ │
│             │  └─────────────────────────────────────┘ │
│             │         ALERT HISTORY                    │
│             │                                           │
│             │  ── Ghi nhận của giáo viên ──           │
│             │  ┌─────────────────────────────────────┐ │
│             │  │ (●) Đã liên hệ  (○) Đã gặp        │ │
│             │  │ (○) Đã ghi chú  (○) Không cần XL  │ │
│             │  │                                     │ │
│             │  │ ┌───────────────────────────────┐  │ │
│             │  │ │ Nhập ghi chú...               │  │ │
│             │  │ └───────────────────────────────┘  │ │
│             │  │                                     │ │
│             │  │ [  Lưu phản hồi  ]                  │ │
│             │  └─────────────────────────────────────┘ │
│             │         ACTION FORM                      │
└─────────────────────────────────────────────────────────┘
```

**Hero Card:**
- Avatar (initials circle lớn, 64px)
- Họ tên (text-xl, font-semibold)
- MSSV (text-sm, gray)
- Ngành (text-sm)
- AlertBadge (StatusBadge lớn)
- Headline (text-sm, italic, max-w-lg)

**Signal Cards (3 cards):**

| Signal | Icon (Lucide) | Khi triggered | Khi stable |
|--------|--------------|---------------|------------|
| Điểm học tập | BookOpen | Warning color | Green color |
| Điểm danh | ClipboardList | Warning color | Green color |
| Nộp bài | FileText | Warning color | Green color |

Mỗi card:
- Header: Icon + Tên tín hiệu
- Status: Badge nhỏ (Stable/Watch/Review/...)
- Explanation: Text paragraph — **KHÔNG có z-score, KHÔNG có số liệu thô**
- Border left: màu theo status
- Nếu `data_sufficiency === 'insufficient'`: hiển thị "Chưa đủ dữ liệu" thay vì explanation

**Timeline Chart (Chart.js):**
- Type: `line`
- 3 datasets: Grade, Attendance, Submission
- Colors:
  - Grade: `#3b82f6` (blue-500)
  - Attendance: `#22c55e` (green-500)
  - Submission: `#f59e0b` (amber-500)
- Y-axis: 0 → 1 (normalized)
- X-axis: Tuần (W1, W2, W3, ...)
- Tooltip: hiển thị giá trị khi hover
- Legend: hiển thị tên 3 đường
- Tension: 0.3 (smooth curves)
- Point radius: 3, hover radius: 6
- Null values: gap (không nối qua null)

**Alert History:**
- Dạng vertical timeline
- Mỗi item:Dot marker màu level + Ngày + Level Badge + Headline + Danh sách chi tiết (bullet list)
- Mới nhất ở trên

**Action Form:**
- Radio group 4 options: Đã liên hệ, Đã gặp, Đã ghi chú, Không cần xử lý
- Textarea: placeholder "Nhập ghi chú..."
- Button: "Lưu phản hồi" — primary color
- Loading state khi submit
- Success: ToastNotification hiện 3s rồi tự mất
- Error: ToastNotification màu đỏ

---

## 5. Design System

### 5.1 Alert Level Colors

```typescript
// utils/constants.ts
export const ALERT_CONFIG = {
  stable: {
    color: '#22c55e',           // green-500
    bg: '#f0fdf4',              // green-50
    bgDark: '#14532d',          // green-900 (dark mode)
    border: '#bbf7d0',          // green-200
    label: 'Ổn định',
    icon: 'CheckCircle',        // Lucide
  },
  watch: {
    color: '#eab308',           // yellow-500
    bg: '#fefce8',              // yellow-50
    bgDark: '#713f12',          // yellow-900
    border: '#fef08a',          // yellow-200
    label: 'Theo dõi thay đổi',
    icon: 'Eye',
  },
  review: {
    color: '#f97316',           // orange-500
    bg: '#fff7ed',              // orange-50
    bgDark: '#7c2d12',          // orange-900
    border: '#fed7aa',          // orange-200
    label: 'Cần giáo viên xem xét',
    icon: 'AlertTriangle',
  },
  improving: {
    color: '#3b82f6',           // blue-500
    bg: '#eff6ff',              // blue-50
    bgDark: '#1e3a5f',          // blue-900
    border: '#bfdbfe',          // blue-200
    label: 'Đang cải thiện',
    icon: 'TrendingUp',
  },
  insufficient_data: {
    color: '#9ca3af',           // gray-400
    bg: '#f9fafb',              // gray-50
    bgDark: '#374151',          // gray-700
    border: '#e5e7eb',          // gray-200
    label: 'Chưa đủ dữ liệu',
    icon: 'HelpCircle',
  },
} as const
```

### 5.2 Tailwind Custom Theme

```javascript
// tailwind.config.js (mới, cần tạo)
export default {
  content: ['./index.html', './src/**/*.{vue,ts}'],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      borderRadius: {
        'xl': '12px',
        '2xl': '16px',
      },
      boxShadow: {
        'card': '0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)',
        'card-hover': '0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04)',
      },
      colors: {
        // Semantic tokens
        surface: {
          DEFAULT: '#ffffff',
          secondary: '#f8fafc',
          dark: '#0f172a',
          'dark-secondary': '#1e293b',
        },
        border: {
          DEFAULT: '#e2e8f0',
          dark: '#334155',
        },
      },
      animation: {
        'fade-in': 'fadeIn 0.2s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'shimmer': 'shimmer 1.5s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
    },
  },
  plugins: [],
}
```

### 5.3 Typography

```
Font: Inter (Google Fonts, import trong index.html)
- Page title: text-2xl font-semibold tracking-tight
- Section title: text-lg font-semibold
- Card title: text-sm font-medium
- Body: text-sm text-gray-600
- Caption: text-xs text-gray-400
- Mono (MSSV): font-mono text-sm
```

### 5.4 Spacing & Layout

```
Sidebar width: 256px (Desktop), 0px + overlay (Tablet)
Header height: 64px
Content padding: 24px (Desktop), 16px (Tablet)
Card padding: 20px
Card gap: 16px
Table row height: 56px
Border radius: 12px (cards), 8px (buttons/inputs), 6px (badges)
```

### 5.5 Micro-animations

| Interaction | Animation |
|------------|-----------|
| Card hover | translateY(-2px) + shadow increase, 200ms ease |
| Button click | scale(0.98), 100ms |
| Page transition | fadeIn + slideUp, 300ms |
| Sidebar item active | Background slide, 200ms |
| Badge appear | fadeIn, 200ms |
| Toast enter | slideUp from bottom-right, 300ms |
| Toast exit | fadeOut, 200ms |
| Skeleton shimmer | Linear gradient sweep, 1.5s infinite |
| Chart load | Draw animation (Chart.js default) |
| Dark mode toggle | Color transition, 300ms |

---

## 6. Chi tiết Components

### 6.1 Layout Components

**DashboardLayout.vue**
- Flex container: Sidebar (fixed left) + Main area (flex-1)
- Main area: Header (fixed top) + Content (scrollable, padding-top: header height)
- Responsive: Sidebar ẩn trên tablet, toggle bằng hamburger menu

**AppSidebar.vue**
- Fixed left, full height, bg-white (light) / bg-slate-900 (dark)
- Top: Logo "Aegis AI" + tagline "Hệ thống Cảnh báo sớm"
- Nav items: Dashboard, Học sinh (dùng router-link)
- Active state: bg-blue-50, text-blue-600, border-left: 3px blue-500
- Bottom: Teacher info (small)
- Icons: Lucide — LayoutDashboard, Users

**AppHeader.vue**
- Fixed top, height: 64px
- Left: Page title (dynamic, từ router meta)
- Right: NotificationBell (badge count optional), ThemeToggle, TeacherAvatar

### 6.2 UI Reusable Components

**StatusBadge.vue**
```vue
<!-- Props -->
{ level: AlertLevel, size?: 'sm' | 'md' }

<!-- Render -->
<span :class="badgeClasses">
  <component :is="icon" class="w-3 h-3" />
  {{ label }}
</span>
```

**SummaryCard.vue**
```vue
<!-- Props -->
{
  title: string,
  value: number,
  icon: Component,          // Lucide icon component
  color: string,            // Tailwind color class
  trend?: 'up' | 'down',   // Optional trend indicator
}

<!-- Behavior -->
- Hover: shadow-card → shadow-card-hover
- Click (optional): emit('click')
- Transition: animate-fade-in on mount
```

**LoadingSkeleton.vue**
```vue
<!-- Props -->
{ type: 'card' | 'table-row' | 'chart' | 'text', count?: number }

<!-- Render -->
<div class="animate-shimmer bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 rounded-xl" />
```

**EmptyState.vue**
```vue
<!-- Props -->
{
  icon: Component,
  title: string,
  description: string,
  actionLabel?: string,
}

<!-- Behavior -->
emit('action') khi click button
```

**ToastNotification.vue**
```vue
<!-- Props (from store) -->
{
  id: string,
  type: 'success' | 'error' | 'info',
  message: string,
  duration?: number,    // Default 3000ms
}

<!-- Behavior -->
- Auto-dismiss sau duration
- Position: bottom-right
- Animation: slideUp + fadeOut
```

**Modal.vue**
```vue
<!-- Props -->
{
  isOpen: boolean,
  title: string,
}

<!-- Events -->
emit('close')

<!-- Behavior -->
- Backdrop overlay (click to close)
- Escape key to close
- Focus trap
- Animation: fadeIn backdrop + scale-up content
```

### 6.3 Feature Components

**SignalCard.vue**
```vue
<!-- Props -->
{ signal: SignalOut }

<!-- Render -->
<div class="signal-card" :class="borderColorClass">
  <div class="flex items-center gap-3">
    <component :is="signalIcon" />
    <div>
      <h4>{{ signalName }}</h4>
      <StatusBadge :level="signalStatus" size="sm" />
    </div>
  </div>
  <div v-if="signal.data_sufficiency === 'insufficient'" class="text-gray-400 italic">
    Chưa đủ dữ liệu để đánh giá
  </div>
  <p v-else class="text-sm text-gray-600">
    {{ signal.explanation }}
  </p>
</div>
```

**TimelineChart.vue**
```vue
<!-- Props -->
{ timeline: TimelinePoint[] }

<!-- Behavior -->
- watch(timeline) → rebuild chart
- Destroy chart on unmount
- Responsive resize observer
- Dark mode: update grid/label colors
```

**ActionForm.vue**
```vue
<!-- Props -->
{ studentId: string }

<!-- State -->
- selectedAction: Ref<ActionTaken | null>
- notes: Ref<string>
- submitting: Ref<boolean>

<!-- Behavior -->
- Validate: action required, notes optional
- Call feedbackStore.submit()
- On success: emit('submitted'), show toast
- On error: show error toast
```

---

## 7. Pinia Stores

### 7.1 overviewStore.ts

```typescript
export const useOverviewStore = defineStore('overview', () => {
  // State
  const stats = ref<OverviewStats | null>(null)
  const recentChanges = ref<StudentSummary[]>([])
  const loading = ref(false)

  // Getters
  const reviewStudents = computed(() =>
    recentChanges.value.filter(s => s.alert_level === 'review')
  )

  // Actions
  async function fetchStats() { ... }
  async function fetchRecentChanges() { ... }

  return { stats, recentChanges, loading, reviewStudents, fetchStats, fetchRecentChanges }
})
```

### 7.2 studentStore.ts

```typescript
export const useStudentStore = defineStore('student', () => {
  // State
  const students = ref<StudentSummary[]>([])
  const currentStudent = ref<StudentDetail | null>(null)
  const loading = ref(false)
  const filters = ref({
    search: '',
    levels: [] as AlertLevel[],
    major: '',
    sort: 'desc' as 'asc' | 'desc',
  })

  // Getters
  const filteredStudents = computed(() => { ... })

  // Actions
  async function fetchAll() { ... }
  async function fetchDetail(id: string) { ... }

  return { students, currentStudent, loading, filters, filteredStudents, fetchAll, fetchDetail }
})
```

### 7.3 feedbackStore.ts

```typescript
export const useFeedbackStore = defineStore('feedback', () => {
  const submitting = ref(false)
  const lastResult = ref<FeedbackResponse | null>(null)

  async function submit(request: FeedbackRequest) { ... }
  async function fetchHistory(studentId: string) { ... }

  return { submitting, lastResult, submit, fetchHistory }
})
```

---

## 8. Dependencies cần cài đặt

### 8.1 npm packages (mới)

```bash
cd frontend

# Core (đã có)
# vue, pinia, vue-router

# UI & Icons
npm install lucide-vue-next          # Lucide icons
npm install chart.js                 # Chart.js
npm install vue-chartjs              # Vue wrapper cho Chart.js

# HTTP
npm install axios                    # Axios HTTP client

# CSS
npm install -D tailwindcss @tailwindcss/vite   # Tailwind CSS v4

# Utilities
npm install @vueuse/core             # VueUse composables (useDark, useToggle, etc.)

# Optional
npm install @headlessui/vue          # Accessible UI primitives (Radio, Dialog, etc.)
```

### 8.2 Google Fonts

Thêm vào `index.html`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### 8.3 Vite Config cập nhật

```typescript
// vite.config.ts — thêm proxy + Tailwind
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [vue(), vueDevTools(), tailwindcss()],
  resolve: { alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) } },
  server: {
    proxy: {
      '/api': { target: 'http://localhost:8000', changeOrigin: true },
    },
  },
})
```

---

## 9. Các hạn chế cần lưu ý

### 9.1 Backend chưa implement

Tất cả API endpoints hiện tại trả `501 Not Implemented`. Frontend cần:

- **Mock data** để phát triển UI song song với backend
- Tạo file `services/mock.ts` chứa mock data theo đúng TypeScript types
- Switch giữa mock và real API qua environment variable:

```typescript
// services/api.ts
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'

export async function fetchStudents(): Promise<StudentSummary[]> {
  if (USE_MOCK) return mockStudents
  const res = await api.get('/api/students')
  return res.data
}
```

### 9.2 Dark Mode

Dark mode là optional. Nếu implement:
- Dùng `@vueuse/core` `useDark()` + `useToggle()`
- Tailwind `darkMode: 'class'`
- Tất cả color tokens cần có dark variant
- Chart.js cần update colors khi switch

### 9.3 Responsive Breakpoints

| Breakpoint | Width | Behavior |
|-----------|-------|----------|
| Desktop | >= 1024px | Sidebar + full table |
| Tablet | 768px - 1023px | Collapsed sidebar (overlay) + card layout |
| Mobile | < 768px | Hidden sidebar (hamburger) + card layout |

### 9.4 i18n

Hiện tại chỉ cần tiếng Việt. Nếu cần multi-language trong tương lai, cấu trúc components đã sẵn sàng để extract strings.

---

## 10. Implementation Phases

### Phase 1: Foundation (Day 1)

**Mục tiêu:** Setup infrastructure, xóa default template

- [ ] Cài đặt dependencies (tailwindcss, axios, chart.js, vue-chartjs, lucide-vue-next, @vueuse/core)
- [ ] Config Tailwind CSS v4 (content, theme, darkMode)
- [ ] Config Vite proxy
- [ ] Tạo TypeScript types trong `types/index.ts`
- [ ] Tạo constants (alert colors, labels, icons) trong `utils/constants.ts`
- [ ] Tạo `utils/format.ts` (date formatting, relative time)
- [ ] Tạo `composables/useAlertLevel.ts`
- [ ] Xóa toàn bộ default template components (HelloWorld, TheWelcome, icons, etc.)
- [ ] Setup Google Fonts (Inter)
- [ ] Setup `main.css` với Tailwind directives
- [ ] Tạo mock data file `services/mock.ts`

**Files tạo mới:** ~8 files
**Files xóa:** HelloWorld.vue, TheWelcome.vue, WelcomeItem.vue, AboutView.vue, HomeView.vue, 5 icon components, counter.ts, base.css

### Phase 2: Layout System (Day 1-2)

**Mục tiêu:** Dashboard layout hoàn chỉnh

- [ ] `DashboardLayout.vue` — layout wrapper
- [ ] `AppSidebar.vue` — sidebar navigation
- [ ] `AppHeader.vue` — header bar
- [ ] `composables/useTheme.ts` — dark/light toggle
- [ ] Cập nhật `App.vue` — wrap với DashboardLayout
- [ ] Cập nhật `router/index.ts` — routes mới
- [ ] Responsive sidebar (collapse on tablet)

### Phase 3: UI Primitives (Day 2)

**Mục tiêu:** Component library cơ bản

- [ ] `StatusBadge.vue`
- [ ] `SummaryCard.vue`
- [ ] `EmptyState.vue`
- [ ] `LoadingSkeleton.vue`
- [ ] `ToastNotification.vue`
- [ ] `Modal.vue`
- [ ] `PageTitle.vue`
- [ ] `SearchBar.vue`

### Phase 4: Dashboard Page (Day 2-3)

**Mục tiêu:** Trang Dashboard hoàn chỉnh

- [ ] `overviewStore.ts` — Pinia store
- [ ] `DashboardView.vue` — page orchestration
- [ ] 6 SummaryCards với data mock
- [ ] `AlertDistributionChart.vue` — Donut chart
- [ ] `RecentChangesTable.vue` — bảng thay đổi
- [ ] Click interactions (card → filter list, row → detail)

### Phase 5: Student List Page (Day 3)

**Mục tiêu:** Danh sách học sinh với filtering

- [ ] `studentStore.ts` — Pinia store
- [ ] `StudentListView.vue` — page orchestration
- [ ] `StudentFilters.vue` — toolbar
- [ ] `StudentTable.vue` — desktop table
- [ ] `StudentCard.vue` — tablet card grid
- [ ] Search, filter, sort functionality

### Phase 6: Student Detail Page (Day 3-4)

**Mục tiêu:** Trang chi tiết đầy đủ

- [ ] `HeroCard.vue`
- [ ] `SignalSection.vue` + `SignalCard.vue` (×3)
- [ ] `TimelineChart.vue` — Chart.js integration
- [ ] `AlertHistoryTimeline.vue`
- [ ] `ActionForm.vue`
- [ ] `feedbackStore.ts`
- [ ] Toast on feedback submit

### Phase 7: Polish & Responsive (Day 4-5)

** mục tiêu:** Responsive, animations, edge cases

- [ ] Responsive testing (1024px, 768px breakpoints)
- [ ] Skeleton loading cho tất cả pages
- [ ] Empty states cho tất cả pages
- [ ] Page transitions
- [ ] Dark mode toggle (optional)
- [ ] Micro-animations (hover, click, enter)
- [ ] Error handling UI (API failures)
- [ ] Browser testing (Chrome, Firefox)

### Phase 8: Integration (Day 5)

**Mục tiêu:** Kết nối với backend thực

- [ ] Test với backend running (uvicorn)
- [ ] Xử lý error responses
- [ ] Remove mock data flag
- [ ] Final QA

---

## 11. Git Branching cho Frontend

```
frontend (current)
├── feat/fe-layout-system         ← Phase 2
├── feat/fe-ui-components         ← Phase 3
├── feat/fe-dashboard-page        ← Phase 4
├── feat/fe-student-list          ← Phase 5
├── feat/fe-student-detail        ← Phase 6
├── feat/fe-polish-responsive     ← Phase 7
└── feat/fe-backend-integration   ← Phase 8
```

Commit message pattern:
```
feat(fe/layout): add DashboardLayout with sidebar and header
feat(fe/components): add StatusBadge and SummaryCard
feat(fe/dashboard): implement overview page with charts
feat(fe/student-list): add filtering and responsive card view
feat(fe/student-detail): add signal cards and timeline chart
fix(fe/sidebar): correct mobile toggle behavior
chore(fe): update dependencies
```

---

## 12. Checklist chất lượng

Trước khi merge mỗi phase:

- [ ] Không có TypeScript errors (`npm run type-check`)
- [ ] Build thành công (`npm run build`)
- [ ] Responsive trên Desktop (1440px) và Tablet (768px)
- [ ] Loading states hiển thị đúng
- [ ] Empty states hiển thị đúng
- [ ] Không có z-score hay thuật toán thống kê nào trên UI
- [ ] Ngôn ngữ hiển thị: Tiếng Việt
- [ ] Màu sắc đúng mapping AlertLevel
- [ ] Hover animations mượt
- [ ] Keyboard navigation hoạt động (Tab, Enter)
- [ ] Không có console errors

---

## 13. Từ ngữ CẤM trên UI

| Từ cấm | Thay thế |
|---------|----------|
| Risk Score | Không dùng |
| AI Score | Không dùng |
| Z-score | Không dùng |
| Predict/Prediction | Không dùng |
| Dropout | "Bỏ học" chỉ trong context policy, KHÔNG trên UI |
| Dangerous/Nguy hiểm | Không dùng |
| Classification | Không dùng |
| Clustering | Không dùng |
| At-risk | "Cần theo dõi", "Cần xem xét" |
| Score | Mô tả bằng ngôn ngữ tự nhiên |

**Thay vào đó, mỗi cảnh báo phải có `explanation` bằng tiếng Việt tự nhiên, ví dụ:**
- "Điểm quiz gần đây thấp hơn đáng kể so với mức bình thường của em"
- "Em đã vắng mặt 2 buổi liên tiếp gần đây"
- "Bài nộp gần nhất đến trễ so với hạn chót"

---

## 14. Tóm tắt

Frontend Aegis AI là một **SaaS Dashboard hiện đại** với:

- **3 trang chính:** Dashboard, Danh sách HS, Chi tiết HS
- **17+ reusable components** tách biệt rõ ràng
- **3 Pinia stores** quản lý state
- **API service layer** tách biệt với mock support
- **TypeScript types** mirror hoàn toàn backend schemas
- **Tailwind CSS** với design tokens tùy biến
- **Chart.js** cho timeline visualization
- **Responsive** Desktop + Tablet
- **Dark/Light mode** optional

Triết lý xuyên suốt: **AI chỉ hỗ trợ phát hiện sớm, giáo viên đưa ra quyết định cuối cùng.**
