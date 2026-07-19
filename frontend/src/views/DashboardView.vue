<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useOverviewStore } from '@/stores/overviewStore'
import PageTitle from '@/components/ui/PageTitle.vue'
import SummaryCard from '@/components/ui/SummaryCard.vue'
import WarningBanner from '@/components/ui/WarningBanner.vue'
import AlertDistributionChart from '@/components/dashboard/AlertDistributionChart.vue'
import RecentChangesTable from '@/components/dashboard/RecentChangesTable.vue'
import TrendChart from '@/components/dashboard/TrendChart.vue'
import MajorDistributionChart from '@/components/dashboard/MajorDistributionChart.vue'
import SignalStats from '@/components/dashboard/SignalStats.vue'
import PriorityStudents from '@/components/dashboard/PriorityStudents.vue'
import { Users, CheckCircle, Eye, AlertTriangle, TrendingUp, HelpCircle } from 'lucide-vue-next'

const router = useRouter()
const overviewStore = useOverviewStore()

onMounted(() => {
  overviewStore.fetchStats()
  overviewStore.fetchRecentChanges()
})

function navigateToStudents(level?: string) {
  if (level) {
    router.push({ path: '/students', query: { level } })
  } else {
    router.push('/students')
  }
}

function viewDetail(studentId: string) {
  router.push(`/students/${studentId}`)
}
</script>

<template>
  <div class="animate-fade-in space-y-6">
    <PageTitle title="Tổng quan" subtitle="Theo dõi tình hình học tập của học sinh" />

    <!-- Warning Banner -->
    <WarningBanner />

    <!-- Error state -->
    <div
      v-if="overviewStore.error"
      class="p-4 rounded-xl bg-red-50 border border-red-200 flex items-center gap-3"
    >
      <span class="text-sm text-red-600">{{ overviewStore.error }}</span>
      <button
        @click="overviewStore.fetchStats()"
        class="ml-auto text-sm font-medium text-red-600 hover:text-red-700 underline"
      >
        Thử lại
      </button>
    </div>

    <!-- Loading state -->
    <template v-if="overviewStore.loading && !overviewStore.stats">
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="i in 6" :key="i" class="h-24 bg-white rounded-2xl animate-pulse" />
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">
        <div class="lg:col-span-2 space-y-6">
          <div class="h-80 bg-white rounded-2xl animate-pulse" />
          <div class="h-32 bg-white rounded-2xl animate-pulse" />
        </div>
        <div class="lg:col-span-3 space-y-6">
          <div class="h-80 bg-white rounded-2xl animate-pulse" />
          <div class="h-64 bg-white rounded-2xl animate-pulse" />
        </div>
      </div>
    </template>

    <template v-else-if="overviewStore.stats">
      <!-- 1. Summary Cards -->
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-4">
        <SummaryCard
          title="Tổng học sinh"
          :value="overviewStore.stats.total_students"
          :icon="Users"
          color="#6b7280"
          @click="navigateToStudents()"
        />
        <SummaryCard
          title="Ổn định"
          :value="overviewStore.stats.stable_count"
          :icon="CheckCircle"
          color="#22c55e"
          @click="navigateToStudents('stable')"
        />
        <SummaryCard
          title="Theo dõi"
          :value="overviewStore.stats.watch_count"
          :icon="Eye"
          color="#eab308"
          @click="navigateToStudents('watch')"
        />
        <SummaryCard
          title="Cần xem xét"
          :value="overviewStore.stats.review_count"
          :icon="AlertTriangle"
          color="#f97316"
          @click="navigateToStudents('review')"
        />
        <SummaryCard
          title="Đang cải thiện"
          :value="overviewStore.stats.improving_count"
          :icon="TrendingUp"
          color="#3b82f6"
          @click="navigateToStudents('improving')"
        />
        <SummaryCard
          title="Chưa đủ dữ liệu"
          :value="overviewStore.stats.insufficient_count"
          :icon="HelpCircle"
          color="#9ca3af"
          @click="navigateToStudents('insufficient_data')"
        />
      </div>

      <!-- 2. Charts: Donut + Trend -->
      <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">
        <div class="lg:col-span-2">
          <AlertDistributionChart :stats="overviewStore.stats" />
        </div>
        <div class="lg:col-span-3">
          <TrendChart />
        </div>
      </div>

      <!-- 3. Signal Stats + Major Distribution -->
      <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">
        <div class="lg:col-span-2">
          <SignalStats />
        </div>
        <div class="lg:col-span-3">
          <MajorDistributionChart />
        </div>
      </div>

      <!-- 4. Priority Students -->
      <PriorityStudents @view-detail="viewDetail" />

      <!-- 5. Recent Changes Table -->
      <RecentChangesTable
        :students="overviewStore.recentChanges"
        :loading="overviewStore.loading"
        @view-detail="viewDetail"
      />
    </template>
  </div>
</template>
