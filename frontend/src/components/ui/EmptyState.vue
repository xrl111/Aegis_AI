<script setup lang="ts">
import type { Component } from 'vue'

defineProps<{
  icon?: Component
  title: string
  description?: string
  actionLabel?: string
}>()

const emit = defineEmits<{
  action: []
}>()
</script>

<template>
  <div class="flex flex-col items-center py-12 text-center">
    <component
      v-if="icon"
      :is="icon"
      :size="48"
      class="mb-4 text-gray-300"
    />

    <h3 class="text-lg font-medium text-gray-600">{{ title }}</h3>

    <p v-if="description" class="mt-2 max-w-sm text-sm text-gray-400">
      {{ description }}
    </p>

    <button
      v-if="actionLabel"
      class="mt-6 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      @click="emit('action')"
    >
      {{ actionLabel }}
    </button>
  </div>
</template>
