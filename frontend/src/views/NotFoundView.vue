<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Home, ArrowLeft } from 'lucide-vue-next'

const router = useRouter()
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-slate-50 flex items-center justify-center p-4">
    <div class="text-center animate-fade-in">
      <div class="text-[120px] font-bold text-gray-200 leading-none select-none">404</div>
      <h1 class="text-xl font-semibold text-gray-900 -mt-4">Trang không tồn tại</h1>
      <p class="text-sm text-gray-500 mt-2 max-w-sm mx-auto">
        Trang bạn tìm kiếm có thể đã bị di chuyển hoặc không còn tồn tại.
      </p>
      <div class="flex items-center justify-center gap-3 mt-6">
        <button
          @click="router.back()"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-xl border border-gray-300 text-sm font-medium text-gray-700 hover:bg-gray-50 transition"
        >
          <ArrowLeft :size="16" />
          Quay lại
        </button>
        <router-link
          to="/"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-600 text-sm font-medium text-white hover:bg-blue-700 transition"
        >
          <Home :size="16" />
          Về trang chủ
        </router-link>
      </div>
    </div>
  </div>
</template>
