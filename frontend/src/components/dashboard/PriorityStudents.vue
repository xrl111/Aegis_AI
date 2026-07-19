<script setup lang="ts">
import { mockPriorityStudents } from '@/services/mock'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import { getInitials, getAvatarColor } from '@/utils/format'

const emit = defineEmits<{
  viewDetail: [studentId: string]
}>()
</script>

<template>
  <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
    <div class="mb-4">
      <h3 class="text-lg font-semibold text-gray-900">Học sinh cần ưu tiên</h3>
      <p class="text-sm text-gray-500 mt-0.5">Sắp xếp theo số tín hiệu kích hoạt</p>
    </div>

    <div class="divide-y divide-gray-100">
      <div
        v-for="student in mockPriorityStudents"
        :key="student.student_id"
        class="flex items-center gap-3 py-3 px-2 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
        @click="emit('viewDetail', student.student_id)"
      >
        <div
          class="w-9 h-9 rounded-full flex items-center justify-center text-white text-xs font-semibold flex-shrink-0"
          :style="{ backgroundColor: getAvatarColor(student.student_name) }"
        >
          {{ getInitials(student.student_name) }}
        </div>

        <div class="min-w-0 flex-1">
          <div class="flex items-center gap-2">
            <p class="text-sm font-medium text-gray-900 truncate">{{ student.student_name }}</p>
            <StatusBadge :level="student.alert_level" size="sm" />
          </div>
          <p class="text-xs text-gray-500 line-clamp-1">{{ student.headline }}</p>
        </div>

        <span
          class="inline-flex items-center justify-center min-w-[1.5rem] h-6 px-1.5 rounded-full text-xs font-semibold flex-shrink-0"
          :class="student.triggered_signal_count > 0
            ? 'bg-red-50 text-red-600'
            : 'bg-gray-100 text-gray-500'"
        >
          {{ student.triggered_signal_count }}
        </span>
      </div>
    </div>
  </div>
</template>
