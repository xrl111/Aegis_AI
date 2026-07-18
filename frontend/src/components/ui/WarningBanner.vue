<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { AlertTriangle, X } from 'lucide-vue-next'
import { useOverviewStore } from '@/stores/overviewStore'

const router = useRouter()
const overviewStore = useOverviewStore()
const dismissed = ref(false)

watch(
  () => overviewStore.stats,
  () => { dismissed.value = false },
)

function goToReview() {
  dismissed.value = true
  router.push({ path: '/students', query: { level: 'review' } })
}

function goToWatch() {
  dismissed.value = true
  router.push({ path: '/students', query: { level: 'watch' } })
}
</script>

<template>
  <Transition
    enter-active-class="transition-all duration-300 ease-out"
    enter-from-class="opacity-0 -translate-y-2 max-h-0"
    enter-to-class="opacity-100 translate-y-0 max-h-24"
    leave-active-class="transition-all duration-200 ease-in"
    leave-from-class="opacity-100 translate-y-0 max-h-24"
    leave-to-class="opacity-0 -translate-y-2 max-h-0"
  >
    <div
      v-if="
        !dismissed &&
        overviewStore.stats &&
        (overviewStore.stats.review_count > 0 || overviewStore.stats.watch_count > 0)
      "
      class="overflow-hidden"
    >
      <div
        class="flex items-center gap-3 rounded-xl border px-4 py-3"
        :class="
          overviewStore.stats.review_count > 0
            ? 'bg-orange-50 border-orange-200'
            : 'bg-yellow-50 border-yellow-200'
        "
      >
        <AlertTriangle
          :size="18"
          class="flex-shrink-0"
          :class="overviewStore.stats.review_count > 0 ? 'text-orange-500' : 'text-yellow-500'"
        />

        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-800">
            <template v-if="overviewStore.stats.review_count > 0">
              <button
                @click="goToReview"
                class="font-semibold underline underline-offset-2 hover:text-orange-600 transition-colors"
              >
                {{ overviewStore.stats.review_count }} học sinh cần giáo viên xem xét
              </button>
            </template>
            <template v-if="overviewStore.stats.review_count > 0 && overviewStore.stats.watch_count > 0">
              <span class="text-gray-400 mx-1">·</span>
            </template>
            <template v-if="overviewStore.stats.watch_count > 0">
              <button
                @click="goToWatch"
                class="font-semibold underline underline-offset-2 hover:text-yellow-600 transition-colors"
              >
                {{ overviewStore.stats.watch_count }} học sinh cần theo dõi
              </button>
            </template>
          </p>
        </div>

        <button
          @click="dismissed = true"
          class="flex-shrink-0 p-1 rounded-lg hover:bg-white/60 transition-colors"
          title="Đã biết"
        >
          <X :size="16" class="text-gray-400" />
        </button>
      </div>
    </div>
  </Transition>
</template>
