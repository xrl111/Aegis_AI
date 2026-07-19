<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Shield, LayoutDashboard, Users, User } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/authStore'

defineProps<{
  isOpen: boolean
}>()

const emit = defineEmits<{
  close: []
}>()

const route = useRoute()
const authStore = useAuthStore()

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Tổng quan' },
  { to: '/students', icon: Users, label: 'Học sinh' },
]

function isActive(to: string): boolean {
  if (to === '/') return route.path === '/'
  return route.path.startsWith(to)
}
</script>

<template>
  <!-- Mobile backdrop -->
  <Transition name="fade">
    <div
      v-if="isOpen"
      class="fixed inset-0 z-40 bg-black/40 lg:hidden"
      @click="emit('close')"
    />
  </Transition>

  <!-- Sidebar -->
  <aside
    :class="[
      'fixed top-0 left-0 z-50 flex h-full w-64 flex-col border-r border-gray-200 bg-white transition-transform duration-300 ease-in-out',
      isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0',
    ]"
  >
    <!-- Logo -->
    <div class="flex items-center gap-3 px-6 py-5">
      <div class="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-600">
        <Shield class="h-5 w-5 text-white" :stroke-width="2.2" />
      </div>
      <div>
        <h1 class="text-base font-bold tracking-tight text-gray-900">Aegis AI</h1>
        <p class="text-xs text-gray-400">Cảnh báo sớm học sinh</p>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="mt-2 flex-1 space-y-1 px-3">
      <router-link
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        @click="emit('close')"
        :class="[
          'group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-all duration-150',
          isActive(item.to)
            ? 'border-l-[3px] border-blue-600 bg-blue-50 pl-[21px] text-blue-600'
            : 'border-l-[3px] border-transparent text-gray-600 hover:bg-gray-50 hover:text-gray-900',
        ]"
      >
        <component
          :is="item.icon"
          :class="[
            'h-[18px] w-[18px] shrink-0',
            isActive(item.to) ? 'text-blue-600' : 'text-gray-400 group-hover:text-gray-600',
          ]"
          :stroke-width="2"
        />
        <span>{{ item.label }}</span>
      </router-link>
    </nav>

    <!-- User info -->
    <div class="border-t border-gray-100 px-4 py-4">
      <div class="flex items-center gap-3 rounded-xl px-3 py-2">
        <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-gray-100">
          <User class="h-4 w-4 text-gray-500" :stroke-width="2" />
        </div>
        <div class="min-w-0 flex-1">
          <p class="truncate text-sm font-medium text-gray-700">{{ authStore.user?.role || 'Giáo viên' }}</p>
          <p class="truncate text-xs text-gray-400">{{ authStore.user?.name || 'Chưa đăng nhập' }}</p>
        </div>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
