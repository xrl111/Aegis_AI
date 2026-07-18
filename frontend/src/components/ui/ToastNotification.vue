<script setup lang="ts">
import { computed } from 'vue'
import { CheckCircle, XCircle, Info, AlertTriangle, X } from 'lucide-vue-next'

const props = defineProps<{
  type: 'success' | 'error' | 'info' | 'warning'
  message: string
  show: boolean
}>()

defineEmits<{
  close: []
}>()

const config = computed(() => {
  switch (props.type) {
    case 'success':
      return {
        bg: 'bg-green-50 border-green-200 text-green-800',
        icon: CheckCircle,
        iconColor: 'text-green-500',
      }
    case 'error':
      return {
        bg: 'bg-red-50 border-red-200 text-red-800',
        icon: XCircle,
        iconColor: 'text-red-500',
      }
    case 'warning':
      return {
        bg: 'bg-orange-50 border-orange-200 text-orange-800',
        icon: AlertTriangle,
        iconColor: 'text-orange-500',
      }
    case 'info':
      return {
        bg: 'bg-blue-50 border-blue-200 text-blue-800',
        icon: Info,
        iconColor: 'text-blue-500',
      }
  }
})
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="translate-y-4 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="translate-y-4 opacity-0"
    >
      <div
        v-if="show"
        class="fixed bottom-6 right-6 z-50 flex items-center gap-3 rounded-xl border px-4 py-3 shadow-lg"
        :class="config.bg"
      >
        <component :is="config.icon" :size="18" :class="config.iconColor" />
        <span class="text-sm font-medium">{{ message }}</span>
        <button
          class="ml-2 rounded p-0.5 opacity-60 transition-opacity hover:opacity-100"
          @click="$emit('close')"
        >
          <X :size="14" />
        </button>
      </div>
    </Transition>
  </Teleport>
</template>
