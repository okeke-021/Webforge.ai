<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
        Choose Tech Stack
      </h2>
      <p class="text-gray-600 dark:text-gray-400">
        Select the technologies for your application
      </p>
    </div>

    <!-- Frontend Framework -->
    <div class="space-y-3">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
        Frontend Framework
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button
          v-for="framework in frontendFrameworks"
          :key="framework.id"
          @click="selectFrontend(framework.id)"
          :class="[
            'p-6 border-2 rounded-lg transition-all text-left',
            techStack.frontend === framework.id
              ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
              : 'border-gray-300 dark:border-gray-600 hover:border-blue-400'
          ]"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="text-4xl">{{ framework.icon }}</div>
            <span
              v-if="framework.recommended"
              class="px-2 py-1 text-xs bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 rounded"
            >
              Recommended
            </span>
          </div>
          <h4 class="font-bold text-gray-900 dark:text-white mb-1">
            {{ framework.name }}
          </h4>
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">
            {{ framework.description }}
          </p>
          <div class="flex flex-wrap gap-1">
            <span
              v-for="tag in framework.tags"
              :key="tag"
              class="px-2 py-0.5 text-xs bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded"
            >
              {{ tag }}
            </span>
          </div>
        </button>
      </div>
    </div>

    <!-- Backend Framework -->
    <div class="space-y-3">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
        Backend Framework
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button
          v-for="framework in backendFrameworks"
          :key="framework.id"
          @click="selectBackend(framework.id)"
          :class="[
            'p-6 border-2 rounded-lg transition-all text-left',
            techStack.backend === framework.id
              ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
              : 'border-gray-300 dark:border-gray-600 hover:border-blue-400'
          ]"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="text-4xl">{{ framework.icon }}</div>
            <span
              v-if="framework.recommended"
              class="px-2 py-1 text-xs bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 rounded"
            >
              Recommended
            </span>
          </div>
          <h4 class="font-bold text-gray-900 dark:text-white mb-1">
            {{ framework.name }}
          </h4>
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">
            {{ framework.description }}
          </p>
          <div class="flex flex-wrap gap-1">
            <span
              v-for="tag in framework.tags"
              :key="tag"
              class="px-2 py-0.5 text-xs bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded"
            >
              {{ tag }}
            </span>
          </div>
        </button>
      </div>
    </div>

    <!-- Database -->
    <div class="space-y-3">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
        Database
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <button
          v-for="db in databases"
          :key="db.id"
          @click="selectDatabase(db.id)"
          :class="[
            'p-4 border-2 rounded-lg transition-all text-left',
            techStack.database === db.id
              ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
              : 'border-gray-300 dark:border-gray-600 hover:border-blue-400'
          ]"
        >
          <div class="text-3xl mb-2">{{ db.icon }}</div>
          <h4 class="font-bold text-gray-900 dark:text-white text-sm mb-1">
            {{ db.name }}
          </h4>
          <p class="text-xs text-gray-600 dark:text-gray-400">
            {{ db.description }}
          </p>
        </button>
      </div>
    </div>

    <!-- Additional Libraries -->
    <div class="space-y-3">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
        Additional Libraries <span class="text-sm font-normal text-gray-500">(Optional)</span>
      </h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <button
          v-for="lib in additionalLibraries"
          :key="lib.id"
          @click="toggleLibrary(lib.id)"
          :class="[
            'p-3 border rounded-lg transition-all text-left',
            selectedLibraries.includes(lib.id)
              ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
              : 'border-gray-300 dark:border-gray-600 hover:border-blue-400'
          ]"
        >
          <div class="flex items-center justify-between">
            <div>
              <h4 class="font-semibold text-gray-900 dark:text-white text-sm">
                {{ lib.name }}
              </h4>
              <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">
                {{ lib.purpose }}
              </p>
            </div>
            <div
              :class="[
                'w-4 h-4 rounded border-2 flex items-center justify-center flex-shrink-0',
                selectedLibraries.includes(lib.id)
                  ? 'bg-blue-600 border-blue-600'
                  : 'border-gray-300 dark:border-gray-600'
              ]"
            >
              <svg
                v-if="selectedLibraries.includes(lib.id)"
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
        class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
      >
        Next: Style Preferences
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useGeneratorStore } from '../../stores/generator'

const generatorStore = useGeneratorStore()

const techStack = ref({ ...generatorStore.techStack })
const selectedLibraries = ref([])

