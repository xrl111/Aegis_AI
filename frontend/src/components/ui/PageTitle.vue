<script setup lang="ts">
import { ArrowLeft } from 'lucide-vue-next'

defineProps<{
  title: string
  subtitle?: string
  backTo?: string
}>()
</script>

<template>
  <div class="flex items-center gap-3">
    <router-link
      v-if="backTo"
      :to="backTo"
      class="flex h-8 w-8 items-center justify-center rounded-lg text-gray-400 transition-colors hover:bg-gray-100 hover:text-gray-600"
    >
      <ArrowLeft :size="18" />
    </router-link>

    <div>
      <h1 class="text-2xl font-semibold tracking-tight text-gray-900">{{ title }}</h1>
      <p v-if="subtitle" class="mt-0.5 text-sm text-gray-500">{{ subtitle }}</p>
    </div>
  </div>
</template>
