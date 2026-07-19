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
} from 'chart.js'
import { mockWeeklyTrend } from '@/services/mock'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend)

const chartData = computed(() => ({
  labels: mockWeeklyTrend.map((w) => w.week),
  datasets: [
    {
      label: 'Ổn định',
      data: mockWeeklyTrend.map((w) => w.stable),
      borderColor: '#22c55e',
      backgroundColor: '#22c55e20',
      tension: 0.3,
      pointRadius: 4,
      pointHoverRadius: 6,
      borderWidth: 2,
      fill: false,
    },
    {
      label: 'Theo dõi',
      data: mockWeeklyTrend.map((w) => w.watch),
      borderColor: '#eab308',
      backgroundColor: '#eab30820',
      tension: 0.3,
      pointRadius: 4,
      pointHoverRadius: 6,
      borderWidth: 2,
      fill: false,
    },
    {
      label: 'Cần xem xét',
      data: mockWeeklyTrend.map((w) => w.review),
      borderColor: '#f97316',
      backgroundColor: '#f9731620',
      tension: 0.3,
      pointRadius: 4,
      pointHoverRadius: 6,
      borderWidth: 2,
      fill: false,
    },
    {
      label: 'Đang cải thiện',
      data: mockWeeklyTrend.map((w) => w.improving),
      borderColor: '#3b82f6',
      backgroundColor: '#3b82f620',
      tension: 0.3,
      pointRadius: 4,
      pointHoverRadius: 6,
      borderWidth: 2,
      fill: false,
    },
    {
      label: 'Chưa đủ DL',
      data: mockWeeklyTrend.map((w) => w.insufficient),
      borderColor: '#9ca3af',
      backgroundColor: '#9ca3af20',
      tension: 0.3,
      pointRadius: 4,
      pointHoverRadius: 6,
      borderWidth: 2,
      fill: false,
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index' as const, intersect: false },
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: { usePointStyle: true, pointStyle: 'circle', padding: 16, font: { size: 12 } },
    },
    tooltip: {
      backgroundColor: '#1e293b',
      padding: 10,
      cornerRadius: 8,
      titleFont: { size: 12 },
      bodyFont: { size: 12 },
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: { stepSize: 5, font: { size: 11 }, color: '#94a3b8' },
      grid: { color: '#f1f5f9' },
      title: { display: true, text: 'Số học sinh', font: { size: 12 }, color: '#64748b' },
    },
    x: {
      ticks: { font: { size: 11 }, color: '#94a3b8' },
      grid: { display: false },
    },
  },
}
</script>

<template>
  <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Xu hướng theo tuần</h3>
    <div class="h-[280px]">
      <Line :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>
