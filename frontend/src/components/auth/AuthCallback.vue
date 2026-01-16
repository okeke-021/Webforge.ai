<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
    <div class="text-center">
      <div class="inline-block w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4" />
      <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
        Completing sign in...
      </h2>
      <p class="text-gray-600 dark:text-gray-400">
        Please wait while we redirect you
      </p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

onMounted(async () => {
  try {
    // Check authentication status
    await authStore.checkAuth()
    
    // Redirect to dashboard or home
    const redirect = sessionStorage.getItem('authRedirect') || '/dashboard'
    sessionStorage.removeItem('authRedirect')
    
    router.push(redirect)
  } catch (error) {
    console.error('Auth callback error:', error)
    router.push('/?error=auth_failed')
  }
})
</script>
