import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const initialized = ref(false)
  const loading = ref(false)

  const isAuthenticated = computed(() => !!user.value)
  const subscription = computed(() => user.value?.subscription || 'free')
  const usageLimit = computed(() => {
    const limits = {
      free: { generations: 3, dailyRequests: 5 },
      pro: { generations: 10, dailyRequests: 20 },
      enterprise: { generations: 20, dailyRequests: 50 }
    }
    return limits[subscription.value] || limits.free
  })

  async function checkAuth() {
    try {
      loading.value = true
      const response = await api.get('/auth/me/')
      user.value = response.data
    } catch (error) {
      user.value = null
    } finally {
      initialized.value = true
      loading.value = false
    }
  }

  async function login(provider = 'github') {
    const backendUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    window.location.href = `${backendUrl}/auth/${provider}/login/`
  }

  async function logout() {
    try {
      await api.post('/auth/logout/')
      user.value = null
      window.location.href = '/'
    } catch (error) {
      console.error('Logout failed:', error)
    }
  }

  function checkUsageLimit(type = 'generations') {
    if (!user.value) return false
    
    const usage = user.value.usage || {}
    const limit = usageLimit.value
    
    if (type === 'generations') {
      return (usage.monthlyGenerations || 0) < limit.generations
    }
    
    if (type === 'dailyRequests') {
      return (usage.todayRequests || 0) < limit.dailyRequests
    }
    
    return false
  }

  return {
    user,
    initialized,
    loading,
    isAuthenticated,
    subscription,
    usageLimit,
    checkAuth,
    login,
    logout,
    checkUsageLimit
  }
})
