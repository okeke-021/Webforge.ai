<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
        Style Preferences
      </h2>
      <p class="text-gray-600 dark:text-gray-400">
        Customize the look and feel of your application
      </p>
    </div>

    <!-- Theme Style -->
    <div class="space-y-3">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Design Style</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <button
          v-for="theme in themes"
          :key="theme.id"
          @click="stylePreferences.theme = theme.id"
          :class="[
            'p-4 border-2 rounded-lg transition-all',
            stylePreferences.theme === theme.id
              ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
              : 'border-gray-300 dark:border-gray-600 hover:border-blue-400'
          ]"
        >
          <div class="aspect-video bg-gradient-to-br rounded mb-2" :style="theme.gradient" />
          <h4 class="font-semibold text-gray-900 dark:text-white text-sm">{{ theme.name }}</h4>
        </button>
      </div>
    </div>

    <!-- Color Scheme -->
    <div class="space-y-3">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Color Scheme</h3>
      <div class="grid grid-cols-3 md:grid-cols-6 gap-3">
        <button
          v-for="color in colorSchemes"
          :key="color.id"
          @click="stylePreferences.colorScheme = color.id"
          :class="[
            'p-4 border-2 rounded-lg transition-all',
            stylePreferences.colorScheme === color.id
              ? 'border-2 ring-2 ring-offset-2'
              : 'border-gray-300 dark:border-gray-600'
          ]"
          :style="{ borderColor: color.primary, ringColor: color.primary }"
        >
          <div class="flex space-x-1 mb-2">
            <div class="w-full h-8 rounded" :style="{ backgroundColor: color.primary }" />
          </div>
          <p class="text-xs font-medium text-gray-900 dark:text-white">{{ color.name }}</p>
        </button>
      </div>
    </div>

    <!-- Layout Type -->
    <div class="space-y-3">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Layout Type</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button
          v-for="layout in layouts"
          :key="layout.id"
          @click="stylePreferences.layout = layout.id"
          :class="[
            'p-4 border-2 rounded-lg transition-all text-left',
            stylePreferences.layout === layout.id
              ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
              : 'border-gray-300 dark:border-gray-600 hover:border-blue-400'
          ]"
        >
          <div class="mb-3">
            <div v-html="layout.preview" class="h-20" />
          </div>
          <h4 class="font-semibold text-gray-900 dark:text-white mb-1">{{ layout.name }}</h4>
          <p class="text-xs text-gray-600 dark:text-gray-400">{{ layout.description }}</p>
        </button>
      </div>
    </div>

    <!-- Typography -->
    <div class="space-y-3">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Typography</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <button
          v-for="font in fonts"
          :key="font.id"
          @click="stylePreferences.font = font.id"
          :class="[
            'p-4 border-2 rounded-lg transition-all',
            stylePreferences.font === font.id
              ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
              : 'border-gray-300 dark:border-gray-600 hover:border-blue-400'
          ]"
        >
          <p :style="{ fontFamily: font.family }" class="text-xl font-bold text-gray-900 dark:text-white mb-1">
            Aa
          </p>
          <p class="text-xs text-gray-600 dark:text-gray-400">{{ font.name }}</p>
        </button>
      </div>
    </div>

    <!-- Additional Options -->
    <div class="space-y-3">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Additional Options</h3>
      <div class="space-y-2">
        <label class="flex items-center space-x-3 p-3 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer">
          <input
            v-model="stylePreferences.darkMode"
            type="checkbox"
            class="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
          />
          <div>
            <p class="font-medium text-gray-900 dark:text-white">Dark Mode Support</p>
            <p class="text-xs text-gray-600 dark:text-gray-400">Include dark theme toggle</p>
          </div>
        </label>
        <label class="flex items-center space-x-3 p-3 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer">
          <input
            v-model="stylePreferences.animations"
            type="checkbox"
            class="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
          />
          <div>
            <p class="font-medium text-gray-900 dark:text-white">Animations & Transitions</p>
            <p class="text-xs text-gray-600 dark:text-gray-400">Add smooth animations</p>
          </div>
        </label>
        <label class="flex items-center space-x-3 p-3 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 cursor-pointer">
          <input
            v-model="stylePreferences.accessibility"
            type="checkbox"
            class="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
          />
          <div>
            <p class="font-medium text-gray-900 dark:text-white">Accessibility Features</p>
            <p class="text-xs text-gray-600 dark:text-gray-400">WCAG 2.1 compliant</p>
          </div>
        </label>
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
        Review & Generate
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useGeneratorStore } from '../../stores/generator'

const generatorStore = useGeneratorStore()

const stylePreferences = ref({
  theme: 'modern',
  colorScheme: 'blue',
  layout: 'dashboard',
  font: 'inter',
  darkMode: true,
  animations: true,
  accessibility: true,
  ...generatorStore.stylePreferences
})

const themes = [
  { id: 'modern', name: 'Modern', gradient: 'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
  { id: 'minimal', name: 'Minimal', gradient: 'background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)' },
  { id: 'vibrant', name: 'Vibrant', gradient: 'background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' },
  { id: 'professional', name: 'Professional', gradient: 'background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%)' }
]

const colorSchemes = [
  { id: 'blue', name: 'Blue', primary: '#3B82F6' },
  { id: 'purple', name: 'Purple', primary: '#8B5CF6' },
  { id: 'green', name: 'Green', primary: '#10B981' },
  { id: 'red', name: 'Red', primary: '#EF4444' },
  { id: 'orange', name: 'Orange', primary: '#F59E0B' },
  { id: 'pink', name: 'Pink', primary: '#EC4899' }
]

const layouts = [
  {
    id: 'dashboard',
    name: 'Dashboard',
    description: 'Sidebar with main content area',
    preview: '<div class="flex h-full bg-gray-200 dark:bg-gray-700 rounded"><div class="w-1/4 bg-gray-800"></div><div class="flex-1 bg-white dark:bg-gray-600 m-1 rounded"></div></div>'
  },
  {
    id: 'landing',
    name: 'Landing Page',
    description: 'Hero section with sections',
    preview: '<div class="h-full bg-gray-200 dark:bg-gray-700 rounded"><div class="h-2/3 bg-blue-500"></div><div class="h-1/3 bg-white dark:bg-gray-600"></div></div>'
  },
  {
    id: 'app',
    name: 'Application',
    description: 'Top nav with content grid',
    preview: '<div class="flex flex-col h-full bg-gray-200 dark:bg-gray-700 rounded"><div class="h-1/6 bg-gray-800"></div><div class="flex-1 bg-white dark:bg-gray-600 m-1 rounded"></div></div>'
  }
]

const fonts = [
  { id: 'inter', name: 'Inter', family: 'Inter, sans-serif' },
  { id: 'roboto', name: 'Roboto', family: 'Roboto, sans-serif' },
  { id: 'poppins', name: 'Poppins', family: 'Poppins, sans-serif' },
  { id: 'montserrat', name: 'Montserrat', family: 'Montserrat, sans-serif' }
]

const handleNext = () => {
  generatorStore.stylePreferences = stylePreferences.value
  generatorStore.nextStep()
}
</script>
