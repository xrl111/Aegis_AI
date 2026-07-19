<script setup lang="ts">
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import type { OverviewStats, AlertLevel } from '@/types'
import { ALERT_CONFIG } from '@/utils/constants'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps<{
  stats: OverviewStats
}>()

const LEVEL_ORDER: AlertLevel[] = [
  'stable',
  'watch',
  'review',
  'improving',
  'insufficient_data',
]

const LEVEL_COLORS: Record<AlertLevel, string> = {
  stable: '#22c55e',
  watch: '#eab308',
  review: '#f97316',
  improving: '#3b82f6',
  insufficient_data: '#9ca3af',
}

const COUNT_KEY: Record<AlertLevel, keyof OverviewStats> = {
  stable: 'stable_count',
  watch: 'watch_count',
  review: 'review_count',
  improving: 'improving_count',
  insufficient_data: 'insufficient_count',
}

const chartData = computed(() => ({
  labels: LEVEL_ORDER.map((l) => ALERT_CONFIG[l].label),
  datasets: [
    {
      data: LEVEL_ORDER.map((l) => props.stats[COUNT_KEY[l]] as number),
      backgroundColor: LEVEL_ORDER.map((l) => LEVEL_COLORS[l]),
      borderWidth: 0,
      hoverOffset: 4,
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  cutout: '65%',
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      callbacks: {
        label: (ctx: { parsed: number; label: string }) => {
          return ` ${ctx.label}: ${ctx.parsed} học sinh`
        },
      },
    },
  },
}
</script>

<template>
  <div class="rounded-2xl bg-white p-6 shadow">
    <h3 class="text-lg font-semibold text-gray-900">
      Phân bố học sinh theo mức
    </h3>

    <div class="mt-4 flex items-center gap-6">
      <!-- Chart with center text overlay -->
      <div class="relative h-52 w-52 flex-shrink-0">
        <Doughnut :data="chartData" :options="chartOptions" />
        <!-- Center text -->
        <div
          class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none"
        >
          <span class="text-2xl font-bold text-gray-900">
            {{ stats.total_students }}
          </span>
          <span class="text-xs text-gray-500">học sinh</span>
        </div>
      </div>

      <!-- Custom legend -->
      <div class="flex flex-1 flex-col gap-2.5">
        <div
          v-for="level in LEVEL_ORDER"
          :key="level"
          class="flex items-center gap-2.5"
        >
          <span
            class="inline-block h-3 w-3 rounded-full flex-shrink-0"
            :style="{ backgroundColor: LEVEL_COLORS[level] }"
          />
          <span class="flex-1 text-sm text-gray-600">
            {{ ALERT_CONFIG[level].label }}
          </span>
          <span class="text-sm font-medium text-gray-900 tabular-nums">
            {{ stats[COUNT_KEY[level]] }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
