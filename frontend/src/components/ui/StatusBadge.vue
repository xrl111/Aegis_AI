<script setup lang="ts">
import { computed } from 'vue'
import { ALERT_CONFIG } from '@/utils/constants'
import type { AlertLevel } from '@/types'

const props = withDefaults(
  defineProps<{
    level: AlertLevel
    size?: 'sm' | 'md'
  }>(),
  { size: 'md' },
)

const config = computed(() => ALERT_CONFIG[props.level])
const Icon = computed(() => config.value.icon)

const sizeClasses = computed(() =>
  props.size === 'sm'
    ? 'text-xs px-2 py-0.5 gap-1'
    : 'text-sm px-2.5 py-1 gap-1.5',
)

const iconSize = computed(() => (props.size === 'sm' ? 12 : 14))
</script>

<template>
  <span
    class="inline-flex items-center rounded-full font-medium leading-none"
    :class="sizeClasses"
    :style="{
      backgroundColor: config.bg,
      color: config.color,
    }"
  >
    <Icon :size="iconSize" />
    <span>{{ config.label }}</span>
  </span>
</template>
