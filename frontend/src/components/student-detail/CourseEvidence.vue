<script setup lang="ts">
import type { CourseDetail } from '@/types'
import { BookOpen } from 'lucide-vue-next'

defineProps<{
  courses: CourseDetail[]
}>()

// Helper format điểm thành chuỗi hiển thị
function formatScore(score: number): string {
  return score.toFixed(1)
}
</script>

<template>
  <div class="bg-surface rounded-2xl p-6 shadow-card">
    <div class="flex items-center gap-2 mb-4">
      <BookOpen class="text-blue-500" :size="20" />
      <h2 class="text-lg font-semibold text-gray-900">Chi tiết bảng điểm & chuyên cần</h2>
    </div>

    <div v-if="courses && courses.length > 0" class="overflow-x-auto">
      <table class="w-full text-left border-collapse min-w-[600px]">
        <thead>
          <tr class="border-b border-border text-sm text-gray-500">
            <th class="py-3 px-4 font-medium">Môn học</th>
            <th class="py-3 px-4 font-medium">Điểm thành phần</th>
            <th class="py-3 px-4 font-medium text-right w-32">Chuyên cần</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-border">
          <tr v-for="course in courses" :key="course.course_id" class="text-sm">
            <td class="py-4 px-4 align-top">
              <div class="font-medium text-gray-900">{{ course.course_id }}</div>
              <div class="text-xs text-gray-500">{{ course.course_name }}</div>
            </td>
            <td class="py-4 px-4">
              <div class="flex flex-wrap gap-2">
                <div 
                  v-for="(g, idx) in course.grades" 
                  :key="idx"
                  class="bg-gray-50 border border-gray-200 rounded px-2 py-1 text-xs"
                >
                  <span class="text-gray-500">{{ g.assessment }}:</span> 
                  <span 
                    class="font-medium ml-1"
                    :class="g.score <= g.class_average - 2.0 ? 'text-red-600 font-bold' : 'text-gray-900'"
                  >{{ formatScore(g.score) }}</span>
                  <span class="text-gray-400 ml-1 font-normal">(avg: {{ formatScore(g.class_average) }})</span>
                </div>
              </div>
            </td>
            <td class="py-4 px-4 text-right align-top">
              <span 
                class="font-medium" 
                :class="course.attendance_rate < 0.75 ? 'text-red-600' : 'text-gray-900'"
              >
                {{ Math.round(course.attendance_rate * 100) }}%
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="text-center py-8 text-gray-400">
      <p class="text-sm">Chưa có dữ liệu môn học trong học kỳ này.</p>
    </div>
  </div>
</template>
