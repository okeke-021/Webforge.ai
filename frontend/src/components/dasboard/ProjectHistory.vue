<template>
  <div class="p-6">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Your Projects</h2>
      <button
        @click="$router.push('/generator')"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
      >
        + New Project
      </button>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
    </div>

    <div v-else-if="projects.length === 0" class="text-center py-12">
      <svg class="w-16 h-16 mx-auto text-gray-400 dark:text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">No projects yet</h3>
      <p class="text-gray-600 dark:text-gray-400 mb-4">Get started by generating your first app</p>
      <button
        @click="$router.push('/generator')"
        class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
      >
        Create Your First Project
      </button>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="project in projects"
        :key="project.id"
        class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:border-blue-500 dark:hover:border-blue-400 transition-colors cursor-pointer"
        @click="$router.push(`/results/${project.id}`)"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <h3 class="font-semibold text-gray-900 dark:text-white mb-1">{{ project.name }}</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">{{ project.description }}</p>
            
            <div class="flex items-center space-x-4 text-sm">
              <span
                :class="[
                  'px-2 py-1 rounded-full',
                  getStatusClass(project.status)
                ]"
              >
                {{ project.status }}
              </span>
              <span class="text-gray-500 dark:text-gray-400">
                {{ formatDate(project.created_at) }}
              </span>
              <span class="text-gray-500 dark:text-gray-400">
                {{ project.tech_stack?.frontend }} + {{ project.tech_stack?.backend }}
              </span>
            </div>
          </div>

          <div class="flex items-center space-x-2">
            <button
              v-if="project.status === 'completed'"
              @click.stop="downloadProject(project.id)"
              class="p-2 text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
            </button>
            <button
              @click.stop="deleteProject(project.id)"
              class="p-2 text-gray-600 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../services/api'

const router = useRouter()
const projects = ref([])
const loading = ref(true)

onMounted(async () => {
  await fetchProjects()
})

const fetchProjects = async () => {
  try {
    loading.value = true
    const response = await api.get('/generator/projects/')
    projects.value = response.data
  } catch (error) {
    console.error('Failed to fetch projects:', error)
  } finally {
    loading.value = false
  }
}

const getStatusClass = (status) => {
  const classes = {
    completed: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    failed: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
    pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
    generating: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400'
  }
  return classes[status] || classes.pending
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return 'Today'
  if (days === 1) return 'Yesterday'
  if (days < 7) return `${days} days ago`
  
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const downloadProject = async (projectId) => {
  try {
    const response = await api.get(`/generator/projects/${projectId}/download/`, {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'project.zip')
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    alert('Failed to download project')
  }
}

const deleteProject = async (projectId) => {
  if (!confirm('Are you sure you want to delete this project?')) return
  
  try {
    await api.delete(`/generator/projects/${projectId}/`)
    await fetchProjects()
  } catch (error) {
    alert('Failed to delete project')
  }
}
</script>
