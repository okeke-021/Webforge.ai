<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-8 px-4">
    <div class="max-w-4xl mx-auto">
      <!-- Progress Steps -->
      <div class="mb-8">
        <div class="flex items-center justify-between">
          <div
            v-for="(step, idx) in stepLabels"
            :key="idx"
            class="flex items-center"
            :class="{ 'flex-1': idx < stepLabels.length - 1 }"
          >
            <div class="flex items-center">
              <div
                :class="[
                  'w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all',
                  currentStep > idx + 1
                    ? 'bg-green-500 text-white'
                    : currentStep === idx + 1
                    ? 'bg-blue-600 text-white ring-4 ring-blue-200 dark:ring-blue-900'
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400'
                ]"
              >
                <span v-if="currentStep > idx + 1">✓</span>
                <span v-else>{{ idx + 1 }}</span>
              </div>
              <div
                v-if="idx < stepLabels.length - 1"
                :class="[
                  'ml-4 text-sm font-medium transition-colors',
                  currentStep > idx + 1
                    ? 'text-green-600 dark:text-green-400'
                    : currentStep === idx + 1
                    ? 'text-blue-600 dark:text-blue-400'
                    : 'text-gray-400 dark:text-gray-600'
                ]"
              >
                {{ step }}
              </div>
            </div>
            <div
              v-if="idx < stepLabels.length - 1"
              :class="[
                'flex-1 h-1 mx-4 transition-colors rounded',
                currentStep > idx + 1
                  ? 'bg-green-500'
                  : 'bg-gray-200 dark:bg-gray-700'
              ]"
            />
          </div>
        </div>
      </div>

      <!-- Content -->
      <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
        <component :is="currentComponent" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useGeneratorStore } from '../stores/generator'
import DescriptionInput from '../components/generator/DescriptionInput.vue'
import FeatureSelector from '../components/generator/FeatureSelector.vue'
import TechStackSelector from '../components/generator/TechStackSelector.vue'
import StylePreferences from '../components/generator/StylePreferences.vue'
import GenerationProgress from '../components/generator/GenerationProgress.vue'

const generatorStore = useGeneratorStore()

const currentStep = computed(() => generatorStore.currentStep)

const stepLabels = [
  'Describe',
  'Features',
  'Tech Stack',
  'Style',
  'Generate'
]

const components = {
  1: DescriptionInput,
  2: FeatureSelector,
  3: TechStackSelector,
  4: StylePreferences,
  5: GenerationProgress
}

const currentComponent = computed(() => components[currentStep.value])
</script>
