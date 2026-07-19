<script setup lang="ts">
import { Eye } from 'lucide-vue-next'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import { formatRelativeTime, getInitials, getAvatarColor } from '@/utils/format'
import type { StudentSummary } from '@/types'

defineProps<{
  students: StudentSummary[]
  loading: boolean
}>()

const emit = defineEmits<{
  viewDetail: [studentId: string]
}>()
</script>

<template>
  <div class="hidden lg:block bg-white rounded-2xl overflow-hidden shadow-sm border border-gray-100">
    <div class="overflow-x-auto">
      <table class="w-full">
        <thead>
          <tr class="bg-gray-50">
            <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-12">
              STT
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Học sinh
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Ngành
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Trạng thái
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Tín hiệu
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Cập nhật
            </th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              Thao tác
            </th>
          </tr>
        </thead>

        <!-- Loading skeleton -->
        <tbody v-if="loading" class="divide-y divide-gray-100">
          <tr v-for="i in 5" :key="i" class="animate-pulse">
            <td class="px-4 py-4 text-center">
              <div class="h-4 w-6 bg-gray-200 rounded mx-auto" />
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-gray-200" />
                <div class="space-y-1.5">
                  <div class="h-4 w-32 bg-gray-200 rounded" />
                  <div class="h-3 w-20 bg-gray-200 rounded" />
                </div>
              </div>
            </td>
            <td class="px-6 py-4">
              <div class="h-4 w-28 bg-gray-200 rounded" />
            </td>
            <td class="px-6 py-4">
              <div class="h-6 w-24 bg-gray-200 rounded-full" />
            </td>
            <td class="px-6 py-4">
              <div class="h-6 w-8 bg-gray-200 rounded-full" />
            </td>
            <td class="px-6 py-4">
              <div class="h-4 w-20 bg-gray-200 rounded" />
            </td>
            <td class="px-6 py-4 text-right">
              <div class="h-8 w-20 bg-gray-200 rounded-lg ml-auto" />
            </td>
          </tr>
        </tbody>

        <!-- Data rows -->
        <tbody v-else-if="students.length > 0" class="divide-y divide-gray-100">
          <tr
            v-for="(student, index) in students"
            :key="student.student_id"
            class="hover:bg-gray-50 transition-colors"
          >
            <!-- STT -->
            <td class="px-4 py-4 text-center">
              <span class="text-sm font-medium text-gray-500">{{ index + 1 }}</span>
            </td>

            <!-- Avatar + Name + MSSV -->
            <td class="px-6 py-4">
              <div class="flex items-center gap-3">
                <div
                  class="w-10 h-10 rounded-full flex items-center justify-center text-white text-sm font-semibold flex-shrink-0"
                  :style="{ backgroundColor: getAvatarColor(student.student_name) }"
                >
                  {{ getInitials(student.student_name) }}
                </div>
                <div class="min-w-0">
                  <p class="text-sm font-medium text-gray-900 truncate">
                    {{ student.student_name }}
                  </p>
                  <p class="text-xs text-gray-500">{{ student.student_id }}</p>
                </div>
              </div>
            </td>

            <!-- Major -->
            <td class="px-6 py-4">
              <span class="text-sm text-gray-700">{{ student.major }}</span>
            </td>

            <!-- Alert Level -->
            <td class="px-6 py-4">
              <StatusBadge :level="student.alert_level" size="sm" />
            </td>

            <!-- Signal count -->
            <td class="px-6 py-4">
              <span
                class="inline-flex items-center justify-center min-w-[1.75rem] h-7 px-2 rounded-full text-xs font-semibold"
                :class="student.triggered_signal_count > 0
                  ? 'bg-red-50 text-red-600'
                  : 'bg-gray-100 text-gray-500'"
              >
                {{ student.triggered_signal_count }}
              </span>
            </td>

            <!-- Updated at -->
            <td class="px-6 py-4">
              <span class="text-sm text-gray-500">
                {{ formatRelativeTime(student.updated_at) }}
              </span>
            </td>

            <!-- Action -->
            <td class="px-6 py-4 text-right">
              <button
                @click="emit('viewDetail', student.student_id)"
                class="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-blue-600
                       bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
              >
                <Eye :size="14" />
                <span>Xem</span>
              </button>
            </td>
          </tr>
        </tbody>

        <!-- Empty state -->
        <tbody v-else>
          <tr>
            <td colspan="7" class="px-6 py-12 text-center">
              <p class="text-sm text-gray-500">Không tìm thấy học sinh</p>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
