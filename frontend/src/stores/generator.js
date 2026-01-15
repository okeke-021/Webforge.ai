import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'
import { connectWebSocket } from '../services/websocket'

export const useGeneratorStore = defineStore('generator', () => {
  const currentStep = ref(1)
  const totalSteps = ref(5)
  const description = ref('')
  const features = ref([])
  const techStack = ref({
    frontend: 'react',
    backend: 'nodejs',
    database: 'postgresql'
  })
  const stylePreferences = ref({
    theme: 'modern',
    colorScheme: 'blue',
    layout: 'dashboard'
  })
  const generationStatus = ref('idle')
  const progress = ref(0)
  const currentProject = ref(null)
  const statusMessages = ref([])
  const socket = ref(null)

  function nextStep() {
    if (currentStep.value < totalSteps.value) {
      currentStep.value++
    }
  }

  function prevStep() {
    if (currentStep.value > 1) {
      currentStep.value--
    }
  }

  function resetWizard() {
    currentStep.value = 1
    description.value = ''
    features.value = []
    techStack.value = {
      frontend: 'react',
      backend: 'nodejs',
      database: 'postgresql'
    }
    stylePreferences.value = {
      theme: 'modern',
      colorScheme: 'blue',
      layout: 'dashboard'
    }
    generationStatus.value = 'idle'
    progress.value = 0
    statusMessages.value = []
  }

  async function startGeneration() {
    try {
      generationStatus.value = 'starting'
      progress.value = 0
      statusMessages.value = []

      const payload = {
        description: description.value,
        features: features.value,
        tech_stack: techStack.value,
        style_preferences: stylePreferences.value
      }

      const response = await api.post('/generator/generate/', payload)
      currentProject.value = response.data
      
      connectToWebSocket(response.data.id)
      
      return response.data
    } catch (error) {
      generationStatus.value = 'failed'
      throw error
    }
  }

  function connectToWebSocket(projectId) {
    socket.value = connectWebSocket(projectId, {
      onStatus: (data) => {
        generationStatus.value = data.status
        progress.value = data.progress || 0
        if (data.message) {
          statusMessages.value.push({
            timestamp: new Date().toISOString(),
            message: data.message,
            type: data.type || 'info'
          })
        }
      },
      onComplete: (data) => {
        generationStatus.value = 'completed'
        progress.value = 100
        currentProject.value = { ...currentProject.value, ...data }
      },
      onError: (error) => {
        generationStatus.value = 'failed'
        statusMessages.value.push({
          timestamp: new Date().toISOString(),
          message: error.message || 'Generation failed',
          type: 'error'
        })
      }
    })
  }

  function disconnectWebSocket() {
    if (socket.value) {
      socket.value.disconnect()
      socket.value = null
    }
  }

  return {
    currentStep,
    totalSteps,
    description,
    features,
    techStack,
    stylePreferences,
    generationStatus,
    progress,
    currentProject,
    statusMessages,
    nextStep,
    prevStep,
    resetWizard,
    startGeneration,
    disconnectWebSocket
  }
})
