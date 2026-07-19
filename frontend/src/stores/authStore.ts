import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export interface User {
  id: string
  name: string
  email: string
  role: string
  avatar?: string
}

const MOCK_USERS: Record<string, { password: string; user: User }> = {
  'admin@aegis.ai': {
    password: '123456',
    user: {
      id: 'T001',
      name: 'Admin',
      email: 'admin@aegis.ai',
      role: 'Giáo viên',
    },
  },
  'giao@aegis.ai': {
    password: '123456',
    user: {
      id: 'T002',
      name: 'Trần Văn Giảng',
      email: 'giao@aegis.ai',
      role: 'Giáo viên',
    },
  },
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const error = ref('')
  const loading = ref(false)

  const isAuthenticated = computed(() => !!user.value)

  function init() {
    const saved = localStorage.getItem('aegis_user')
    if (saved) {
      try {
        user.value = JSON.parse(saved)
      } catch {
        localStorage.removeItem('aegis_user')
      }
    }
  }

  async function login(email: string, password: string): Promise<boolean> {
    loading.value = true
    error.value = ''
    await new Promise((r) => setTimeout(r, 600))

    const record = MOCK_USERS[email]
    if (!record || record.password !== password) {
      error.value = 'Email hoặc mật khẩu không đúng'
      loading.value = false
      return false
    }

    user.value = record.user
    localStorage.setItem('aegis_user', JSON.stringify(record.user))
    loading.value = false
    return true
  }

  async function register(
    name: string,
    email: string,
    password: string
  ): Promise<boolean> {
    loading.value = true
    error.value = ''
    await new Promise((r) => setTimeout(r, 600))

    if (MOCK_USERS[email]) {
      error.value = 'Email đã được sử dụng'
      loading.value = false
      return false
    }

    const newUser: User = {
      id: `T${String(Object.keys(MOCK_USERS).length + 1).padStart(3, '0')}`,
      name,
      email,
      role: 'Giáo viên',
    }

    MOCK_USERS[email] = { password, user: newUser }
    user.value = newUser
    localStorage.setItem('aegis_user', JSON.stringify(newUser))
    loading.value = false
    return true
  }

  function logout() {
    user.value = null
    localStorage.removeItem('aegis_user')
  }

  init()

  return { user, error, loading, isAuthenticated, login, register, logout }
})
