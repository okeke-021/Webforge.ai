<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
        Select Features
      </h2>
      <p class="text-gray-600 dark:text-gray-400">
        Choose the features you want in your application
      </p>
    </div>

    <!-- Search Features -->
    <div class="relative">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search features..."
        class="w-full px-4 py-3 pl-10 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
      />
      <svg class="absolute left-3 top-3.5 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </div>

    <!-- Feature Categories -->
    <div class="space-y-4">
      <div v-for="category in filteredCategories" :key="category.name" class="space-y-3">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
          <span class="mr-2">{{ category.icon }}</span>
          {{ category.name }}
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <button
            v-for="feature in category.features"
            :key="feature.id"
            @click="toggleFeature(feature.id)"
            :class="[
              'p-4 text-left border rounded-lg transition-all',
              selectedFeatures.includes(feature.id)
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 dark:border-blue-400'
                : 'border-gray-300 dark:border-gray-600 hover:border-blue-400 dark:hover:border-blue-500'
            ]"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="flex items-center space-x-2">
                  <h4 class="font-semibold text-gray-900 dark:text-white text-sm">
                    {{ feature.name }}
                  </h4>
                  <span
                    v-if="feature.popular"
                    class="px-2 py-0.5 text-xs bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400 rounded"
                  >
                    Popular
                  </span>
                </div>
                <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">
                  {{ feature.description }}
                </p>
              </div>
              <div
                :class="[
                  'w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0 ml-2',
                  selectedFeatures.includes(feature.id)
                    ? 'bg-blue-600 border-blue-600'
                    : 'border-gray-300 dark:border-gray-600'
                ]"
              >
                <svg
                  v-if="selectedFeatures.includes(feature.id)"
                  class="w-3 h-3 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                </svg>
              </div>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Selected Count -->
    <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
      <p class="text-sm text-gray-700 dark:text-gray-300">
        <span class="font-semibold">{{ selectedFeatures.length }}</span> features selected
      </p>
    </div>

    <!-- Navigation -->
    <div class="flex justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
      <button
        @click="generatorStore.prevStep()"
        class="px-6 py-3 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition"
      >
        Back
      </button>
      <button
        @click="handleNext"
        :disabled="selectedFeatures.length === 0"
        class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
      >
        Next: Choose Tech Stack
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useGeneratorStore } from '../../stores/generator'

const generatorStore = useGeneratorStore()

const searchQuery = ref('')
const selectedFeatures = ref([...generatorStore.features])

const featureCategories = [
  {
    name: 'Authentication',
    icon: '🔐',
    features: [
      { id: 'email_auth', name: 'Email/Password Auth', description: 'Traditional email and password authentication', popular: true },
      { id: 'social_auth', name: 'Social Login', description: 'OAuth with Google, GitHub, Facebook', popular: true },
      { id: 'two_factor', name: 'Two-Factor Auth', description: 'SMS or authenticator app 2FA' },
      { id: 'magic_link', name: 'Magic Link', description: 'Passwordless email authentication' }
    ]
  },
  {
    name: 'Data Management',
    icon: '💾',
    features: [
      { id: 'crud', name: 'CRUD Operations', description: 'Create, Read, Update, Delete functionality', popular: true },
      { id: 'search', name: 'Search & Filter', description: 'Advanced search and filtering', popular: true },
      { id: 'pagination', name: 'Pagination', description: 'Paginated data display' },
      { id: 'export', name: 'Data Export', description: 'Export to CSV, PDF, Excel' }
    ]
  },
  {
    name: 'User Interface',
    icon: '🎨',
    features: [
      { id: 'responsive', name: 'Responsive Design', description: 'Mobile-first responsive layout', popular: true },
      { id: 'dark_mode', name: 'Dark Mode', description: 'Light and dark theme support', popular: true },
      { id: 'dashboard', name: 'Dashboard', description: 'Analytics and overview dashboard' },
      { id: 'notifications', name: 'Notifications', description: 'In-app notification system' }
    ]
  },
  {
    name: 'Communication',
    icon: '💬',
    features: [
      { id: 'comments', name: 'Comments System', description: 'User comments and replies' },
      { id: 'chat', name: 'Real-time Chat', description: 'Live messaging between users' },
      { id: 'email_notifications', name: 'Email Notifications', description: 'Automated email alerts' },
      { id: 'push_notifications', name: 'Push Notifications', description: 'Browser push notifications' }
    ]
  },
  {
    name: 'Media',
    icon: '📸',
    features: [
      { id: 'file_upload', name: 'File Upload', description: 'Upload and manage files', popular: true },
      { id: 'image_processing', name: 'Image Processing', description: 'Resize, crop, optimize images' },
      { id: 'video_support', name: 'Video Support', description: 'Video upload and playback' },
      { id: 'gallery', name: 'Media Gallery', description: 'Image and video gallery' }
    ]
  },
  {
    name: 'Analytics',
    icon: '📊',
    features: [
      { id: 'analytics', name: 'Analytics Dashboard', description: 'Usage statistics and insights' },
      { id: 'reporting', name: 'Report Generation', description: 'Automated report creation' },
      { id: 'charts', name: 'Charts & Graphs', description: 'Data visualization' },
      { id: 'activity_log', name: 'Activity Log', description: 'User activity tracking' }
    ]
  },
  {
    name: 'Payment',
    icon: '💳',
    features: [
      { id: 'payment', name: 'Payment Processing', description: 'Stripe or PayPal integration' },
      { id: 'subscription', name: 'Subscriptions', description: 'Recurring payment plans' },
      { id: 'invoicing', name: 'Invoicing', description: 'Automated invoice generation' },
      { id: 'shopping_cart', name: 'Shopping Cart', description: 'E-commerce cart functionality' }
    ]
  },
  {
    name: 'Advanced',
    icon: '⚡',
    features: [
      { id: 'api', name: 'REST API', description: 'RESTful API endpoints', popular: true },
      { id: 'websocket', name: 'WebSocket', description: 'Real-time bidirectional communication' },
      { id: 'background_jobs', name: 'Background Jobs', description: 'Async task processing' },
      { id: 'rate_limiting', name: 'Rate Limiting', description: 'API rate limiting and throttling' }
    ]
  }
]

const filteredCategories = computed(() => {
  if (!searchQuery.value) return featureCategories
  
  const query = searchQuery.value.toLowerCase()
  return featureCategories
    .map(category => ({
      ...category,
      features: category.features.filter(feature =>
        feature.name.toLowerCase().includes(query) ||
        feature.description.toLowerCase().includes(query)
      )
    }))
    .filter(category => category.features.length > 0)
})

const toggleFeature = (featureId) => {
  const index = selectedFeatures.value.indexOf(featureId)
  if (index > -1) {
    selectedFeatures.value.splice(index, 1)
  } else {
    selectedFeatures.value.push(featureId)
  }
}

const handleNext = () => {
  generatorStore.features = selectedFeatures.value
  generatorStore.nextStep()
}
</script>
