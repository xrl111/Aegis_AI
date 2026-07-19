<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { Mail, Lock, LogIn, Eye, EyeOff } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const showPassword = ref(false)

async function handleLogin() {
  if (!email.value || !password.value) return
  const ok = await authStore.login(email.value, password.value)
  if (ok) router.push('/')
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-slate-50 flex items-center justify-center p-4">
    <div class="w-full max-w-md animate-fade-in">
      <!-- Logo -->
      <div class="text-center mb-8">
        <img src="/logo.svg" alt="Aegis AI" class="w-16 h-16 mb-4" />
        <h1 class="text-2xl font-bold text-gray-900">Aegis AI</h1>
        <p class="text-sm text-gray-500 mt-1">Hệ thống Cảnh báo sớm học sinh</p>
      </div>

      <!-- Login Card -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
        <h2 class="text-lg font-semibold text-gray-900 mb-1">Đăng nhập</h2>
        <p class="text-sm text-gray-500 mb-6">Nhập thông tin tài khoản để truy cập hệ thống</p>

        <!-- Error -->
        <div
          v-if="authStore.error"
          class="mb-4 p-3 rounded-xl bg-red-50 border border-red-200 text-sm text-red-600"
        >
          {{ authStore.error }}
        </div>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <!-- Email -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Email</label>
            <div class="relative">
              <Mail class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" :size="18" />
              <input
                v-model="email"
                type="email"
                placeholder="admin@aegis.ai"
                required
                class="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-300 text-sm
                       focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                       placeholder-gray-400 transition"
              />
            </div>
          </div>

          <!-- Password -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Mật khẩu</label>
            <div class="relative">
              <Lock class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" :size="18" />
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Nhập mật khẩu"
                required
                class="w-full pl-10 pr-10 py-2.5 rounded-xl border border-gray-300 text-sm
                       focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                       placeholder-gray-400 transition"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <EyeOff v-if="showPassword" :size="18" />
                <Eye v-else :size="18" />
              </button>
            </div>
          </div>

          <!-- Submit -->
          <button
            type="submit"
            :disabled="authStore.loading"
            class="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl bg-blue-600
                   text-white text-sm font-medium hover:bg-blue-700 transition
                   disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <template v-if="authStore.loading">
              <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Đang đăng nhập...
            </template>
            <template v-else>
              <LogIn :size="18" />
              Đăng nhập
            </template>
          </button>
        </form>

        <!-- Register link -->
        <p class="mt-6 text-center text-sm text-gray-500">
          Chưa có tài khoản?
          <router-link to="/register" class="text-blue-600 font-medium hover:text-blue-700 transition">
            Đăng ký ngay
          </router-link>
        </p>
      </div>

      <!-- Demo hint -->
      <div class="mt-4 text-center text-xs text-gray-400">
        Demo: <span class="font-mono">admin@aegis.ai</span> / <span class="font-mono">123456</span>
      </div>
    </div>
  </div>
</template>
