<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-8 px-4">
    <div class="max-w-7xl mx-auto">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">Dashboard</h1>
        <p class="text-gray-600 dark:text-gray-400">Manage your generated projects</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <UsageAnalytics />
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-lg shadow">
        <ProjectHistory />
      </div>
    </div>
  </div>
</template>

<script setup>
import ProjectHistory from '../components/dashboard/ProjectHistory.vue'
import UsageAnalytics from '../components/dashboard/UsageAnalytics.vue'
</script>
