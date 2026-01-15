<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-8 px-4">
    <div class="max-w-7xl mx-auto">
      <div v-if="loading" class="text-center py-20">
        <div class="inline-block w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
        <p class="mt-4 text-gray-600 dark:text-gray-400">Loading project...</p>
      </div>

      <div v-else-if="error" class="text-center py-20">
        <p class="text-red-600 dark:text-red-400">{{ error }}</p>
        <button @click="$router.push('/dashboard')" class="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg">
          Back to Dashboard
        </button>
      </div>

      <div v-else-if="project" class="space-y-6">
        <!-- Header -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div class="flex items-start justify-between">
            <div>
              <div class="flex items-center space-x-3 mb-2">
                <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
                  {{ project.name }}
                </h1>
                <span v-if="project.is_draft" class="px-3 py-1 bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400 rounded-full text-sm font-semibold">
                  Draft - Iteration {{ project.iteration_count }}
                </span>
              </div>
              <p class="text-gray-600 dark:text-gray-400">
                {{ project.description }}
              </p>
              <div class="flex items-center space-x-4 mt-4">
                <span class="px-3 py-1 bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 rounded-full text-sm">
                  {{ project.status }}
                </span>
                <span class="text-sm text-gray-500 dark:text-gray-400">
                  Created {{ formatDate(project.created_at) }}
                </span>
              </div>
            </div>
            <div class="flex space-x-3">
              <button
                v-if="!project.is_draft"
                @click="downloadProject"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition flex items-center space-x-2"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                <span>Download ZIP</span>
              </button>
              <a
                v-if="project.github_repo_url"
                :href="project.github_repo_url"
                target="_blank"
                class="px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition flex items-center space-x-2"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
                <span>View on GitHub</span>
              </a>
            </div>
          </div>
        </div>

        <!-- Draft Mode Actions -->
        <div v-if="project.is_draft" class="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                ✨ Review & Refine Your App
              </h3>
              <p class="text-gray-700 dark:text-gray-300 mb-4">
                Preview the generated code below. Want to add more features or make changes? You can refine this project before committing to GitHub.
              </p>
              <div class="flex space-x-3">
                <button
                  @click="showRefinementModal = true"
                  class="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition font-semibold flex items-center space-x-2"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  <span>Add Features / Make Changes</span>
                </button>
                <button
                  @click="finalizeProject"
                  :disabled="finalizing"
                  class="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-300 transition font-semibold flex items-center space-x-2"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span>{{ finalizing ? 'Finalizing...' : 'Finalize & Push to GitHub' }}</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Suggested Features (Draft Mode) -->
        <div v-if="project.is_draft && suggestedFeatures.length > 0" class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            💡 Suggested Enhancements
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button
              v-for="(suggestion, idx) in suggestedFeatures"
              :key="idx"
              @click="applySuggestion(suggestion)"
              class="p-4 text-left border border-gray-200 dark:border-gray-700 rounded-lg hover:border-blue-500 dark:hover:border-blue-400 hover:bg-blue-50 dark:hover:bg-gray-700 transition"
            >
              <div class="flex items-start justify-between mb-2">
                <h4 class="font-semibold text-gray-900 dark:text-white">{{ suggestion.feature }}</h4>
                <span class="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded">
                  {{ suggestion.complexity }}
                </span>
              </div>
              <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">{{ suggestion.description }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-500">✨ {{ suggestion.benefit }}</p>
            </button>
          </div>
        </div>

        <!-- Refinement History -->
        <div v-if="project.iteration_count > 1" class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            📝 Refinement History
          </h3>
          <div class="space-y-3">
            <div
              v-for="(refinement, idx) in refinementHistory"
              :key="idx"
              class="flex items-start space-x-3 p-3 bg-gray-50 dark:bg-gray-700 rounded"
            >
              <div class="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-semibold flex-shrink-0">
                {{ refinement.iteration_number }}
              </div>
              <div class="flex-1">
                <p class="text-sm font-semibold text-gray-900 dark:text-white">{{ refinement.requested_changes }}</p>
                <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  Changed {{ refinement.files_changed.length }} files
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Tabs -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow">
          <div class="border-b border-gray-200 dark:border-gray-700">
            <nav class="flex space-x-8 px-6" aria-label="Tabs">
              <button
                v-for="tab in tabs"
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="[
                  'py-4 px-1 border-b-2 font-medium text-sm transition-colors',
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                    : 'border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
                ]"
              >
                {{ tab.label }}
              </button>
            </nav>
          </div>

          <div class="p-6">
            <CodePreview v-if="activeTab === 'code'" :files="project.generated_files" />
            <LivePreview v-else-if="activeTab === 'preview'" :project="project" />
            <div v-else-if="activeTab === 'specs'" class="prose dark:prose-invert max-w-none">
              <pre class="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg overflow-x-auto">{{ JSON.stringify(project.specifications, null, 2) }}</pre>
            </div>
          </div>
        </div>
      </div>

      <!-- Refinement Modal -->
      <div v-if="showRefinementModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
          <div class="p-6 border-b border-gray-200 dark:border-gray-700">
            <div class="flex items-center justify-between">
              <h2 class="text-2xl font-bold text-gray-900 dark:text-white">✨ Refine Your App</h2>
              <button @click="showRefinementModal = false" class="text-gray-500 hover:text-gray-700 dark:hover:text-gray-300">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          <div class="p-6 space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                What would you like to add or change?
              </label>
              <textarea
                v-model="refinementRequest"
                rows="6"
                placeholder="Examples:
