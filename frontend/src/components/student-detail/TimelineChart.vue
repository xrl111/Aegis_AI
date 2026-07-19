<script setup lang="ts">
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'
import { Inbox } from 'lucide-vue-next'
import type { TimelinePoint } from '@/types'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend, Filler)

const props = defineProps<{
  timeline: TimelinePoint[]
}>()

const chartData = computed(() => ({
  labels: props.timeline.map((p) => p.week),
  datasets: [
    {
      label: 'Điểm số',
      data: props.timeline.map((p) => p.grade_value),
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59,130,246,0.08)',
      tension: 0.3,
      pointRadius: 3,
      pointHoverRadius: 6,
      spanGaps: false,
    },
    {
      label: 'Điểm danh',
      data: props.timeline.map((p) => p.attendance_value),
      borderColor: '#22c55e',
      backgroundColor: 'rgba(34,197,94,0.08)',
      tension: 0.3,
      pointRadius: 3,
      pointHoverRadius: 6,
      spanGaps: false,
    },
    {
      label: 'Nộp bài',
      data: props.timeline.map((p) => p.submission_value),
      borderColor: '#f59e0b',
      backgroundColor: 'rgba(245,158,11,0.08)',
      tension: 0.3,
      pointRadius: 3,
      pointHoverRadius: 6,
      spanGaps: false,
    },
  ],
}))

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index' as const,
    intersect: false,
  },
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: {
        usePointStyle: true,
        pointStyle: 'circle',
        padding: 20,
        font: { size: 12 },
      },
    },
    tooltip: {
      backgroundColor: '#1e293b',
      titleFont: { size: 12 },
      bodyFont: { size: 12 },
      padding: 10,
      cornerRadius: 8,
      callbacks: {
        label(ctx: any) {
          const val = ctx.raw as number | null
          if (val === null) return `${ctx.dataset.label}: Không có`
          return `${ctx.dataset.label}: ${Math.round(val * 100)}%`
        },
      },
    },
  },
  scales: {
    x: {
      grid: {
        color: 'rgba(0,0,0,0.04)',
        drawBorder: false,
      },
      ticks: {
        font: { size: 11 },
        color: '#94a3b8',
      },
    },
    y: {
      min: 0,
      max: 1,
      grid: {
        color: 'rgba(0,0,0,0.06)',
        drawBorder: false,
        lineWidth: 1,
      },
      ticks: {
        stepSize: 0.25,
        font: { size: 11 },
        color: '#94a3b8',
        callback(value: number | string) {
          const num = typeof value === 'string' ? parseFloat(value) : value
          return `${Math.round(num * 100)}%`
        },
      },
    },
  },
}))
</script>

<template>
  <div class="bg-surface rounded-2xl p-6 shadow-card">
    <h2 class="text-lg font-semibold text-gray-900 mb-4">Biểu đồ theo thời gian</h2>

    <template v-if="timeline.length > 0">
      <div style="height: 300px;">
        <Line :data="chartData" :options="chartOptions" />
      </div>
    </template>

    <template v-else>
      <div class="flex flex-col items-center justify-center py-12 text-gray-400">
        <Inbox :size="40" class="mb-3 opacity-50" />
        <p class="text-sm">Chưa có dữ liệu biểu đồ.</p>
      </div>
    </template>
  </div>
</template>
