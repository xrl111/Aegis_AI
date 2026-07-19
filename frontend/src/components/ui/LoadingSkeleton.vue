<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    type: 'card' | 'row' | 'text' | 'chart'
    count?: number
  }>(),
  { count: 3 },
)

const items = computed(() => Array.from({ length: props.count }))

const shimmerClass =
  'bg-gradient-to-r from-gray-200 via-gray-100 to-gray-200 bg-[length:200%_100%] animate-shimmer'
</script>

<template>
  <div class="flex flex-col gap-3">
    <template v-for="(_, index) in items" :key="index">
      <!-- Card skeleton -->
      <div v-if="type === 'card'" :class="[shimmerClass, 'h-24 w-full rounded-2xl']" />

      <!-- Row skeleton -->
      <div v-else-if="type === 'row'" :class="[shimmerClass, 'h-14 w-full rounded-lg']" />

      <!-- Text skeleton (3 lines) -->
      <div v-else-if="type === 'text'" class="flex flex-col gap-2">
        <div :class="[shimmerClass, 'h-4 w-full rounded']" />
        <div :class="[shimmerClass, 'h-4 w-4/5 rounded']" />
        <div :class="[shimmerClass, 'h-4 w-3/5 rounded']" />
      </div>

      <!-- Chart skeleton -->
      <div v-else-if="type === 'chart'" :class="[shimmerClass, 'h-64 w-full rounded-2xl']" />
    </template>
  </div>
</template>
