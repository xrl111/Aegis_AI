import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { StudentSummary, StudentDetail, AlertLevel } from '@/types'
import { fetchStudents, fetchStudentDetail } from '@/services/api'
import { mockStudents, mockStudentDetail } from '@/services/mock'

const USE_MOCK = false

export interface StudentFilters {
  search: string
  levels: AlertLevel[]
  major: string
  sort: 'asc' | 'desc'
}

export const useStudentStore = defineStore('student', () => {
  const students = ref<StudentSummary[]>([])
  const currentStudent = ref<StudentDetail | null>(null)
  const loading = ref(false)
  const detailLoading = ref(false)
  const error = ref<string | null>(null)

  const filters = ref<StudentFilters>({
    search: '',
    levels: [],
    major: '',
    sort: 'desc',
  })

  const majors = computed(() => {
    const set = new Set(students.value.map((s) => s.major))
    return Array.from(set).sort()
  })

  const filteredStudents = computed(() => {
    let result = [...students.value]

    if (filters.value.search) {
      const q = filters.value.search.toLowerCase()
      result = result.filter(
        (s) =>
          s.student_name.toLowerCase().includes(q) ||
          s.student_id.toLowerCase().includes(q)
      )
    }

    if (filters.value.levels.length > 0) {
      result = result.filter((s) => filters.value.levels.includes(s.alert_level))
    }

    if (filters.value.major) {
      result = result.filter((s) => s.major === filters.value.major)
    }

    result.sort((a, b) => {
      if (!a.updated_at) return 1
      if (!b.updated_at) return -1
      const diff = new Date(a.updated_at).getTime() - new Date(b.updated_at).getTime()
      return filters.value.sort === 'desc' ? -diff : diff
    })

    return result
  })

  async function fetchAll() {
    loading.value = true
    error.value = null
    try {
      if (USE_MOCK) {
        students.value = mockStudents
      } else {
        students.value = await fetchStudents()
      }
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Không thể tải danh sách học sinh'
    } finally {
      loading.value = false
    }
  }

  async function fetchDetail(id: string) {
    detailLoading.value = true
    error.value = null
    try {
      if (USE_MOCK) {
        const found = mockStudents.find((s) => s.student_id === id)
        if (found) {
          currentStudent.value = {
            ...mockStudentDetail,
            student_id: found.student_id,
            student_name: found.student_name,
            major: found.major,
            alert_level: found.alert_level,
            headline: found.headline,
          }
        } else {
          currentStudent.value = null
        }
      } else {
        currentStudent.value = await fetchStudentDetail(id)
      }
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'Không thể tải thông tin học sinh'
      currentStudent.value = null
    } finally {
      detailLoading.value = false
    }
  }

  return {
    students,
    currentStudent,
    loading,
    detailLoading,
    error,
    filters,
    majors,
    filteredStudents,
    fetchAll,
    fetchDetail,
  }
})
