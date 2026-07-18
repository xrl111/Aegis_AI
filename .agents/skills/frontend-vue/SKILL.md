---
name: frontend-vue
description: |
  Skill hỗ trợ phát triển frontend Vue 3 cho Aegis AI.
  Trigger khi làm việc với Vue components, TypeScript, Pinia stores,
  hoặc bất kỳ file nào trong frontend/.
---

# Frontend Vue 3 — Development Skill

## Kiến trúc Frontend

```
frontend/src/
├── App.vue                    # Root component + layout
├── main.ts                    # App bootstrap
├── router/index.ts            # Route definitions
├── stores/                    # Pinia stores (state + API calls)
│   ├── studentStore.ts        # Student list + detail
│   ├── overviewStore.ts       # Dashboard stats
│   └── feedbackStore.ts       # Teacher feedback
├── views/                     # Page-level components (1 per route)
│   ├── OverviewView.vue       # Trang tổng quan
│   ├── StudentDetailView.vue  # Chi tiết 1 học sinh
│   └── FeedbackView.vue       # Phản hồi giáo viên
├── components/                # Reusable UI components
│   ├── StatusBadge.vue        # Badge màu theo trạng thái
│   ├── AlertCard.vue          # Card cảnh báo expandable
│   ├── TimelineChart.vue      # Biểu đồ timeline
│   └── StudentTable.vue       # Bảng danh sách HS
├── types/                     # TypeScript interfaces
│   └── index.ts               # StudentSummary, SignalResult, etc.
└── services/                  # API client
    └── api.ts                 # Axios/fetch wrapper
```

## Quy tắc khi code frontend

### 1. Component Pattern — `<script setup>` + TypeScript

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useStudentStore } from '@/stores/studentStore'
import StatusBadge from '@/components/StatusBadge.vue'
import type { StudentSummary } from '@/types'

// Props
const props = defineProps<{
  studentId: string
}>()

// Store — tất cả API call đi qua store
const studentStore = useStudentStore()

// Computed
const alertLevel = computed(() => studentStore.currentStudent?.alertLevel)

// Lifecycle
onMounted(() => {
  studentStore.fetchDetail(props.studentId)
})
</script>

<template>
  <div class="student-detail">
    <StatusBadge :level="alertLevel" />
    <!-- ... -->
  </div>
</template>
```

### 2. API Call — Luôn qua Pinia Store

```typescript
// ✅ Đúng — store gọi API
// stores/studentStore.ts
export const useStudentStore = defineStore('student', () => {
  const students = ref<StudentSummary[]>([])
  const loading = ref(false)

  async function fetchAll() {
    loading.value = true
    try {
      const res = await api.get('/api/students')
      students.value = res.data
    } finally {
      loading.value = false
    }
  }

  return { students, loading, fetchAll }
})

// ❌ Sai — component gọi API trực tiếp
// SomeComponent.vue
onMounted(async () => {
  const res = await fetch('/api/students')  // KHÔNG!
})
```

### 3. TypeScript Types — Mirror API schemas

```typescript
// types/index.ts — phải khớp với backend/api/schemas.py

export type AlertLevel =
  | 'insufficient_data'
  | 'stable'
  | 'watch'
  | 'review'
  | 'improving'

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
  signal_type: 'grade' | 'attendance' | 'submission'
  is_triggered: boolean
  data_sufficiency: 'sufficient' | 'partial' | 'insufficient'
  explanation: string    // Tiếng Việt, phi kỹ thuật — KHÔNG có z-score
}
```

### 4. Màu sắc trạng thái — Thống nhất toàn app

```typescript
// Mapping chuẩn — dùng ở mọi nơi hiển thị trạng thái
export const ALERT_COLORS: Record<AlertLevel, string> = {
  stable: '#22c55e',            // Xanh lá
  watch: '#eab308',             // Vàng
  review: '#f97316',            // Cam
  insufficient_data: '#9ca3af', // Xám
  improving: '#3b82f6',         // Xanh dương
}

export const ALERT_LABELS: Record<AlertLevel, string> = {
  stable: 'Ổn định',
  watch: 'Theo dõi thay đổi',
  review: 'Cần giáo viên xem xét',
  insufficient_data: 'Chưa đủ dữ liệu',
  improving: 'Đang cải thiện',
}
```

### 5. Ngôn ngữ hiển thị — Tiếng Việt

- Mọi label, button, heading: **Tiếng Việt**
- Placeholder, tooltip: Tiếng Việt
- Error messages cho user: Tiếng Việt
- Code comments, variable names: Tiếng Anh

### 6. Vite Proxy — Dev environment

```typescript
// vite.config.ts — proxy API calls tới backend
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

### 7. Router Setup

```typescript
// router/index.ts
const routes = [
  { path: '/', name: 'overview', component: OverviewView },
  { path: '/student/:id', name: 'student-detail', component: StudentDetailView },
  { path: '/feedback', name: 'feedback', component: FeedbackView },
]
```

## Ràng buộc UI (luôn check)

- [ ] KHÔNG hiển thị z-score hay con số thống kê thô cho giáo viên
- [ ] KHÔNG dùng label "nguy hiểm", "sẽ bỏ học", "yếu kém"
- [ ] Mỗi cảnh báo có headline (1 dòng) + chi tiết (expandable)
- [ ] Màu sắc đúng mapping (xanh/vàng/cam/xám/xanh dương)
- [ ] "Chưa đủ dữ liệu" là trạng thái riêng, không ẩn đi

## Chạy dev server

```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
# API proxy → http://localhost:8000
```
