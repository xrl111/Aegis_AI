<script setup lang="ts">
import { Info } from 'lucide-vue-next'
import type { StudentDetail } from '@/types'
import { getInitials, getAvatarColor } from '@/utils/format'
import StatusBadge from '@/components/ui/StatusBadge.vue'

defineProps<{
  student: StudentDetail
}>()
</script>

<template>
  <div class="bg-surface rounded-2xl p-6 shadow-card">
    <div class="flex items-start gap-5">
      <!-- Avatar -->
      <div
        class="shrink-0 flex items-center justify-center w-16 h-16 rounded-full text-white text-xl font-bold"
        :style="{ backgroundColor: getAvatarColor(student.student_name) }"
      >
        {{ getInitials(student.student_name) }}
      </div>

      <!-- Info -->
      <div class="flex-1 min-w-0">
        <h2 class="text-xl font-semibold text-gray-900">{{ student.student_name }}</h2>
        <p class="text-sm text-gray-500 mt-0.5">
          {{ student.student_id }} &middot; {{ student.major }}
        </p>

        <div class="mt-3">
          <StatusBadge :level="student.alert_level" size="md" />
        </div>

        <p class="text-sm text-gray-600 italic mt-2 max-w-lg leading-relaxed">
          {{ student.headline }}
        </p>
      </div>
    </div>

    <!-- Seasonal suppression banner -->
    <div
      v-if="student.is_seasonal_suppressed"
      class="flex items-center gap-2 mt-4 px-4 py-2.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-700 text-sm"
    >
      <Info :size="16" class="shrink-0" />
      <span>Cảnh báo đang được lọc do ảnh hưởng mùa học</span>
    </div>
  </div>
</template>
