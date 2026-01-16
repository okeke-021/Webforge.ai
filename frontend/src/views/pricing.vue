<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-12 px-4">
    <div class="max-w-7xl mx-auto">
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          Choose Your Plan
        </h1>
        <p class="text-xl text-gray-600 dark:text-gray-400">
          Start free, upgrade as you grow
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
        <!-- Free Plan -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 border border-gray-200 dark:border-gray-700">
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Free</h3>
          <div class="mb-6">
            <span class="text-4xl font-bold text-gray-900 dark:text-white">$0</span>
            <span class="text-gray-600 dark:text-gray-400">/month</span>
          </div>
          <ul class="space-y-4 mb-8">
            <li class="flex items-start">
              <svg class="w-6 h-6 text-green-500 flex-shrink-0 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="text-gray-700 dark:text-gray-300">3 app generations per month</span>
            </li>
            <li class="flex items-start">
              <svg class="w-6 h-6 text-green-500 flex-shrink-0 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="text-gray-700 dark:text-gray-300">5 requests per day</span>
            </li>
            <li class="flex items-start">
              <svg class="w-6 h-6 text-green-500 flex-shrink-0 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="text-gray-700 dark:text-gray-300">All frameworks supported</span>
            </li>
            <li class="flex items-start">
              <svg class="w-6 h-6 text-green-500 flex-shrink-0 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="text-gray-700 dark:text-gray-300">GitHub integration</span>
            </li>
            <li class="flex items-start">
              <svg class="w-6 h-6 text-green-500 flex-shrink-0 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="text-gray-700 dark:text-gray-300">Code validation</span>
            </li>
          </ul>
          <button
            v-if="!isAuthenticated"
            @click="handleSignUp"
            class="w-full px-6 py-3 bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition font-semibold"
          >
            Get Started
          </button>
          <div v-else class="w-full px-6 py-3 bg-gray-100 dark:bg-gray-900 text-gray-600 dark:text-gray-400 rounded-lg text-center font-semibold">
            Current Plan
          </div>
        </div>

        <!-- Pro Plan -->
        <div class="bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl shadow-2xl p-8 transform scale-105 relative">
          <div class="absolute -top-4 left-1/2 transform -translate-x-1/2 bg-yellow-400 text-gray-900 px-4 py-1 rounded-full text-sm font-bold">
            MOST POPULAR
          </div>
          <h3 class="text-2xl font-bold text-white mb-2">Pro</h3>
          <div class="mb-6">
            <span class="text-4xl font-bold text-white">$30</span>
            <span class="text-blue-100">/month</span>
          </div>
          <ul class="space-y-4 mb-8">
            <li class="flex items-start">
              <svg class="w-6 h-6 text-white flex-shrink-0 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="text-white">10 app generations per month</span>
            </li>
            <li class="flex items-start">
              <svg class="w-6 h-6 text-white flex-shrink-0 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="text-white">20 requests per day</span>
            </li>
            <li class="flex items-start">
              <svg class="w-6 h-6 text-white flex-shrink-0 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="text-white">Everything in Free</span>
            </li>
            <li class="flex items-start">
              <svg class="w-6 h-6 text-white flex-shrink-0 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="text-white">Priority generation queue</span>
            </li>
            <li class="flex items-start">
              <svg class="w-6 h-6 text-white flex-shrink-0 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="text-white">Priority support</span>
            </li>
          </ul>
          <button
            class="w-full px-6 py-3 bg-white text-blue-600 rounded-lg hover:bg-gray-100 transition font-semibold"
          >
            Upgrade to Pro
          </button>
        </div>

        <!-- Enterprise Plan -->
        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 border border-gray-200 dark:border-gray-700">
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Enterprise</h3>
          <div class="mb-6">
            <span class="text-4xl font-bold text-gray-900 dark:text-white">$150</span>
            <span class="text-gray-600 dark:text-gray-400">/month</span>
          </div>
          <ul class="space-y-4 mb-8">
            <li class="flex items-start">
              <svg class="w-6 h-6 text-green-500 flex-shrink-0 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="text-gray-700 dark:text-gray-300">20 app generations per month</span>
            </li>
            <li class="flex items-start">
              <svg class="w-6 h-6 text-green-500 flex-shrink-0 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="text-gray-700 dark:text-gray-300">50 requests per day</span>
            </li>
            <li class="flex items-start">
              <svg class="w-6 h-6 text-green-500 flex-shrink-0 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="text-gray-700 dark:text-gray-300">Everything in Pro</span>
            </li>
            <li class="flex items-start">
              <svg class="w-6 h-6 text-green-500 flex-shrink-0 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="text-gray-700 dark:text-gray-300">Debug existing repositories</span>
            </li>
            <li class="flex items-start">
              <svg class="w-6 h-6 text-green-500 flex-shrink-0 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="text-gray-700 dark:text-gray-300">Custom integrations</span>
            </li>
            <li class="flex items-start">
              <svg class="w-6 h-6 text-green-500 flex-shrink-0 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span class="text-gray-700 dark:text-gray-300">Dedicated support</span>
            </li>
          </ul>
          <button
            class="w-full px-6 py-3 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-lg hover:bg-gray-800 dark:hover:bg-gray-100 transition font-semibold"
          >
            Contact Sales
          </button>
        </div>
      </div>

      <!-- FAQ -->
      <div class="mt-16 max-w-3xl mx-auto">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white text-center mb-8">
          Frequently Asked Questions
        </h2>
        <div class="space-y-4">
          <div class="bg-white dark:bg-gray-800 rounded-lg p-6">
            <h3 class="font-semibold text-gray-900 dark:text-white mb-2">
              Can I cancel anytime?
            </h3>
            <p class="text-gray-600 dark:text-gray-400">
              Yes, you can cancel your subscription at any time. You'll continue to have access until the end of your billing period.
            </p>
          </div>
          <div class="bg-white dark:bg-gray-800 rounded-lg p-6">
            <h3 class="font-semibold text-gray-900 dark:text-white mb-2">
              What payment methods do you accept?
            </h3>
            <p class="text-gray-600 dark:text-gray-400">
              We accept all major credit cards through our secure payment processor, Paddle.
            </p>
          </div>
          <div class="bg-white dark:bg-gray-800 rounded-lg p-6">
            <h3 class="font-semibold text-gray-900 dark:text-white mb-2">
              Do unused generations roll over?
            </h3>
            <p class="text-gray-600 dark:text-gray-400">
              No, unused generations reset at the beginning of each billing cycle.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)

const handleSignUp = () => {
  authStore.login()
}
</script>
