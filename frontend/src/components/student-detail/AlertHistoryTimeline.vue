<script setup lang="ts">
import { computed } from 'vue'
import { Inbox } from 'lucide-vue-next'
import type { AlertHistoryItem } from '@/types'
import { ALERT_CONFIG } from '@/utils/constants'
import { formatDate } from '@/utils/format'
import StatusBadge from '@/components/ui/StatusBadge.vue'

const props = defineProps<{
  history: AlertHistoryItem[]
}>()

// Newest on top
const sortedHistory = computed(() =>
  [...props.history].sort(
    (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime(),
  ),
)
</script>

<template>
  <div>
    <h2 class="text-lg font-semibold text-gray-900 mb-4">Lịch sử cảnh báo</h2>

    <template v-if="history.length > 0">
      <div class="relative pl-6">
        <!-- Vertical line -->
        <div
          class="absolute left-[5px] top-2 bottom-2 w-0.5 bg-gray-200"
          aria-hidden="true"
        />

        <div
          v-for="(item, index) in sortedHistory"
          :key="index"
          class="relative mb-6 last:mb-0"
        >
          <!-- Dot -->
          <div
            class="absolute -left-6 top-1.5 w-3 h-3 rounded-full border-2 border-white"
            :style="{ backgroundColor: ALERT_CONFIG[item.level].color }"
            :title="ALERT_CONFIG[item.level].label"
          />

          <!-- Content card -->
          <div class="bg-surface border border-border rounded-xl p-4 ml-2">
            <div class="flex items-center gap-2 mb-1">
              <span class="text-xs text-gray-400">{{ formatDate(item.date) }}</span>
              <StatusBadge :level="item.level" size="sm" />
            </div>

            <p class="text-sm font-medium text-gray-800 mb-1">{{ item.headline }}</p>

            <ul v-if="item.details.length > 0" class="mt-2 space-y-0.5">
              <li
                v-for="(detail, dIdx) in item.details"
                :key="dIdx"
                class="text-sm text-gray-600 list-disc ml-4"
              >
                {{ detail }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </template>

    <template v-else>
      <div class="flex flex-col items-center justify-center py-12 text-gray-400">
        <Inbox :size="40" class="mb-3 opacity-50" />
        <p class="text-sm">Chưa có lịch sử cảnh báo.</p>
      </div>
    </template>
  </div>
</template>
