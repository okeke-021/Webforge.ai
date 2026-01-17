<template>
  <div class="space-y-6">
    <div class="text-center">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
        {{ statusTitle }}
      </h2>
      <p class="text-gray-600 dark:text-gray-400">
        {{ statusMessage }}
      </p>
    </div>

    <!-- Progress Bar -->
    <div class="space-y-2">
      <div class="flex justify-between text-sm text-gray-600 dark:text-gray-400">
        <span>Progress</span>
        <span>{{ progress }}%</span>
      </div>
      <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
        <div
          class="h-full bg-gradient-to-r from-blue-500 to-purple-600 transition-all duration-500 ease-out rounded-full"
          :style="{ width: `${progress}%` }"
        >
          <div class="h-full w-full animate-pulse bg-white/20" />
        </div>
      </div>
    </div>

    <!-- Generation Steps -->
    <div class="space-y-3">
      <div
        v-for="step in steps"
        :key="step.id"
        class="flex items-start space-x-3 p-4 rounded-lg border transition-all"
        :class="getStepClass(step)"
      >
        <div class="flex-shrink-0 mt-1">
          <div v-if="step.status === 'completed'" class="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div v-else-if="step.status === 'in_progress'" class="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
          <div v-else-if="step.status === 'failed'" class="w-6 h-6 bg-red-500 rounded-full flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
          <div v-else class="w-6 h-6 bg-gray-300 dark:bg-gray-600 rounded-full" />
        </div>
        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between">
            <h4 class="text-sm font-semibold text-gray-900 dark:text-white">
              {{ step.title }}
            </h4>
            <span
              v-if="step.status === 'in_progress'"
              class="text-xs text-blue-600 dark:text-blue-400 animate-pulse"
            >
              In Progress...
            </span>
          </div>
          <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
            {{ step.description }}
          </p>
          <div v-if="step.details && step.status === 'in_progress'" class="mt-2 text-xs text-gray-500 dark:text-gray-500">
            {{ step.details }}
          </div>
        </div>
      </div>
    </div>

    <!-- Status Messages -->
    <div
      v-if="statusMessages.length > 0"
      class="max-h-48 overflow-y-auto space-y-2 bg-gray-50 dark:bg-gray-800 rounded-lg p-4"
    >
      <div
        v-for="(msg, idx) in recentMessages"
        :key="idx"
        class="text-xs text-gray-600 dark:text-gray-400 flex items-start space-x-2"
      >
        <span class="text-gray-400">{{ formatTime(msg.timestamp) }}</span>
        <span :class="getMessageClass(msg.type)">{{ msg.message }}</span>
      </div>
    </div>

    <!-- Error Display -->
    <div
      v-if="generationStatus === 'failed'"
      class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4"
    >
      <div class="flex items-start space-x-3">
        <svg class="w-6 h-6 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div class="flex-1">
          <h4 class="text-sm font-semibold text-red-900 dark:text-red-200 mb-1">
            Generation Failed
          </h4>
          <p class="text-sm text-red-800 dark:text-red-300">
            {{ errorMessage || 'An error occurred during generation. Please try again.' }}
          </p>
          <button
            @click="handleRetry"
            class="mt-3 px-4 py-2 bg-red-600 text-white text-sm rounded hover:bg-red-700 transition"
          >
            Try Again
          </button>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div v-if="generationStatus === 'completed'" class="flex justify-center pt-6">
      <button
        @click="viewResults"
        class="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all transform hover:scale-105 shadow-lg"
      >
        View Your Generated App →
      </button>
    </div>

    <div v-else-if="generationStatus === 'idle'" class="flex justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
      <button
        @click="generatorStore.prevStep()"
        class="px-6 py-3 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition"
      >
        Back
      </button>
      <button
        @click="handleGenerate"
        :disabled="isGenerating"
        class="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg"
      >
        <span v-if="!isGenerating">🚀 Start Generation</span>
        <span v-else>Generating...</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useGeneratorStore } from '../../stores/generator'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const generatorStore = useGeneratorStore()
const authStore = useAuthStore()

