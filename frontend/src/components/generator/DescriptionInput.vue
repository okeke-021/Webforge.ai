<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
        Describe Your App
      </h2>
      <p class="text-gray-600 dark:text-gray-400">
        Tell us what you want to build. Be as detailed as possible for best results.
      </p>
    </div>

    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          App Name
        </label>
        <input
          v-model="appName"
          type="text"
          placeholder="e.g., Task Manager Pro"
          class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          @input="updateDescription"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Description
          <span class="text-gray-500 text-xs ml-2">{{ description.length }}/2000 characters</span>
        </label>
        <textarea
          v-model="description"
          rows="8"
          maxlength="2000"
          placeholder="Describe your app in detail. Include:
- What problem does it solve?
- Who are the users?
- What are the main features?
- Any specific requirements?

Example: A task management application for teams to collaborate on projects. Users can create tasks, assign them to team members, set deadlines, and track progress. Features include real-time updates, file attachments, comments, and analytics dashboard."
          class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white resize-none"
          @input="updateDescription"
        />
      </div>

      <!-- Quick Prompts -->
      <div>
        <p class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
          Quick Start Templates
        </p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <button
            v-for="template in templates"
            :key="template.name"
            @click="applyTemplate(template)"
            class="p-4 text-left border border-gray-300 dark:border-gray-600 rounded-lg hover:border-blue-500 dark:hover:border-blue-400 hover:bg-blue-50 dark:hover:bg-gray-700 transition"
          >
            <div class="flex items-start space-x-3">
              <span class="text-2xl">{{ template.icon }}</span>
              <div>
                <h4 class="font-semibold text-gray-900 dark:text-white text-sm">
                  {{ template.name }}
                </h4>
                <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">
                  {{ template.shortDesc }}
                </p>
              </div>
            </div>
          </button>
        </div>
      </div>

      <!-- AI Suggestions -->
      <div v-if="showSuggestions" class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <div class="flex items-start space-x-2">
          <svg class="w-5 h-5 text-blue-600 dark:text-blue-400 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
          </svg>
          <div class="flex-1">
            <p class="text-sm font-medium text-blue-900 dark:text-blue-300">
              AI Suggestions
            </p>
            <ul class="mt-2 space-y-1 text-sm text-blue-800 dark:text-blue-400">
              <li>• Add more details about user authentication requirements</li>
              <li>• Specify the target platform (web, mobile, or both)</li>
              <li>• Mention any third-party integrations needed</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <div class="flex justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
      <button
        @click="$router.push('/')"
        class="px-6 py-3 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition"
      >
        Cancel
      </button>
      <button
        @click="handleNext"
        :disabled="!isValid"
        class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
      >
        Next: Select Features
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useGeneratorStore } from '../../stores/generator'

const generatorStore = useGeneratorStore()

const appName = ref('')
const description = ref(generatorStore.description || '')

const templates = [
  {
    name: 'E-commerce Store',
    icon: '🛍️',
    shortDesc: 'Online shopping platform',
    description: 'An e-commerce platform where users can browse products, add items to cart, make purchases, and track orders. Features include product search, filtering, user reviews, and payment processing.'
  },
  {
    name: 'Social Media Dashboard',
    icon: '📱',
    shortDesc: 'Social network interface',
    description: 'A social media application where users can create profiles, post updates, follow other users, like and comment on posts, and send direct messages. Features include real-time notifications and media uploads.'
  },
  {
    name: 'Project Management',
    icon: '📊',
    shortDesc: 'Team collaboration tool',
    description: 'A project management tool for teams to organize tasks, set deadlines, assign responsibilities, and track progress. Features include kanban boards, gantt charts, time tracking, and team chat.'
  },
  {
    name: 'Blog Platform',
    icon: '✍️',
    shortDesc: 'Content publishing system',
    description: 'A blogging platform where users can write and publish articles, manage drafts, add images, categorize content, and engage with readers through comments. Features include markdown support and SEO optimization.'
  }
]

const showSuggestions = computed(() => {
  return description.value.length > 50 && description.value.length < 200
})

const isValid = computed(() => {
  return description.value.trim().length >= 50
})

const applyTemplate = (template) => {
  appName.value = template.name
  description.value = template.description
  updateDescription()
}

const updateDescription = () => {
  generatorStore.description = description.value
}

const handleNext = () => {
  if (isValid.value) {
    generatorStore.nextStep()
  }
}

watch(() => generatorStore.description, (newVal) => {
  if (newVal !== description.value) {
    description.value = newVal
  }
})
</script>
