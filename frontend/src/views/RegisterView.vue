<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { Mail, Lock, User, UserPlus, Eye, EyeOff } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const localError = ref('')

async function handleRegister() {
  localError.value = ''

  if (!name.value || !email.value || !password.value) {
    localError.value = 'Vui lòng nhập đầy đủ thông tin'
    return
  }
  if (password.value !== confirmPassword.value) {
    localError.value = 'Mật khẩu xác nhận không khớp'
    return
  }
  if (password.value.length < 6) {
    localError.value = 'Mật khẩu phải có ít nhất 6 ký tự'
    return
  }

  const ok = await authStore.register(name.value, email.value, password.value)
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
        <p class="text-sm text-gray-500 mt-1">Tạo tài khoản giáo viên mới</p>
      </div>

      <!-- Register Card -->
      <div class="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
        <h2 class="text-lg font-semibold text-gray-900 mb-1">Đăng ký</h2>
        <p class="text-sm text-gray-500 mb-6">Nhập thông tin để tạo tài khoản</p>

        <!-- Error -->
        <div
          v-if="authStore.error || localError"
          class="mb-4 p-3 rounded-xl bg-red-50 border border-red-200 text-sm text-red-600"
        >
          {{ localError || authStore.error }}
        </div>

        <form @submit.prevent="handleRegister" class="space-y-4">
          <!-- Name -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Họ và tên</label>
            <div class="relative">
              <User class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" :size="18" />
              <input
                v-model="name"
                type="text"
                placeholder="Nguyễn Văn A"
                required
                class="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-300 text-sm
                       focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                       placeholder-gray-400 transition"
              />
            </div>
          </div>

          <!-- Email -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Email</label>
            <div class="relative">
              <Mail class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" :size="18" />
              <input
                v-model="email"
                type="email"
                placeholder="giao@aegis.ai"
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
                placeholder="Ít nhất 6 ký tự"
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

          <!-- Confirm Password -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Xác nhận mật khẩu</label>
            <div class="relative">
              <Lock class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" :size="18" />
              <input
                v-model="confirmPassword"
                type="password"
                placeholder="Nhập lại mật khẩu"
                required
                class="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-300 text-sm
                       focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
                       placeholder-gray-400 transition"
              />
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
              Đang tạo tài khoản...
            </template>
            <template v-else>
              <UserPlus :size="18" />
              Đăng ký
            </template>
          </button>
        </form>

        <!-- Login link -->
        <p class="mt-6 text-center text-sm text-gray-500">
          Đã có tài khoản?
          <router-link to="/login" class="text-blue-600 font-medium hover:text-blue-700 transition">
            Đăng nhập
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>