const frontendFrameworks = [
  {
    id: 'react',
    name: 'React',
    icon: '⚛️',
    description: 'Popular library for building user interfaces',
    tags: ['Components', 'Hooks', 'Virtual DOM'],
    recommended: true
  },
  {
    id: 'vue',
    name: 'Vue.js',
    icon: '💚',
    description: 'Progressive framework for building UIs',
    tags: ['Reactive', 'Easy Learning', 'Composition API'],
    recommended: true
  },
  {
    id: 'angular',
    name: 'Angular',
    icon: '🅰️',
    description: 'Full-featured framework by Google',
    tags: ['TypeScript', 'Enterprise', 'Full Stack']
  },
  {
    id: 'nextjs',
    name: 'Next.js',
    icon: '▲',
    description: 'React framework with SSR and SSG',
    tags: ['SEO', 'Server Rendering', 'File Routing']
  },
  {
    id: 'svelte',
    name: 'Svelte',
    icon: '🔥',
    description: 'Compiler-based framework with no virtual DOM',
    tags: ['Lightweight', 'Fast', 'Simple']
  },
  {
    id: 'vanilla',
    name: 'Vanilla JS',
    icon: '🟨',
    description: 'Pure JavaScript without frameworks',
    tags: ['No Dependencies', 'Lightweight', 'Fast']
  }
]

const backendFrameworks = [
  {
    id: 'nodejs',
    name: 'Node.js + Express',
    icon: '🟢',
    description: 'JavaScript runtime for server-side',
    tags: ['Fast', 'Async', 'JavaScript'],
    recommended: true
  },
  {
    id: 'django',
    name: 'Django',
    icon: '🐍',
    description: 'Python web framework with batteries included',
    tags: ['Python', 'ORM', 'Admin Panel'],
    recommended: true
  },
  {
    id: 'fastapi',
    name: 'FastAPI',
    icon: '⚡',
    description: 'Modern Python framework with automatic docs',
    tags: ['Fast', 'Type Hints', 'Async']
  },
  {
    id: 'nestjs',
    name: 'NestJS',
    icon: '🦅',
    description: 'Progressive Node.js framework',
    tags: ['TypeScript', 'Modular', 'Scalable']
  },
  {
    id: 'rails',
    name: 'Ruby on Rails',
    icon: '💎',
    description: 'Convention over configuration framework',
    tags: ['Ruby', 'MVC', 'Rapid Dev']
  },
  {
    id: 'spring',
    name: 'Spring Boot',
    icon: '🍃',
    description: 'Java framework for enterprise apps',
    tags: ['Java', 'Enterprise', 'Microservices']
  }
]

const databases = [
  {
    id: 'postgresql',
    name: 'PostgreSQL',
    icon: '🐘',
    description: 'Powerful open-source SQL database'
  },
  {
    id: 'mongodb',
    name: 'MongoDB',
    icon: '🍃',
    description: 'NoSQL document database'
  },
  {
    id: 'mysql',
    name: 'MySQL',
    icon: '🐬',
    description: 'Popular open-source SQL database'
  },
  {
    id: 'sqlite',
    name: 'SQLite',
    icon: '💿',
    description: 'Lightweight embedded database'
  }
]

const additionalLibraries = [
  { id: 'tailwind', name: 'Tailwind CSS', purpose: 'Utility-first CSS' },
  { id: 'redux', name: 'Redux', purpose: 'State management' },
  { id: 'graphql', name: 'GraphQL', purpose: 'Query language' },
  { id: 'websocket', name: 'Socket.io', purpose: 'Real-time' },
  { id: 'stripe', name: 'Stripe', purpose: 'Payments' },
  { id: 'aws', name: 'AWS SDK', purpose: 'Cloud services' },
  { id: 'redis', name: 'Redis', purpose: 'Caching' },
  { id: 'docker', name: 'Docker', purpose: 'Containerization' }
]

const selectFrontend = (id) => {
  techStack.value.frontend = id
}

const selectBackend = (id) => {
  techStack.value.backend = id
}

const selectDatabase = (id) => {
  techStack.value.database = id
}

const toggleLibrary = (id) => {
  const index = selectedLibraries.value.indexOf(id)
  if (index > -1) {
    selectedLibraries.value.splice(index, 1)
  } else {
    selectedLibraries.value.push(id)
  }
}

const handleNext = () => {
  techStack.value.additionalLibraries = selectedLibraries.value
  generatorStore.techStack = techStack.value
  generatorStore.nextStep()
}
</script>