- Add user authentication with email/password
- Add a dark mode toggle
- Make the homepage more visually appealing
- Add a search feature for products
- Include form validation"
                class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white resize-none"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                Quick Add Features
              </label>
              <div class="grid grid-cols-2 gap-3">
                <button
                  v-for="quickFeature in quickFeatures"
                  :key="quickFeature"
                  @click="toggleQuickFeature(quickFeature)"
                  :class="[
                    'p-3 text-sm rounded-lg border transition',
                    selectedQuickFeatures.includes(quickFeature)
                      ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300'
                      : 'border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:border-blue-400'
                  ]"
                >
                  {{ quickFeature }}
                </button>
              </div>
            </div>

            <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200 dark:border-gray-700">
              <button
                @click="showRefinementModal = false"
                class="px-6 py-2 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition"
              >
                Cancel
              </button>
              <button
                @click="submitRefinement"
                :disabled="!canSubmitRefinement || isRefining"
                class="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition font-semibold"
              >
                {{ isRefining ? 'Refining...' : '✨ Refine Project' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../services/api'
import CodePreview from '../components/preview/CodePreview.vue'
import LivePreview from '../components/preview/LivePreview.vue'

const route = useRoute()
const router = useRouter()

const project = ref(null)
const loading = ref(true)
const error = ref(null)
const activeTab = ref('code')
const showRefinementModal = ref(false)
const refinementRequest = ref('')
const selectedQuickFeatures = ref([])
const isRefining = ref(false)
const finalizing = ref(false)
const suggestedFeatures = ref([])
const refinementHistory = ref([])

const tabs = [
  { id: 'code', label: 'Code' },
  { id: 'preview', label: 'Live Preview' },
  { id: 'specs', label: 'Specifications' }
]

const quickFeatures = [
  'Authentication',
  'Dark Mode',
  'Search Functionality',
  'Form Validation',
  'Pagination',
  'File Upload',
  'Email Notifications',
  'Charts/Analytics'
]

const canSubmitRefinement = computed(() => {
  return refinementRequest.value.trim().length > 10 || selectedQuickFeatures.value.length > 0
})

onMounted(async () => {
  await loadProject()
  if (project.value?.is_draft) {
    await loadSuggestedFeatures()
    await loadRefinementHistory()
  }
})

const loadProject = async () => {
  try {
    loading.value = true
    const projectId = route.params.projectId
    const response = await api.get(`/generator/projects/${projectId}/`)
    project.value = response.data
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to load project'
  } finally {
    loading.value = false
  }
}

const loadSuggestedFeatures = async () => {
  try {
    const response = await api.get(`/generator/projects/${project.value.id}/suggested-features/`)
    suggestedFeatures.value = response.data
  } catch (err) {
    console.error('Failed to load suggestions:', err)
  }
}

const loadRefinementHistory = async () => {
  try {
    const response = await api.get(`/generator/projects/${project.value.id}/refinements/`)
    refinementHistory.value = response.data
  } catch (err) {
    console.error('Failed to load history:', err)
  }
}

const toggleQuickFeature = (feature) => {
  const index = selectedQuickFeatures.value.indexOf(feature)
  if (index > -1) {
    selectedQuickFeatures.value.splice(index, 1)
  } else {
    selectedQuickFeatures.value.push(feature)
  }
}

const applySuggestion = (suggestion) => {
  refinementRequest.value = `Add ${suggestion.feature}: ${suggestion.description}`
  showRefinementModal.value = true
}

const submitRefinement = async () => {
  if (!canSubmitRefinement.value) return

  try {
    isRefining.value = true
    showRefinementModal.value = false

    const response = await api.post(`/generator/projects/${project.value.id}/refine/`, {
      requested_features: selectedQuickFeatures.value,
      requested_changes: refinementRequest.value
    })

    // Poll for refinement completion
    await pollRefinementStatus(response.data.refinement_id)

    // Reload project
    await loadProject()
    await loadRefinementHistory()

    refinementRequest.value = ''
    selectedQuickFeatures.value = []
  } catch (err) {
    alert(err.response?.data?.message || 'Failed to refine project')
  } finally {
    isRefining.value = false
  }
}

const pollRefinementStatus = async (refinementId) => {
  return new Promise((resolve) => {
    const interval = setInterval(async () => {
      try {
        const response = await api.get(`/generator/refinements/${refinementId}/`)
        if (response.data.status === 'completed' || response.data.status === 'failed') {
          clearInterval(interval)
          resolve()
        }
      } catch (err) {
        clearInterval(interval)
        resolve()
      }
    }, 2000)
  })
}

const finalizeProject = async () => {
  if (!confirm('Are you sure? This will push the project to GitHub and mark it as final.')) return

  try {
    finalizing.value = true
    await api.post(`/generator/projects/${project.value.id}/finalize/`)
    await loadProject()
    alert('Project finalized and pushed to GitHub!')
  } catch (err) {
    alert(err.response?.data?.message || 'Failed to finalize project')
  } finally {
    finalizing.value = false
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const downloadProject = async () => {
  try {
    const response = await api.get(
      `/generator/projects/${project.value.id}/download/`,
      { responseType: 'blob' }
    )
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${project.value.name}.zip`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (err) {
    alert('Failed to download project')
  }
}
</script>
