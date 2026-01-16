<template>
  <div class="space-y-4">
    <div class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
      <div class="flex items-start space-x-3">
        <svg class="w-5 h-5 text-yellow-600 dark:text-yellow-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
        <div>
          <h4 class="text-sm font-semibold text-yellow-900 dark:text-yellow-200 mb-1">
            Preview Not Available Yet
          </h4>
          <p class="text-sm text-yellow-800 dark:text-yellow-300">
            Live preview requires the application to be deployed. Download the project and run it locally, or push to GitHub and deploy to see it in action.
          </p>
        </div>
      </div>
    </div>

    <!-- Preview Instructions -->
    <div class="bg-white dark:bg-gray-800 rounded-lg p-6 space-y-4">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">How to Preview Your App</h3>
      
      <div class="space-y-3">
        <div class="flex items-start space-x-3">
          <div class="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center flex-shrink-0 font-semibold">
            1
          </div>
          <div>
            <h4 class="font-semibold text-gray-900 dark:text-white mb-1">Download Your Project</h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              Click the "Download ZIP" button above to get all your project files.
            </p>
          </div>
        </div>

        <div class="flex items-start space-x-3">
          <div class="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center flex-shrink-0 font-semibold">
            2
          </div>
          <div>
            <h4 class="font-semibold text-gray-900 dark:text-white mb-1">Install Dependencies</h4>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">
              Extract the ZIP and run:
            </p>
            <pre class="bg-gray-900 text-gray-100 p-3 rounded text-sm overflow-x-auto">
cd {{ project?.name || 'your-project' }}
npm install  # or: pip install -r requirements.txt
            </pre>
          </div>
        </div>

        <div class="flex items-start space-x-3">
          <div class="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center flex-shrink-0 font-semibold">
            3
          </div>
          <div>
            <h4 class="font-semibold text-gray-900 dark:text-white mb-1">Run Development Server</h4>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">
              Start the development server:
            </p>
            <pre class="bg-gray-900 text-gray-100 p-3 rounded text-sm overflow-x-auto">
npm run dev  # or: python manage.py runserver
            </pre>
          </div>
        </div>

        <div class="flex items-start space-x-3">
          <div class="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center flex-shrink-0 font-semibold">
            4
          </div>
          <div>
            <h4 class="font-semibold text-gray-900 dark:text-white mb-1">Open in Browser</h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              Your app will be running at <code class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">http://localhost:3000</code>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Deployment Options -->
    <div class="bg-white dark:bg-gray-800 rounded-lg p-6">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Deploy Your App</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 dark:text-white mb-2">Vercel</h4>
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
            Best for Next.js and React apps
          </p>
          <a
            href="https://vercel.com/new"
            target="_blank"
            class="inline-block px-4 py-2 bg-black text-white rounded text-sm hover:bg-gray-800 transition"
          >
            Deploy to Vercel →
          </a>
        </div>

        <div class="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 dark:text-white mb-2">Netlify</h4>
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
            Great for static sites and SPAs
          </p>
          <a
            href="https://app.netlify.com/start"
            target="_blank"
            class="inline-block px-4 py-2 bg-teal-600 text-white rounded text-sm hover:bg-teal-700 transition"
          >
            Deploy to Netlify →
          </a>
        </div>

        <div class="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
          <h4 class="font-semibold text-gray-900 dark:text-white mb-2">Fly.io</h4>
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">
            Perfect for full-stack apps
          </p>
          <a
            href="https://fly.io/docs/"
            target="_blank"
            class="inline-block px-4 py-2 bg-purple-600 text-white rounded text-sm hover:bg-purple-700 transition"
          >
            Deploy to Fly.io →
          </a>
        </div>
      </div>
    </div>

    <!-- Screenshot Placeholder -->
    <div class="bg-gray-100 dark:bg-gray-900 rounded-lg p-12 text-center">
      <svg class="w-24 h-24 mx-auto text-gray-400 dark:text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
      </svg>
      <p class="text-gray-600 dark:text-gray-400">
        Your app preview will appear here once deployed
      </p>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  project: {
    type: Object,
    required: true
  }
})
</script>
