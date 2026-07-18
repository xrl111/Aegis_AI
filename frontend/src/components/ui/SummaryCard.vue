<script setup lang="ts">
import { computed } from 'vue'
import type { Component } from 'vue'

const props = defineProps<{
  title: string
  value: number
  icon: Component
  color: string
  subtitle?: string
}>()

const emit = defineEmits<{
  click: []
}>()

const hasClick = computed(() => true)

const iconBg = computed(() => {
  // Convert hex color to rgba with ~10% opacity
  const hex = props.color.replace('#', '')
  const r = parseInt(hex.substring(0, 2), 16)
  const g = parseInt(hex.substring(2, 4), 16)
  const b = parseInt(hex.substring(4, 6), 16)
  return `rgba(${r}, ${g}, ${b}, 0.1)`
})
</script>

<template>
  <div
    class="rounded-2xl bg-white p-5 shadow-card transition-all duration-200 cursor-pointer hover:-translate-y-0.5 hover:shadow-card-hover"
    @click="emit('click')"
  >
    <div class="flex items-center gap-4">
      <div
        class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full"
        :style="{ backgroundColor: iconBg }"
      >
        <component :is="icon" :size="20" :style="{ color }" />
      </div>

      <div class="min-w-0">
        <div class="text-2xl font-bold text-gray-900">{{ value }}</div>
        <div class="text-sm text-gray-500">{{ title }}</div>
        <div v-if="subtitle" class="text-xs text-gray-400">{{ subtitle }}</div>
      </div>
    </div>
  </div>
</template>
