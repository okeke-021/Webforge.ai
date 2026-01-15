<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero bg-gradient-to-br from-blue-600 to-purple-700 text-white py-20 px-4">
      <div class="max-w-6xl mx-auto text-center">
        <h1 class="text-5xl md:text-7xl font-bold mb-6 animate-fade-in">
          WebForge.ai
        </h1>
        <p class="text-xl md:text-2xl mb-8 text-blue-100">
          Describe your app, get a complete GitHub repository in minutes
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            v-if="!isAuthenticated"
            @click="handleGetStarted"
            class="px-8 py-4 bg-white text-blue-600 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-all transform hover:scale-105 shadow-lg"
          >
            Get Started Free
          </button>
          <button
            v-else
            @click="$router.push('/generator')"
            class="px-8 py-4 bg-white text-blue-600 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-all transform hover:scale-105 shadow-lg"
          >
            Start Building
          </button>
          <button
            @click="scrollToFeatures"
            class="px-8 py-4 bg-transparent border-2 border-white text-white rounded-lg font-semibold text-lg hover:bg-white hover:text-blue-600 transition-all"
          >
            Learn More
          </button>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-20 px-4 bg-white dark:bg-gray-800">
      <div class="max-w-6xl mx-auto">
        <h2 class="text-4xl font-bold text-center mb-12 text-gray-900 dark:text-white">
          Powerful Features
        </h2>
        <div class="grid md:grid-cols-3 gap-8">
          <div v-for="feature in features" :key="feature.title" 
               class="p-6 rounded-xl bg-gray-50 dark:bg-gray-700 hover:shadow-xl transition-shadow">
            <div class="text-4xl mb-4">{{ feature.icon }}</div>
            <h3 class="text-xl font-semibold mb-3 text-gray-900 dark:text-white">
              {{ feature.title }}
            </h3>
            <p class="text-gray-600 dark:text-gray-300">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="py-20 px-4 bg-gray-50 dark:bg-gray-900">
      <div class="max-w-6xl mx-auto">
        <h2 class="text-4xl font-bold text-center mb-12 text-gray-900 dark:text-white">
          How It Works
        </h2>
        <div class="grid md:grid-cols-4 gap-6">
          <div v-for="(step, idx) in steps" :key="idx" class="text-center">
            <div class="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
              {{ idx + 1 }}
            </div>
            <h3 class="text-lg font-semibold mb-2 text-gray-900 dark:text-white">
              {{ step.title }}
            </h3>
            <p class="text-gray-600 dark:text-gray-300">{{ step.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 px-4 bg-gradient-to-r from-purple-600 to-blue-600 text-white">
      <div class="max-w-4xl mx-auto text-center">
        <h2 class="text-4xl font-bold mb-6">Ready to build your app?</h2>
        <p class="text-xl mb-8">Start generating production-ready code in minutes</p>
        <button
          @click="handleGetStarted"
          class="px-8 py-4 bg-white text-blue-600 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-all transform hover:scale-105 shadow-lg"
        >
          Start Building Now
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)

const features = [
  {
    icon: '🚀',
    title: 'AI-Powered Generation',
    description: 'Advanced AI analyzes your requirements and generates complete, production-ready codebases.'
  },
  {
    icon: '🎨',
    title: 'Multi-Framework Support',
    description: 'Support for React, Vue, Angular, Next.js, Django, Node.js, and more.'
  },
  {
    icon: '📦',
    title: 'GitHub Integration',
    description: 'Automatic repository creation and code commits to your GitHub account.'
  },
  {
    icon: '👀',
    title: 'Live Preview',
    description: 'Interactive preview of your generated app before deployment.'
  },
  {
    icon: '🔒',
    title: 'Secure & Validated',
    description: 'All generated code is validated, tested, and scanned for vulnerabilities.'
  },
  {
    icon: '⚡',
    title: 'Real-Time Updates',
    description: 'Watch your app being built with live progress tracking and updates.'
  }
]

const steps = [
  {
    title: 'Describe',
    description: 'Tell us what app you want to build in natural language.'
  },
  {
    title: 'Configure',
    description: 'Select your tech stack, features, and styling preferences.'
  },
  {
    title: 'Generate',
    description: 'AI generates your complete codebase with validation.'
  },
  {
    title: 'Deploy',
    description: 'Push to GitHub and deploy with one click.'
  }
]

function handleGetStarted() {
  if (isAuthenticated.value) {
    router.push('/generator')
  } else {
    authStore.login()
  }
}

function scrollToFeatures() {
  document.getElementById('features')?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.8s ease-out;
}
</style>
