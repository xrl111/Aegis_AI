import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { OverviewStats, StudentSummary } from '@/types'
import { fetchOverviewStats, fetchStudents } from '@/services/api'
import { mockStats, mockStudents } from '@/services/mock'

const USE_MOCK = true

export const useOverviewStore = defineStore('overview', () => {
  const stats = ref<OverviewStats | null>(null)
  const recentChanges = ref<StudentSummary[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchStats() {
    loading.value = true
    error.value = null
    try {
      if (USE_MOCK) {
        stats.value = mockStats
      } else {
        stats.value = await fetchOverviewStats()
      }
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Không thể tải dữ liệu tổng quan'
    } finally {
      loading.value = false
    }
  }

  async function fetchRecentChanges() {
    loading.value = true
    error.value = null
    try {
      if (USE_MOCK) {
        recentChanges.value = [...mockStudents]
          .sort((a, b) => {
            if (!a.updated_at) return 1
            if (!b.updated_at) return -1
            return new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
          })
          .slice(0, 10)
      } else {
        const all = await fetchStudents()
        recentChanges.value = all
          .sort((a, b) => {
            if (!a.updated_at) return 1
            if (!b.updated_at) return -1
            return new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
          })
          .slice(0, 10)
      }
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Không thể tải danh sách thay đổi'
    } finally {
      loading.value = false
    }
  }

  return { stats, recentChanges, loading, error, fetchStats, fetchRecentChanges }
})
