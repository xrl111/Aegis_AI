<script setup lang="ts">
import { ChevronRight } from 'lucide-vue-next'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import { formatRelativeTime, getInitials, getAvatarColor } from '@/utils/format'
import type { StudentSummary } from '@/types'

defineProps<{
  student: StudentSummary
  index: number
}>()

const emit = defineEmits<{
  viewDetail: [studentId: string]
}>()
</script>

<template>
  <div
    @click="emit('viewDetail', student.student_id)"
    class="bg-white rounded-2xl p-4 shadow-card hover:shadow-card-hover
           transition-all duration-200 cursor-pointer border border-gray-100
           flex flex-col gap-3"
  >
    <!-- Header: STT + Avatar + Name + MSSV -->
    <div class="flex items-center gap-3">
      <span class="text-xs font-medium text-gray-400 w-5 text-center flex-shrink-0">
        {{ index + 1 }}
      </span>
      <div
        class="w-10 h-10 rounded-full flex items-center justify-center text-white text-sm font-semibold flex-shrink-0"
        :style="{ backgroundColor: getAvatarColor(student.student_name) }"
      >
        {{ getInitials(student.student_name) }}
      </div>
      <div class="min-w-0 flex-1">
        <p class="text-sm font-semibold text-gray-900 truncate">
          {{ student.student_name }}
        </p>
        <p class="text-xs text-gray-500">{{ student.student_id }}</p>
      </div>
    </div>

    <!-- Status + Signal count -->
    <div class="flex items-center gap-2">
      <StatusBadge :level="student.alert_level" size="sm" />
      <span
        class="inline-flex items-center justify-center min-w-[1.5rem] h-6 px-1.5 rounded-full text-xs font-semibold"
        :class="student.triggered_signal_count > 0
          ? 'bg-red-50 text-red-600'
          : 'bg-gray-100 text-gray-500'"
      >
        {{ student.triggered_signal_count }} tín hiệu
      </span>
    </div>

    <!-- Headline -->
    <p
      v-if="student.headline"
      class="text-sm text-gray-500 line-clamp-2 leading-relaxed"
    >
      {{ student.headline }}
    </p>

    <!-- Footer: Updated + CTA -->
    <div class="flex items-center justify-between mt-auto pt-2 border-t border-gray-100">
      <span class="text-xs text-gray-400">
        {{ formatRelativeTime(student.updated_at) }}
      </span>
      <span
        class="inline-flex items-center gap-1 text-xs font-medium text-blue-600 group-hover:text-blue-700"
      >
        Xem chi tiết
        <ChevronRight :size="14" />
      </span>
    </div>
  </div>
</template>
