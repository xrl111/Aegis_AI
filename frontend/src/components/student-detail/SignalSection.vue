<script setup lang="ts">
import { Inbox } from 'lucide-vue-next'
import type { SignalOut } from '@/types'
import SignalCard from './SignalCard.vue'

defineProps<{
  signals: SignalOut[]
}>()
</script>

<template>
  <div>
    <h2 class="text-lg font-semibold text-gray-900 mb-4">Các tín hiệu</h2>

    <template v-if="signals.length > 0">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <SignalCard
          v-for="signal in signals"
          :key="signal.signal_type"
          :signal="signal"
        />
      </div>
    </template>

    <template v-else>
      <div class="flex flex-col items-center justify-center py-12 text-gray-400">
        <Inbox :size="40" class="mb-3 opacity-50" />
        <p class="text-sm">Chưa có tín hiệu nào được ghi nhận.</p>
      </div>
    </template>
  </div>
</template>
