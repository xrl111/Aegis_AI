import {
  CheckCircle,
  Eye,
  AlertTriangle,
  TrendingUp,
  HelpCircle,
  BookOpen,
  ClipboardList,
  FileText,
} from 'lucide-vue-next'
import type { AlertLevel, ActionTaken } from '@/types'
import type { Component } from 'vue'

export interface AlertConfig {
  color: string
  bg: string
  bgDark: string
  border: string
  label: string
  icon: Component
}

export const ALERT_CONFIG: Record<AlertLevel, AlertConfig> = {
  stable: {
    color: '#22c55e',
    bg: '#f0fdf4',
    bgDark: '#14532d',
    border: '#bbf7d0',
    label: 'Ổn định',
    icon: CheckCircle,
  },
  watch: {
    color: '#eab308',
    bg: '#fefce8',
    bgDark: '#713f12',
    border: '#fef08a',
    label: 'Theo dõi thay đổi',
    icon: Eye,
  },
  review: {
    color: '#f97316',
    bg: '#fff7ed',
    bgDark: '#7c2d12',
    border: '#fed7aa',
    label: 'Cần giáo viên xem xét',
    icon: AlertTriangle,
  },
  improving: {
    color: '#3b82f6',
    bg: '#eff6ff',
    bgDark: '#1e3a5f',
    border: '#bfdbfe',
    label: 'Đang cải thiện',
    icon: TrendingUp,
  },
  insufficient_data: {
    color: '#9ca3af',
    bg: '#f9fafb',
    bgDark: '#374151',
    border: '#e5e7eb',
    label: 'Chưa đủ dữ liệu',
    icon: HelpCircle,
  },
}

export const SIGNAL_ICONS: Record<string, Component> = {
  grade: BookOpen,
  attendance: ClipboardList,
  submission: FileText,
}

export const SIGNAL_LABELS: Record<string, string> = {
  grade: 'Điểm học tập',
  attendance: 'Điểm danh',
  submission: 'Nộp bài',
}

export const ACTION_LABELS: Record<ActionTaken, string> = {
  contacted: 'Đã liên hệ',
  meeting: 'Đã gặp',
  noted: 'Đã ghi chú',
  dismissed: 'Không cần xử lý',
}
