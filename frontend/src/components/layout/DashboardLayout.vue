<script setup lang="ts">
import { ref, provide } from 'vue'
import AppSidebar from './AppSidebar.vue'
import AppHeader from './AppHeader.vue'
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const sidebarOpen = ref(false)
provide('sidebarOpen', sidebarOpen)

const route = useRoute()

const pageTitle = computed(() => {
  if (route.path === '/') return 'Tổng quan'
  if (route.path === '/students') return 'Danh sách học sinh'
  if (route.path.startsWith('/students/')) return 'Chi tiết học sinh'
  return 'Aegis AI'
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Sidebar -->
    <AppSidebar :is-open="sidebarOpen" @close="sidebarOpen = false" />

    <!-- Main content area -->
    <div class="transition-all duration-300 lg:ml-64">
      <!-- Header -->
      <AppHeader :title="pageTitle" @toggle-sidebar="sidebarOpen = !sidebarOpen" />

      <!-- Page content -->
      <main class="p-4 sm:p-6">
        <RouterView />
      </main>
    </div>
  </div>
</template>
