<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useStudentStore } from '@/stores/studentStore'
import PageTitle from '@/components/ui/PageTitle.vue'
import HeroCard from '@/components/student-detail/HeroCard.vue'
import SignalSection from '@/components/student-detail/SignalSection.vue'
import TimelineChart from '@/components/student-detail/TimelineChart.vue'
import AlertHistoryTimeline from '@/components/student-detail/AlertHistoryTimeline.vue'
import ActionForm from '@/components/feedback/ActionForm.vue'

const route = useRoute()
const studentStore = useStudentStore()

const studentId = computed(() => route.params.id as string)

onMounted(() => {
  if (studentId.value) {
    studentStore.fetchDetail(studentId.value)
  }
})
</script>

<template>
  <div class="min-h-screen bg-surface-secondary py-8">
    <div class="max-w-5xl mx-auto px-4 space-y-6">
      <!-- Page Title -->
      <PageTitle title="Chi tiết học sinh" back-to="/students" />

      <!-- Error state -->
      <div
        v-if="studentStore.error && !studentStore.detailLoading"
        class="bg-white rounded-2xl p-6 shadow-card border border-red-200"
      >
        <p class="text-sm text-red-600">{{ studentStore.error }}</p>
        <button
          @click="studentStore.fetchDetail(studentId)"
          class="mt-2 text-sm font-medium text-red-600 hover:text-red-700 underline"
        >
          Thử lại
        </button>
      </div>

      <!-- Loading skeleton -->
      <template v-if="studentStore.detailLoading">
        <!-- Hero skeleton -->
        <div class="bg-surface rounded-2xl p-6 shadow-card animate-pulse">
          <div class="flex items-start gap-5">
            <div class="w-16 h-16 rounded-full bg-gray-200" />
            <div class="flex-1 space-y-3">
              <div class="h-6 w-48 bg-gray-200 rounded" />
              <div class="h-4 w-64 bg-gray-200 rounded" />
              <div class="h-5 w-28 bg-gray-200 rounded-full" />
              <div class="h-4 w-80 bg-gray-200 rounded" />
            </div>
          </div>
        </div>

        <!-- Signals skeleton -->
        <div>
          <div class="h-6 w-32 bg-gray-200 rounded mb-4 animate-pulse" />
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div
              v-for="i in 3"
              :key="i"
              class="bg-surface rounded-xl p-4 border border-border animate-pulse"
            >
              <div class="flex items-center gap-2 mb-3">
                <div class="w-5 h-5 bg-gray-200 rounded" />
                <div class="h-4 w-24 bg-gray-200 rounded" />
              </div>
              <div class="space-y-2">
                <div class="h-3 w-full bg-gray-200 rounded" />
                <div class="h-3 w-3/4 bg-gray-200 rounded" />
              </div>
            </div>
          </div>
        </div>

        <!-- Chart skeleton -->
        <div class="bg-surface rounded-2xl p-6 shadow-card animate-pulse">
          <div class="h-6 w-44 bg-gray-200 rounded mb-4" />
          <div class="h-[300px] bg-gray-100 rounded-xl" />
        </div>

        <!-- Timeline skeleton -->
        <div>
          <div class="h-6 w-40 bg-gray-200 rounded mb-4 animate-pulse" />
          <div class="space-y-4">
            <div
              v-for="i in 3"
              :key="i"
              class="bg-surface border border-border rounded-xl p-4 animate-pulse ml-6"
            >
              <div class="h-3 w-24 bg-gray-200 rounded mb-2" />
              <div class="h-4 w-48 bg-gray-200 rounded mb-2" />
              <div class="h-3 w-full bg-gray-200 rounded" />
            </div>
          </div>
        </div>

        <!-- Form skeleton -->
        <div class="bg-surface rounded-2xl p-6 shadow-card animate-pulse">
          <div class="h-6 w-44 bg-gray-200 rounded mb-4" />
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
            <div
              v-for="i in 4"
              :key="i"
              class="h-20 bg-gray-100 rounded-xl"
            />
          </div>
          <div class="h-20 bg-gray-100 rounded-xl mb-4" />
          <div class="flex justify-end">
            <div class="h-10 w-36 bg-gray-200 rounded-xl" />
          </div>
        </div>
      </template>

      <!-- Empty state: student not found -->
      <template v-else-if="!studentStore.currentStudent">
        <div class="bg-surface rounded-2xl p-12 shadow-card text-center">
          <p class="text-gray-500 text-sm">
            Không tìm thấy thông tin học sinh. Vui lòng kiểm tra lại đường dẫn.
          </p>
        </div>
      </template>

      <!-- Student detail content -->
      <template v-else>
        <HeroCard :student="studentStore.currentStudent" />
        <SignalSection :signals="studentStore.currentStudent.signals" />
        <TimelineChart :timeline="studentStore.currentStudent.timeline" />
        <AlertHistoryTimeline :history="studentStore.currentStudent.alert_history" />
        <ActionForm :student-id="studentStore.currentStudent.student_id" />
      </template>
    </div>
  </div>
</template>
