export type AlertLevel =
  | 'insufficient_data'
  | 'stable'
  | 'watch'
  | 'review'
  | 'improving'

export type SignalType = 'grade' | 'attendance' | 'submission'

export type DataSufficiency = 'sufficient' | 'partial' | 'insufficient'

export type ActionTaken = 'contacted' | 'meeting' | 'noted' | 'dismissed'

export interface OverviewStats {
  total_students: number
  stable_count: number
  watch_count: number
  review_count: number
  insufficient_count: number
  improving_count: number
}

export interface StudentSummary {
  student_id: string
  student_name: string
  major: string
  alert_level: AlertLevel
  headline: string
  triggered_signal_count: number
  updated_at: string | null
}

export interface SignalOut {
  signal_type: SignalType
  is_triggered: boolean
  data_sufficiency: DataSufficiency
  explanation: string
}

export interface TimelinePoint {
  week: string
  grade_value: number | null
  attendance_value: number | null
  submission_value: number | null
}

export interface AlertHistoryItem {
  date: string
  level: AlertLevel
  headline: string
  details: string[]
}

export interface ComponentGrade {
  assessment: string
  score: number
  class_average: number
}

export interface CourseDetail {
  course_id: string
  course_name: string
  semester: number
  grades: ComponentGrade[]
  attendance_rate: number
}

export interface StudentDetail {
  student_id: string
  student_name: string
  major: string
  cgpa: number
  total_credits: number
  alert_level: AlertLevel
  headline: string
  signals: SignalOut[]
  timeline: TimelinePoint[]
  courses: CourseDetail[]
  alert_history: AlertHistoryItem[]
  is_seasonal_suppressed: boolean
}

export interface FeedbackRequest {
  student_id: string
  teacher_id: string
  action_taken: ActionTaken
  notes: string
}

export interface FeedbackResponse {
  success: boolean
  message: string
}
