<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Users } from 'lucide-vue-next'
import { useStudentStore } from '@/stores/studentStore'
import type { AlertLevel } from '@/types'
import PageTitle from '@/components/ui/PageTitle.vue'
import EmptyState from '@/components/ui/EmptyState.vue'
import StudentTable from '@/components/students/StudentTable.vue'
import StudentCard from '@/components/students/StudentCard.vue'
import StudentFilters from '@/components/students/StudentFilters.vue'

const router = useRouter()
const route = useRoute()
const store = useStudentStore()

const VALID_LEVELS: AlertLevel[] = [
  'stable', 'watch', 'review', 'improving', 'insufficient_data',
]

onMounted(async () => {
  // Apply ?level= query param filter if present (supports comma-separated)
  const levelParam = route.query.level as string | undefined
  if (levelParam) {
    const levels = levelParam
      .split(',')
      .filter((l): l is AlertLevel => VALID_LEVELS.includes(l as AlertLevel))
    if (levels.length > 0) {
      store.filters.levels = levels
    }
  }

  await store.fetchAll()
})

const resultCount = computed(() => store.filteredStudents.length)

function handleViewDetail(studentId: string) {
  router.push(`/students/${studentId}`)
}
</script>

<template>
  <div class="space-y-6 animate-fade-in">
    <!-- Page Title -->
    <PageTitle title="Danh sách học sinh" />

    <!-- Error state -->
    <div
      v-if="store.error"
      class="p-4 rounded-xl bg-red-50 border border-red-200 flex items-center gap-3"
    >
      <span class="text-sm text-red-600">{{ store.error }}</span>
      <button
        @click="store.fetchAll()"
        class="ml-auto text-sm font-medium text-red-600 hover:text-red-700 underline"
      >
        Thử lại
      </button>
    </div>

    <!-- Filters Toolbar -->
    <StudentFilters />

    <!-- Results count -->
    <p class="text-sm text-gray-500">
      Hiển thị <span class="font-medium text-gray-700">{{ resultCount }}</span> học sinh
    </p>

    <!-- Desktop Table (lg+) -->
    <StudentTable
      :students="store.filteredStudents"
      :loading="store.loading"
      @view-detail="handleViewDetail"
    />

    <!-- Mobile / Tablet Cards (below lg) -->
    <div v-if="!store.loading" class="grid grid-cols-1 md:grid-cols-2 gap-4 lg:hidden">
      <StudentCard
        v-for="(student, index) in store.filteredStudents"
        :key="student.student_id"
        :student="student"
        :index="index"
        @view-detail="handleViewDetail"
      />
    </div>

    <!-- Mobile / Tablet Loading skeletons -->
    <div v-if="store.loading" class="grid grid-cols-1 md:grid-cols-2 gap-4 lg:hidden">
      <div
        v-for="i in 6"
        :key="i"
        class="bg-white rounded-2xl p-4 shadow-sm border border-gray-100 animate-pulse"
      >
        <div class="flex items-center gap-3 mb-3">
          <div class="w-10 h-10 rounded-full bg-gray-200" />
          <div class="space-y-1.5">
            <div class="h-4 w-32 bg-gray-200 rounded" />
            <div class="h-3 w-20 bg-gray-200 rounded" />
          </div>
        </div>
        <div class="flex gap-2 mb-3">
          <div class="h-6 w-24 bg-gray-200 rounded-full" />
          <div class="h-6 w-16 bg-gray-200 rounded-full" />
        </div>
        <div class="h-3 w-full bg-gray-200 rounded mb-1" />
        <div class="h-3 w-3/4 bg-gray-200 rounded mb-3" />
        <div class="flex items-center justify-between pt-2 border-t border-gray-100">
          <div class="h-3 w-20 bg-gray-200 rounded" />
          <div class="h-3 w-16 bg-gray-200 rounded" />
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <EmptyState
      v-if="!store.loading && resultCount === 0"
      :icon="Users"
      title="Không tìm thấy học sinh"
      description="Thử thay đổi bộ lọc hoặc từ khóa tìm kiếm để xem kết quả khác."
    />
  </div>
</template>
