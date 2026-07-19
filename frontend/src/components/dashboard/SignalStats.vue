<script setup lang="ts">
import { computed } from 'vue'
import { BookOpen, ClipboardList, FileText } from 'lucide-vue-next'
import { useOverviewStore } from '@/stores/overviewStore'

const overviewStore = useOverviewStore()

const signals = [
  { key: 'grade', icon: BookOpen, color: '#3b82f6' },
  { key: 'attendance', icon: ClipboardList, color: '#22c55e' },
  { key: 'submission', icon: FileText, color: '#f59e0b' },
]

const signalStats = computed(() => overviewStore.stats?.signal_stats || {})
</script>

<template>
  <div class="grid grid-cols-3 gap-4">
    <div
      v-for="s in signals"
      :key="s.key"
      class="bg-white rounded-xl p-4 border border-gray-100"
    >
      <div v-if="signalStats[s.key]">
        <div class="flex items-center gap-2 mb-3">
          <div
            class="w-8 h-8 rounded-lg flex items-center justify-center"
            :style="{ backgroundColor: s.color + '15' }"
          >
            <component :is="s.icon" :size="16" :style="{ color: s.color }" />
          </div>
          <span class="text-xs font-medium text-gray-600">
            {{ signalStats[s.key].label }}
          </span>
        </div>

        <p class="text-xl font-bold text-gray-900">
          {{ signalStats[s.key].triggered }}<span class="text-sm font-normal text-gray-400">/{{ signalStats[s.key].total }}</span>
        </p>

        <div class="mt-2 h-1.5 bg-gray-100 rounded-full overflow-hidden">
          <div
            class="h-full rounded-full transition-all duration-500"
            :style="{
              width: signalStats[s.key].total > 0 ? ((signalStats[s.key].triggered / signalStats[s.key].total) * 100) + '%' : '0%',
              backgroundColor: s.color,
            }"
          />
        </div>

        <p class="mt-1.5 text-xs text-gray-400">
          {{ signalStats[s.key].triggered }} tín hiệu được kích hoạt
        </p>
      </div>
    </div>
  </div>
</template>
