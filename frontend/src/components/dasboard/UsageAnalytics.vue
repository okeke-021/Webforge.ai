<template>
  <div class="col-span-3 grid grid-cols-1 md:grid-cols-3 gap-6">
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">Monthly Generations</h3>
        <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <div class="flex items-end justify-between">
        <div>
          <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ usage.monthlyGenerations }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">of {{ limits.generations }}</p>
        </div>
        <div class="w-24 h-24">
          <svg viewBox="0 0 36 36" class="circular-chart">
            <path
              class="circle-bg"
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              fill="none"
              stroke="#e5e7eb"
              stroke-width="3"
            />
            <path
              class="circle"
              :stroke-dasharray="`${generationPercentage}, 100`"
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              fill="none"
              stroke="#3b82f6"
              stroke-width="3"
              stroke-linecap="round"
            />
          </svg>
        </div>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">Today's Requests</h3>
        <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      </div>
      <div class="flex items-end justify-between">
        <div>
          <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ usage.todayRequests }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">of {{ limits.dailyRequests }}</p>
        </div>
        <div class="w-24 h-24">
          <svg viewBox="0 0 36 36" class="circular-chart">
            <path
              class="circle-bg"
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              fill="none"
              stroke="#e5e7eb"
              stroke-width="3"
            />
            <path
              class="circle"
              :stroke-dasharray="`${requestPercentage}, 100`"
              d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              fill="none"
              stroke="#10b981"
              stroke-width="3"
              stroke-linecap="round"
            />
          </svg>
        </div>
      </div>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-sm font-medium text-gray-600 dark:text-gray-400">Success Rate</h3>
        <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      </div>
      <div>
        <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ successRate }}%</p>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
          {{ usage.successfulProjects }} of {{ usage.totalProjects }} projects
        </p>
      </div>
    </div>

    <div v-if="remaining.generations <= 1" class="col-span-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
      <div class="flex items-start space-x-3">
        <svg class="w-6 h-6 text-yellow-600 dark:text-yellow-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
        <div class="flex-1">
          <h4 class="text-sm font-semibold text-yellow-900 dark:text-yellow-200 mb-1">
            Running low on generations
          </h4>
          <p class="text-sm text-yellow-800 dark:text-yellow-300 mb-3">
            You have {{ remaining.generations }} generation{{ remaining.generations === 1 ? '' : 's' }} left this month.
          </p>
          <button
            @click="$router.push('/pricing')"
            class="px-4 py-2 bg-yellow-600 text-white rounded hover:bg-yellow-700 transition text-sm font-medium"
          >
            Upgrade Plan
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../services/api'

const usage = ref({
  monthlyGenerations: 0,
  todayRequests: 0,
  totalProjects: 0,
  successfulProjects: 0,
  failedProjects: 0
})

const limits = ref({
  generations: 3,
  dailyRequests: 5
})

const remaining = ref({
  generations: 3,
  requests: 5
})

const generationPercentage = computed(() => {
  return (usage.value.monthlyGenerations / limits.value.generations) * 100
})

const requestPercentage = computed(() => {
  return (usage.value.todayRequests / limits.value.dailyRequests) * 100
})

const successRate = computed(() => {
  if (usage.value.totalProjects === 0) return 0
  return Math.round((usage.value.successfulProjects / usage.value.totalProjects) * 100)
})

onMounted(async () => {
  try {
    const response = await api.get('/generator/usage/')
    usage.value = response.data.usage
    limits.value = response.data.limits
    remaining.value = response.data.remaining
  } catch (error) {
    console.error('Failed to fetch usage:', error)
  }
})
</script>

<style scoped>
.circular-chart {
  transform: rotate(-90deg);
}
</style>
