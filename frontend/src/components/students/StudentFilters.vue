<script setup lang="ts">
import { ref, computed } from 'vue'
import { Search, ArrowUpDown, ChevronDown, X } from 'lucide-vue-next'
import { useStudentStore } from '@/stores/studentStore'
import { ALERT_CONFIG } from '@/utils/constants'
import type { AlertLevel } from '@/types'

const store = useStudentStore()

const showLevelDropdown = ref(false)
const showMajorDropdown = ref(false)

const allLevels: AlertLevel[] = ['stable', 'watch', 'review', 'improving', 'insufficient_data']

const selectedLevelCount = computed(() => store.filters.levels.length)

function toggleLevel(level: AlertLevel) {
  const idx = store.filters.levels.indexOf(level)
  if (idx === -1) {
    store.filters.levels.push(level)
  } else {
    store.filters.levels.splice(idx, 1)
  }
}

function selectMajor(major: string) {
  store.filters.major = major
  showMajorDropdown.value = false
}

function toggleSort() {
  store.filters.sort = store.filters.sort === 'asc' ? 'desc' : 'asc'
}

function closeLevelDropdown() {
  showLevelDropdown.value = false
}

function closeMajorDropdown() {
  showMajorDropdown.value = false
}
</script>

<template>
  <div class="flex flex-wrap items-center gap-3">
    <!-- Search input -->
    <div class="relative flex-1 min-w-[200px] max-w-md">
      <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" :size="18" />
      <input
        v-model="store.filters.search"
        type="text"
        placeholder="Tìm kiếm theo tên..."
        class="w-full pl-10 pr-4 py-2 rounded-xl border border-gray-300 bg-white text-sm
               focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
               placeholder-gray-400 transition"
      />
      <button
        v-if="store.filters.search"
        @click="store.filters.search = ''"
        class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
      >
        <X :size="16" />
      </button>
    </div>

    <!-- Alert Level multi-select -->
    <div class="relative">
      <button
        @click="showLevelDropdown = !showLevelDropdown; showMajorDropdown = false"
        class="flex items-center gap-2 px-4 py-2 rounded-xl border border-gray-300 bg-white
               text-sm font-medium text-gray-700 hover:bg-gray-50 transition focus:outline-none
               focus:ring-2 focus:ring-blue-500"
      >
        <span>Mức cảnh báo</span>
        <span
          v-if="selectedLevelCount > 0"
          class="inline-flex items-center justify-center w-5 h-5 rounded-full bg-blue-500 text-white text-xs font-bold"
        >
          {{ selectedLevelCount }}
        </span>
        <ChevronDown :size="16" class="text-gray-400" />
      </button>

      <!-- Level dropdown -->
      <div
        v-if="showLevelDropdown"
        class="absolute z-50 mt-2 w-64 bg-white rounded-xl border border-gray-200 shadow-lg py-2"
      >
        <div class="px-3 py-1 text-xs font-medium text-gray-400 uppercase">Chọn mức cảnh báo</div>
        <button
          v-for="level in allLevels"
          :key="level"
          @click="toggleLevel(level)"
          class="w-full flex items-center gap-3 px-3 py-2 text-sm text-gray-700 hover:bg-gray-50 transition"
        >
          <div
            class="w-4 h-4 rounded border-2 flex items-center justify-center flex-shrink-0 transition"
            :class="store.filters.levels.includes(level)
              ? 'border-blue-500 bg-blue-500'
              : 'border-gray-300'"
          >
            <svg
              v-if="store.filters.levels.includes(level)"
              class="w-3 h-3 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="3"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <span
            class="w-2.5 h-2.5 rounded-full flex-shrink-0"
            :style="{ backgroundColor: ALERT_CONFIG[level].color }"
          />
          <span>{{ ALERT_CONFIG[level].label }}</span>
        </button>
      </div>
    </div>

    <!-- Major single-select -->
    <div class="relative">
      <button
        @click="showMajorDropdown = !showMajorDropdown; showLevelDropdown = false"
        class="flex items-center gap-2 px-4 py-2 rounded-xl border border-gray-300 bg-white
               text-sm font-medium text-gray-700 hover:bg-gray-50 transition focus:outline-none
               focus:ring-2 focus:ring-blue-500"
      >
        <span>{{ store.filters.major || 'Tất cả ngành' }}</span>
        <ChevronDown :size="16" class="text-gray-400" />
      </button>

      <!-- Major dropdown -->
      <div
        v-if="showMajorDropdown"
        class="absolute z-50 mt-2 w-56 bg-white rounded-xl border border-gray-200 shadow-lg py-1 max-h-60 overflow-auto"
      >
        <button
          @click="selectMajor('')"
          class="w-full text-left px-4 py-2 text-sm transition"
          :class="!store.filters.major ? 'bg-blue-50 text-blue-600 font-medium' : 'text-gray-700 hover:bg-gray-50'"
        >
          Tất cả ngành
        </button>
        <button
          v-for="major in store.majors"
          :key="major"
          @click="selectMajor(major)"
          class="w-full text-left px-4 py-2 text-sm transition"
          :class="store.filters.major === major ? 'bg-blue-50 text-blue-600 font-medium' : 'text-gray-700 hover:bg-gray-50'"
        >
          {{ major }}
        </button>
      </div>
    </div>

    <!-- Sort toggle -->
    <button
      @click="toggleSort"
      class="flex items-center gap-2 px-4 py-2 rounded-xl border border-gray-300 bg-white
             text-sm font-medium text-gray-700 hover:bg-gray-50 transition focus:outline-none
             focus:ring-2 focus:ring-blue-500"
      :title="store.filters.sort === 'desc' ? 'Mới nhất lên đầu' : 'Cũ nhất lên đầu'"
    >
      <ArrowUpDown :size="16" />
      <span>{{ store.filters.sort === 'desc' ? 'Mới nhất' : 'Cũ nhất' }}</span>
    </button>
  </div>

  <!-- Click-outside overlay for dropdowns -->
  <Teleport to="body">
    <div
      v-if="showLevelDropdown || showMajorDropdown"
      class="fixed inset-0 z-40"
      @click.self="closeLevelDropdown(); closeMajorDropdown()"
    />
  </Teleport>
</template>
