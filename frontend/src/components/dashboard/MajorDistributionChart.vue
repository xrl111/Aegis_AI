<script setup lang="ts">
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from 'chart.js'
import { mockMajorDistribution } from '@/services/mock'

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend)

const chartData = computed(() => ({
  labels: mockMajorDistribution.map((m) => m.major),
  datasets: [
    { label: 'Ổn định', data: mockMajorDistribution.map((m) => m.stable), backgroundColor: '#22c55e', borderRadius: 6 },
    { label: 'Theo dõi', data: mockMajorDistribution.map((m) => m.watch), backgroundColor: '#eab308', borderRadius: 6 },
    { label: 'Cần xem xét', data: mockMajorDistribution.map((m) => m.review), backgroundColor: '#f97316', borderRadius: 6 },
    { label: 'Đang cải thiện', data: mockMajorDistribution.map((m) => m.improving), backgroundColor: '#3b82f6', borderRadius: 6 },
    { label: 'Chưa đủ DL', data: mockMajorDistribution.map((m) => m.insufficient), backgroundColor: '#9ca3af', borderRadius: 6 },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  indexAxis: 'y' as const,
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: { usePointStyle: true, pointStyle: 'circle', padding: 16, font: { size: 11 } },
    },
    tooltip: {
      backgroundColor: '#1e293b',
      padding: 10,
      cornerRadius: 8,
    },
  },
  scales: {
    x: {
      stacked: true,
      ticks: { font: { size: 11 }, color: '#94a3b8' },
      grid: { color: '#f1f5f9' },
      title: { display: true, text: 'Số học sinh', font: { size: 12 }, color: '#64748b' },
    },
    y: {
      stacked: true,
      ticks: { font: { size: 12 }, color: '#334155' },
      grid: { display: false },
    },
  },
}
</script>

<template>
  <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Phân bố theo ngành</h3>
    <div class="h-[200px]">
      <Bar :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>
