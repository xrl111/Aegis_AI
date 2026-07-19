<script setup lang="ts">
import { ref } from 'vue'
import { Phone, Users, PenLine, XCircle } from 'lucide-vue-next'
import type { ActionTaken } from '@/types'
import { ACTION_LABELS } from '@/utils/constants'
import { useFeedbackStore } from '@/stores/feedbackStore'
import ToastNotification from '@/components/ui/ToastNotification.vue'

const props = defineProps<{
  studentId: string
}>()

const feedbackStore = useFeedbackStore()

const selectedAction = ref<ActionTaken | null>(null)
const notes = ref('')
const toastMessage = ref('')
const toastType = ref<'success' | 'error'>('success')
const showToast = ref(false)

let toastTimer: ReturnType<typeof setTimeout> | null = null

function triggerToast(message: string, type: 'success' | 'error') {
  toastMessage.value = message
  toastType.value = type
  showToast.value = true
  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const actionOptions: { value: ActionTaken; icon: typeof Phone }[] = [
  { value: 'contacted', icon: Phone },
  { value: 'meeting', icon: Users },
  { value: 'noted', icon: PenLine },
  { value: 'dismissed', icon: XCircle },
]

function selectAction(action: ActionTaken) {
  selectedAction.value = action === selectedAction.value ? null : action
}

async function handleSubmit() {
  if (!selectedAction.value) return

  const result = await feedbackStore.submit({
    student_id: props.studentId,
    teacher_id: 'current-teacher',
    action_taken: selectedAction.value,
    notes: notes.value,
  })

  if (result?.success) {
    triggerToast(result.message || 'Đã lưu phản hồi thành công', 'success')
    selectedAction.value = null
    notes.value = ''
  } else {
    triggerToast(result?.message || 'Có lỗi xảy ra, vui lòng thử lại', 'error')
  }
}
</script>

<template>
  <div class="bg-surface rounded-2xl p-6 shadow-card">
    <h2 class="text-lg font-semibold text-gray-900 mb-4">Ghi nhận của giáo viên</h2>

    <!-- Toast -->
    <ToastNotification
      :show="showToast"
      :message="toastMessage"
      :type="toastType"
      @close="showToast = false"
    />

    <!-- Radio group as selectable cards -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-4">
      <button
        v-for="option in actionOptions"
        :key="option.value"
        type="button"
        class="flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all text-sm font-medium cursor-pointer"
        :class="
          selectedAction === option.value
            ? 'border-blue-500 bg-blue-50 text-blue-700'
            : 'border-gray-200 hover:border-gray-300 text-gray-600 bg-surface'
        "
        @click="selectAction(option.value)"
      >
        <component :is="option.icon" :size="20" />
        <span>{{ ACTION_LABELS[option.value] }}</span>
      </button>
    </div>

    <!-- Notes textarea -->
    <textarea
      v-model="notes"
      placeholder="Nhập ghi chú..."
      class="w-full px-4 py-3 rounded-xl border border-border text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none transition-colors"
      style="min-height: 80px;"
    />

    <!-- Submit button -->
    <div class="mt-4 flex justify-end">
      <button
        type="button"
        :disabled="!selectedAction || feedbackStore.submitting"
        class="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl text-sm font-medium text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        :class="
          selectedAction && !feedbackStore.submitting
            ? 'bg-blue-600 hover:bg-blue-700'
            : 'bg-blue-600'
        "
        @click="handleSubmit"
      >
        <svg
          v-if="feedbackStore.submitting"
          class="animate-spin h-4 w-4"
          viewBox="0 0 24 24"
          fill="none"
        >
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
        {{ feedbackStore.submitting ? 'Đang lưu...' : 'Lưu phản hồi' }}
      </button>
    </div>
  </div>
</template>