const steps = ref([
  { id: 'analyzing', title: 'Analyzing Requirements', description: 'Processing your app description', status: 'pending', details: '' },
  { id: 'planning', title: 'Planning Architecture', description: 'Designing the technical structure', status: 'pending', details: '' },
  { id: 'generating', title: 'Generating Code', description: 'Creating all project files', status: 'pending', details: '' },
  { id: 'validating', title: 'Validating Code', description: 'Running quality checks and tests', status: 'pending', details: '' },
  { id: 'packaging', title: 'Packaging Files', description: 'Preparing your project', status: 'pending', details: '' },
  { id: 'github', title: 'Creating GitHub Repo', description: 'Setting up version control', status: 'pending', details: '' }
])

const isGenerating = computed(() => {
  return ['starting', 'analyzing', 'planning', 'generating', 'validating', 'packaging'].includes(generatorStore.generationStatus)
})

const generationStatus = computed(() => generatorStore.generationStatus)
const progress = computed(() => generatorStore.progress)
const statusMessages = computed(() => generatorStore.statusMessages)
const errorMessage = computed(() => generatorStore.currentProject?.error_message)

const recentMessages = computed(() => {
  return statusMessages.value.slice(-10).reverse()
})

const statusTitle = computed(() => {
  const titles = {
    idle: 'Ready to Generate',
    starting: 'Starting Generation',
    analyzing: 'Analyzing Your Requirements',
    planning: 'Planning Architecture',
    generating: 'Generating Code Files',
    validating: 'Validating Code Quality',
    packaging: 'Packaging Your Project',
    completed: '✨ Generation Complete!',
    failed: '❌ Generation Failed'
  }
  return titles[generationStatus.value] || 'Processing...'
})

const statusMessage = computed(() => {
  const messages = {
    idle: 'Click the button below to start generating your application',
    starting: 'Initializing AI generation pipeline...',
    analyzing: 'Understanding your requirements and planning the project structure',
    planning: 'Creating detailed technical specifications and file structure',
    generating: 'Writing code for all components, APIs, and configurations',
    validating: 'Checking code quality, security, and running tests',
    packaging: 'Finalizing your project and preparing for deployment',
    completed: 'Your application is ready! Click below to view and download.',
    failed: 'Something went wrong during generation'
  }
  return messages[generationStatus.value] || 'Working on your project...'
})

watch(generationStatus, (newStatus) => {
  const stepMap = {
    analyzing: 'analyzing',
    planning: 'planning',
    generating: 'generating',
    validating: 'validating',
    packaging: 'packaging',
    completed: 'github'
  }
  
  steps.value.forEach(step => {
    if (stepMap[newStatus] === step.id) {
      step.status = 'in_progress'
    } else if (Object.keys(stepMap).indexOf(newStatus) > Object.keys(stepMap).indexOf(Object.keys(stepMap).find(k => stepMap[k] === step.id))) {
      step.status = 'completed'
    } else if (newStatus === 'failed') {
      if (step.status === 'in_progress') {
        step.status = 'failed'
      }
    }
  })
})

const getStepClass = (step) => {
  if (step.status === 'completed') {
    return 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'
  }
  if (step.status === 'in_progress') {
    return 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800'
  }
  if (step.status === 'failed') {
    return 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800'
  }
  return 'bg-gray-50 dark:bg-gray-800 border-gray-200 dark:border-gray-700'
}

const getMessageClass = (type) => {
  const classes = {
    info: 'text-gray-700 dark:text-gray-300',
    success: 'text-green-600 dark:text-green-400',
    warning: 'text-yellow-600 dark:text-yellow-400',
    error: 'text-red-600 dark:text-red-400'
  }
  return classes[type] || classes.info
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

const handleGenerate = async () => {
  if (!authStore.checkUsageLimit('generations')) {
    alert('You have reached your monthly generation limit. Please upgrade your plan.')
    router.push('/pricing')
    return
  }

  try {
    const result = await generatorStore.startGeneration()
    console.log('Generation started:', result)
  } catch (error) {
    console.error('Generation failed:', error)
  }
}

const handleRetry = () => {
  generatorStore.resetWizard()
}

const viewResults = () => {
  if (generatorStore.currentProject?.id) {
    router.push(`/results/${generatorStore.currentProject.id}`)
  }
}
</script>
