import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { FeedbackRequest, FeedbackResponse } from '@/types'
import { submitFeedback } from '@/services/api'

export const useFeedbackStore = defineStore('feedback', () => {
  const submitting = ref(false)
  const lastResult = ref<FeedbackResponse | null>(null)

  async function submit(request: FeedbackRequest) {
    submitting.value = true
    lastResult.value = null
    try {
      if (import.meta.env.VITE_USE_MOCK === 'true') {
        await new Promise((r) => setTimeout(r, 800))
        lastResult.value = { success: true, message: 'Đã lưu phản hồi thành công' }
      } else {
        lastResult.value = await submitFeedback(request)
      }
      return lastResult.value
    } finally {
      submitting.value = false
    }
  }

  return { submitting, lastResult, submit }
})
