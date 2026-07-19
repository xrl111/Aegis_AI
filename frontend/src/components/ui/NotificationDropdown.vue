<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { AlertTriangle, Eye, X } from 'lucide-vue-next'
import { useOverviewStore } from '@/stores/overviewStore'
import { getInitials, getAvatarColor, formatRelativeTime } from '@/utils/format'
import { ALERT_CONFIG } from '@/utils/constants'
import type { StudentSummary } from '@/types'

const router = useRouter()
const overviewStore = useOverviewStore()
const isOpen = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)

const alertStudents = computed(() => {
  return overviewStore.recentChanges.filter(
    (s) => s.alert_level === 'review' || s.alert_level === 'watch'
  )
})

const reviewCount = computed(
  () => overviewStore.stats?.review_count ?? 0
)
const watchCount = computed(
  () => overviewStore.stats?.watch_count ?? 0
)
const totalCount = computed(() => reviewCount.value + watchCount.value)

function goToStudent(id: string) {
  isOpen.value = false
  router.push(`/students/${id}`)
}

function goToFiltered(level: string) {
  isOpen.value = false
  router.push({ path: '/students', query: { level } })
}

function handleClickOutside(e: MouseEvent) {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target as Node)) {
    isOpen.value = false
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onUnmounted(() => document.removeEventListener('click', handleClickOutside))
</script>

<template>
  <div ref="dropdownRef" class="relative">
    <!-- Bell button -->
    <button
      type="button"
      class="relative inline-flex h-9 w-9 items-center justify-center rounded-lg text-gray-500 transition-colors hover:bg-gray-100 hover:text-gray-700"
      aria-label="Thông báo"
      @click="isOpen = !isOpen"
    >
      <svg class="h-[18px] w-[18px]" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" />
        <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" />
      </svg>
      <span
        v-if="totalCount > 0"
        class="absolute -right-0.5 -top-0.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-red-500 px-1 text-[10px] font-bold text-white"
      >
        {{ totalCount > 99 ? '99+' : totalCount }}
      </span>
    </button>

    <!-- Dropdown -->
    <Transition
      enter-active-class="transition-all duration-200 ease-out"
      enter-from-class="opacity-0 scale-95 -translate-y-1"
      enter-to-class="opacity-100 scale-100 translate-y-0"
      leave-active-class="transition-all duration-150 ease-in"
      leave-from-class="opacity-100 scale-100 translate-y-0"
      leave-to-class="opacity-0 scale-95 -translate-y-1"
    >
      <div
        v-if="isOpen"
        class="absolute right-0 top-full mt-2 w-80 bg-white rounded-2xl border border-gray-200 shadow-xl z-50 overflow-hidden"
      >
        <!-- Header -->
        <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100">
          <div>
            <h3 class="text-sm font-semibold text-gray-900">Thông báo</h3>
            <p v-if="totalCount > 0" class="text-xs text-gray-500">
              {{ reviewCount }} cần xem xét, {{ watchCount }} cần theo dõi
            </p>
          </div>
          <button
            v-if="totalCount > 0"
            @click="goToFiltered('review,watch')"
            class="text-xs text-blue-600 font-medium hover:text-blue-700"
          >
            Xem tất cả
          </button>
        </div>

        <!-- List -->
        <div class="max-h-80 overflow-y-auto">
          <template v-if="alertStudents.length > 0">
            <div
              v-for="student in alertStudents.slice(0, 8)"
              :key="student.student_id"
              @click="goToStudent(student.student_id)"
              class="flex items-start gap-3 px-4 py-3 hover:bg-gray-50 cursor-pointer transition-colors border-b border-gray-50 last:border-0"
            >
              <!-- Avatar -->
              <div
                class="w-8 h-8 rounded-full flex items-center justify-center text-white text-xs font-semibold flex-shrink-0 mt-0.5"
                :style="{ backgroundColor: getAvatarColor(student.student_name) }"
              >
                {{ getInitials(student.student_name) }}
              </div>

              <!-- Content -->
              <div class="min-w-0 flex-1">
                <div class="flex items-center gap-2">
                  <span class="text-sm font-medium text-gray-900 truncate">
                    {{ student.student_name }}
                  </span>
                  <span
                    class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded-full text-[10px] font-medium flex-shrink-0"
                    :style="{
                      backgroundColor: ALERT_CONFIG[student.alert_level].bg,
                      color: ALERT_CONFIG[student.alert_level].color,
                    }"
                  >
                    <component :is="ALERT_CONFIG[student.alert_level].icon" :size="10" />
                    {{ ALERT_CONFIG[student.alert_level].label }}
                  </span>
                </div>
                <p class="text-xs text-gray-500 line-clamp-1 mt-0.5">
                  {{ student.headline }}
                </p>
                <p class="text-[10px] text-gray-400 mt-0.5">
                  {{ formatRelativeTime(student.updated_at) }}
                </p>
              </div>
            </div>
          </template>

          <!-- Empty -->
          <div v-else class="px-4 py-8 text-center">
            <p class="text-sm text-gray-400">Không có thông báo mới</p>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>
