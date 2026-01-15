<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-8 px-4">
    <div class="max-w-6xl mx-auto">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          🐛 Debug Repository
        </h1>
        <p class="text-gray-600 dark:text-gray-400">
          Analyze your GitHub repository and get AI-powered bug fixes
        </p>
      </div>

      <!-- Input Form -->
      <div v-if="!debugSession" class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 mb-8">
        <div class="space-y-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              GitHub Repository URL
            </label>
            <input
              v-model="repoUrl"
              type="url"
              placeholder="https://github.com/username/repository"
              class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
            />
            <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
              Enter the URL of the repository you want to analyze
            </p>
          </div>

          <div v-if="subscription !== 'enterprise'" class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
            <div class="flex items-start space-x-3">
              <svg class="w-6 h-6 text-yellow-600 dark:text-yellow-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              <div>
                <h4 class="text-sm font-semibold text-yellow-900 dark:text-yellow-200 mb-1">
                  Enterprise Feature
                </h4>
                <p class="text-sm text-yellow-800 dark:text-yellow-300">
                  Repository debugging is only available for Enterprise plan subscribers.
                </p>
                <button
                  @click="$router.push('/pricing')"
                  class="mt-3 px-4 py-2 bg-yellow-600 text-white rounded hover:bg-yellow-700 transition text-sm"
                >
                  Upgrade to Enterprise
                </button>
              </div>
            </div>
          </div>

          <button
            @click="startDebug"
            :disabled="!repoUrl || subscription !== 'enterprise' || isAnalyzing"
            class="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition font-semibold"
          >
            {{ isAnalyzing ? 'Analyzing...' : '🔍 Start Analysis' }}
          </button>
        </div>
      </div>

      <!-- Analysis Progress -->
      <div v-if="debugSession && debugSession.status !== 'completed'" class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
        <div class="text-center mb-8">
          <div class="inline-block w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4" />
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
            {{ statusTitle }}
          </h2>
          <p class="text-gray-600 dark:text-gray-400">{{ statusMessage }}</p>
        </div>

        <div class="space-y-2 mb-6">
          <div class="flex justify-between text-sm text-gray-600 dark:text-gray-400">
            <span>Progress</span>
            <span>{{ debugSession.progress }}%</span>
          </div>
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
            <div
              class="h-full bg-gradient-to-r from-blue-500 to-purple-600 rounded-full transition-all duration-500"
              :style="{ width: `${debugSession.progress}%` }"
            />
          </div>
        </div>
      </div>

      <!-- Analysis Results -->
      <div v-if="debugSession && debugSession.status === 'completed'" class="space-y-6">
        <!-- Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm text-gray-600 dark:text-gray-400">Files Analyzed</span>
              <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ debugSession.total_files_analyzed }}</p>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm text-gray-600 dark:text-gray-400">Issues Found</span>
              <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <p class="text-3xl font-bold text-gray-900 dark:text-white">{{ debugSession.total_issues_found }}</p>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm text-gray-600 dark:text-gray-400">Critical Issues</span>
              <span class="text-3xl">🔴</span>
            </div>
            <p class="text-3xl font-bold text-gray-900 dark:text-white">
              {{ debugSession.severity_breakdown?.critical || 0 }}
            </p>
          </div>

          <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm text-gray-600 dark:text-gray-400">Files Fixed</span>
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p class="text-3xl font-bold text-gray-900 dark:text-white">
              {{ Object.keys(debugSession.fixed_files || {}).length }}
            </p>
          </div>
        </div>

        <!-- Issues List -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow">
          <div class="p-6 border-b border-gray-200 dark:border-gray-700">
            <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Detected Issues</h2>
          </div>
          <div class="divide-y divide-gray-200 dark:divide-gray-700">
            <div
              v-for="(issue, idx) in sortedIssues"
              :key="idx"
              class="p-6 hover:bg-gray-50 dark:hover:bg-gray-700 transition"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center space-x-3 mb-2">
                    <span
                      :class="[
                        'px-2 py-1 rounded text-xs font-semibold',
                        getSeverityClass(issue.severity)
                      ]"
                    >
                      {{ issue.severity }}
                    </span>
                    <span class="text-sm text-gray-600 dark:text-gray-400">
                      {{ issue.file }}:{{ issue.line || '?' }}
                    </span>
                  </div>
                  <h3 class="font-semibold text-gray-900 dark:text-white mb-2">
                    {{ issue.description }}
                  </h3>
                  <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
                    💡 {{ issue.suggestion }}
                  </p>
                  <details class="text-sm">
                    <summary class="cursor-pointer text-blue-600 dark:text-blue-400 hover:underline">
                      View code snippet
                    </summary>
                    <div class="mt-3 grid grid-cols-2 gap-4">
                      <div>
                        <p class="text-xs text-gray-500 dark:text-gray-400 mb-2">❌ Before:</p>
                        <pre class="bg-gray-900 text-gray-100 p-3 rounded text-xs overflow-x-auto">{{ issue.code_snippet }}</pre>
                      </div>
                      <div>
                        <p class="text-xs text-gray-500 dark:text-gray-400 mb-2">✅ After:</p>
                        <pre class="bg-gray-900 text-gray-100 p-3 rounded text-xs overflow-x-auto">{{ issue.fixed_code }}</pre>
                      </div>
                    </div>
                  </details>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Next Steps</h3>
          <div class="flex space-x-4">
            <button
              v-if="!debugSession.pull_request_url"
              @click="createPullRequest"
              :disabled="creatingPR"
              class="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-300 transition font-semibold"
            >
              {{ creatingPR ? 'Creating PR...' : '✨ Create Pull Request with Fixes' }}
            </button>
            <a
              v-else
              :href="debugSession.pull_request_url"
              target="_blank"
              class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-semibold inline-block"
            >
              View Pull Request →
            </a>
            <button
              @click="reset"
              class="px-6 py-3 bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition"
            >
              Analyze Another Repo
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

