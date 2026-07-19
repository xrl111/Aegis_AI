import axios from 'axios'
import type {
  OverviewStats,
  StudentSummary,
  StudentDetail,
  FeedbackRequest,
  FeedbackResponse,
} from '@/types'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

export async function fetchOverviewStats(): Promise<OverviewStats> {
  const res = await api.get<OverviewStats>('/overview/stats')
  return res.data
}

export async function fetchStudents(): Promise<StudentSummary[]> {
  const res = await api.get<StudentSummary[]>('/students')
  return res.data
}

export async function fetchStudentDetail(id: string): Promise<StudentDetail> {
  const res = await api.get<StudentDetail>(`/students/${id}`)
  return res.data
}

export async function submitFeedback(
  request: FeedbackRequest
): Promise<FeedbackResponse> {
  const res = await api.post<FeedbackResponse>('/feedback', request)
  return res.data
}

export async function fetchFeedbackHistory(
  studentId: string
): Promise<FeedbackRequest[]> {
  const res = await api.get<FeedbackRequest[]>(`/feedback/${studentId}`)
  return res.data
}
