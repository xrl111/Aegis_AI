<script setup lang="ts">
import { computed } from 'vue'
import type { SignalOut } from '@/types'
import { SIGNAL_ICONS, SIGNAL_LABELS } from '@/utils/constants'

const props = defineProps<{
  signal: SignalOut
}>()

const Icon = computed(() => SIGNAL_ICONS[props.signal.signal_type])

const signalLabel = computed(() => SIGNAL_LABELS[props.signal.signal_type])

const statusLabel = computed(() => {
  if (props.signal.data_sufficiency === 'insufficient') return 'Chưa đủ dữ liệu'
  if (props.signal.is_triggered) return 'Có vấn đề'
  return 'Bình thường'
})

const statusClasses = computed(() => {
  if (props.signal.data_sufficiency === 'insufficient') {
    return 'bg-gray-100 text-gray-500 border border-gray-200'
  }
  if (props.signal.is_triggered) {
    return 'bg-orange-50 text-orange-600 border border-orange-200'
  }
  return 'bg-green-50 text-green-600 border border-green-200'
})

const borderColor = computed(() => {
  if (props.signal.data_sufficiency === 'insufficient') return '#9ca3af'
  if (props.signal.is_triggered) return '#f97316'
  return '#22c55e'
})
</script>

<template>
  <div
    class="bg-surface rounded-xl p-4 border border-border transition-shadow hover:shadow-card-hover"
    :style="{ borderLeftWidth: '3px', borderLeftColor: borderColor }"
  >
    <!-- Header -->
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center gap-2">
        <component :is="Icon" :size="18" class="text-gray-500" />
        <span class="text-sm font-semibold text-gray-800">{{ signalLabel }}</span>
      </div>
      <span
        class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
        :class="statusClasses"
      >
        {{ statusLabel }}
      </span>
    </div>

    <!-- Body -->
    <p
      v-if="signal.data_sufficiency === 'insufficient'"
      class="text-sm text-gray-400 italic leading-relaxed"
    >
      Chưa đủ dữ liệu để đánh giá
    </p>
    <p v-else class="text-sm text-gray-600 leading-relaxed">
      {{ signal.explanation }}
    </p>
  </div>
</template>
