<script setup lang="ts">
import { Sun, Moon, Menu, LogOut } from 'lucide-vue-next'
import { useTheme } from '@/composables/useTheme'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'
import { computed } from 'vue'
import { getInitials } from '@/utils/format'
import NotificationDropdown from '@/components/ui/NotificationDropdown.vue'

defineProps<{
  title: string
}>()

const emit = defineEmits<{
  toggleSidebar: []
}>()

const { isDark, toggleDark } = useTheme()
const authStore = useAuthStore()
const router = useRouter()

const userName = computed(() => authStore.user?.name || 'Giáo viên')
const userInitials = computed(() => getInitials(userName.value))

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <header
    class="sticky top-0 z-30 flex h-16 items-center border-b border-gray-200 bg-white/80 px-6 backdrop-blur-lg"
  >
    <div class="flex w-full items-center justify-between">
      <!-- Left: hamburger + title -->
      <div class="flex items-center gap-3">
        <!-- Mobile hamburger -->
        <button
          type="button"
          class="inline-flex h-9 w-9 items-center justify-center rounded-lg text-gray-500 transition-colors hover:bg-gray-100 hover:text-gray-700 lg:hidden"
          @click="emit('toggleSidebar')"
        >
          <Menu class="h-5 w-5" :stroke-width="2" />
        </button>
        <h1 class="text-lg font-semibold text-gray-900">{{ title }}</h1>
      </div>

      <!-- Right: actions -->
      <div class="flex items-center gap-1">
        <!-- Notification bell with dropdown -->
        <NotificationDropdown />

        <!-- Dark mode toggle -->
        <button
          type="button"
          class="inline-flex h-9 w-9 items-center justify-center rounded-lg text-gray-500 transition-colors hover:bg-gray-100 hover:text-gray-700"
          :aria-label="isDark ? 'Chế độ sáng' : 'Chế độ tối'"
          @click="toggleDark()"
        >
          <Moon v-if="!isDark" class="h-[18px] w-[18px]" :stroke-width="2" />
          <Sun v-else class="h-[18px] w-[18px]" :stroke-width="2" />
        </button>

        <!-- Divider -->
        <div class="mx-2 hidden h-6 w-px bg-gray-200 sm:block" />

        <!-- Teacher avatar + name -->
        <div class="flex items-center gap-2.5 pl-1">
          <div
            class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-600 text-xs font-semibold text-white"
          >
            {{ userInitials }}
          </div>
          <span class="hidden text-sm font-medium text-gray-700 sm:inline">
            {{ userName }}
          </span>
        </div>

        <!-- Logout -->
        <button
          type="button"
          class="inline-flex h-9 w-9 items-center justify-center rounded-lg text-gray-500 transition-colors hover:bg-red-50 hover:text-red-600"
          title="Đăng xuất"
          @click="handleLogout"
        >
          <LogOut class="h-[18px] w-[18px]" :stroke-width="2" />
        </button>
      </div>
    </div>
  </header>
</template>
