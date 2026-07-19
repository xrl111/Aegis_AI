<script setup lang="ts">
import { ExternalLink, Eye } from 'lucide-vue-next'
import { RouterLink } from 'vue-router'
import type { StudentSummary } from '@/types'
import { formatRelativeTime, getInitials, getAvatarColor } from '@/utils/format'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import LoadingSkeleton from '@/components/ui/LoadingSkeleton.vue'

defineProps<{
  students: StudentSummary[]
  loading: boolean
}>()

const emit = defineEmits<{
  viewDetail: [studentId: string]
}>()
</script>

<template>
  <div class="rounded-2xl bg-white shadow overflow-hidden">
    <!-- Header -->
    <div class="flex items-center justify-between px-6 py-4">
      <h3 class="text-lg font-semibold text-gray-900">
        Các thay đổi gần đây
      </h3>
      <RouterLink
        to="/students"
        class="inline-flex items-center gap-1 text-sm font-medium text-blue-600 hover:text-blue-700"
      >
        Xem tất cả
        <ExternalLink :size="14" />
      </RouterLink>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="px-6 pb-6">
      <LoadingSkeleton type="row" :count="5" />
    </div>

    <!-- Table -->
    <div v-else class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-100 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
            <th class="px-6 py-3">Học sinh</th>
            <th class="px-6 py-3">Ngành</th>
            <th class="px-6 py-3">Mức</th>
            <th class="px-6 py-3">Tín hiệu</th>
            <th class="px-6 py-3">Cập nhật</th>
            <th class="px-6 py-3 text-right">Thao tác</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr
            v-for="student in students"
            :key="student.student_id"
            class="cursor-pointer transition-colors hover:bg-gray-50"
            @click="emit('viewDetail', student.student_id)"
          >
            <!-- Student name with avatar -->
            <td class="whitespace-nowrap px-6 py-3">
              <div class="flex items-center gap-3">
                <div
                  class="flex h-9 w-9 items-center justify-center rounded-full text-xs font-semibold text-white"
                  :style="{ backgroundColor: getAvatarColor(student.student_name) }"
                >
                  {{ getInitials(student.student_name) }}
                </div>
                <span class="font-medium text-gray-900">
                  {{ student.student_name }}
                </span>
              </div>
            </td>

            <!-- Major -->
            <td class="whitespace-nowrap px-6 py-3 text-gray-500">
              {{ student.major }}
            </td>

            <!-- Alert level badge -->
            <td class="whitespace-nowrap px-6 py-3">
              <StatusBadge :level="student.alert_level" size="sm" />
            </td>

            <!-- Triggered signals count -->
            <td class="whitespace-nowrap px-6 py-3">
              <span
                class="inline-flex items-center justify-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-700"
              >
                {{ student.triggered_signal_count }}
              </span>
            </td>

            <!-- Relative time -->
            <td class="whitespace-nowrap px-6 py-3 text-gray-500">
              {{ formatRelativeTime(student.updated_at) }}
            </td>

            <!-- Action button -->
            <td class="whitespace-nowrap px-6 py-3 text-right">
              <button
                class="inline-flex items-center gap-1 rounded-lg bg-blue-50 px-3 py-1.5 text-xs font-medium text-blue-600 transition-colors hover:bg-blue-100"
                @click.stop="emit('viewDetail', student.student_id)"
              >
                <Eye :size="14" />
                Xem
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Empty state -->
      <div
        v-if="!loading && students.length === 0"
        class="flex flex-col items-center justify-center py-12 text-gray-400"
      >
        <p class="text-sm">Không có thay đổi nào gần đây</p>
      </div>
    </div>
  </div>
</template>