const authStore = useAuthStore()

const subscription = computed(() => authStore.subscription)

const repoUrl = ref('')
const debugSession = ref(null)
const isAnalyzing = ref(false)
const creatingPR = ref(false)

const sortedIssues = computed(() => {
  if (!debugSession.value?.issues) return []
  
  const severityOrder = { critical: 0, high: 1, medium: 2, low: 3 }
  return [...debugSession.value.issues].sort((a, b) => {
    return severityOrder[a.severity] - severityOrder[b.severity]
  })
})

const statusTitle = computed(() => {
  const titles = {
    pending: 'Initializing Analysis',
    analyzing: 'Analyzing Repository',
    fixing: 'Generating Fixes',
    completed: 'Analysis Complete'
  }
  return titles[debugSession.value?.status] || 'Processing...'
})

const statusMessage = computed(() => {
  const messages = {
    pending: 'Preparing to analyze your repository...',
    analyzing: 'Scanning files and detecting issues...',
    fixing: 'Generating AI-powered fixes...',
    completed: 'All issues have been analyzed and fixed!'
  }
  return messages[debugSession.value?.status] || 'Working on it...'
})

const startDebug = async () => {
  if (!repoUrl.value || subscription.value !== 'enterprise') return
  
  try {
    isAnalyzing.value = true
    const response = await api.post('/generator/debug/', {
      repo_url: repoUrl.value
    })
    
    debugSession.value = response.data
    
    // Poll for updates
    pollDebugStatus()
  } catch (error) {
    alert(error.response?.data?.message || 'Failed to start analysis')
  } finally {
    isAnalyzing.value = false
  }
}

const pollDebugStatus = async () => {
  if (!debugSession.value) return
  
  const interval = setInterval(async () => {
    try {
      const response = await api.get(`/generator/debug/${debugSession.value.id}/`)
      debugSession.value = response.data
      
      if (response.data.status === 'completed' || response.data.status === 'failed') {
        clearInterval(interval)
      }
    } catch (error) {
      clearInterval(interval)
    }
  }, 2000)
}

const createPullRequest = async () => {
  try {
    creatingPR.value = true
    const response = await api.post(`/generator/debug/${debugSession.value.id}/apply-fixes/`)
    debugSession.value.pull_request_url = response.data.pull_request_url
    alert('Pull request created successfully!')
  } catch (error) {
    alert(error.response?.data?.message || 'Failed to create pull request')
  } finally {
    creatingPR.value = false
  }
}

const getSeverityClass = (severity) => {
  const classes = {
    critical: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
    high: 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400',
    medium: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
    low: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400'
  }
  return classes[severity] || classes.medium
}

const reset = () => {
  repoUrl.value = ''
  debugSession.value = null
  isAnalyzing.value = false
  creatingPR.value = false
}
</script>
