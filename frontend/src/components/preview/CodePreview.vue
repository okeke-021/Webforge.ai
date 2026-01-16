<template>
  <div class="space-y-4">
    <!-- File Tree -->
    <div class="flex space-x-4">
      <div class="w-64 bg-gray-50 dark:bg-gray-900 rounded-lg p-4 overflow-y-auto max-h-96">
        <h3 class="font-semibold text-gray-900 dark:text-white mb-3">Files</h3>
        <div class="space-y-1">
          <button
            v-for="(content, path) in files"
            :key="path"
            @click="selectFile(path)"
            :class="[
              'w-full text-left px-3 py-2 rounded text-sm transition-colors',
              selectedFile === path
                ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300'
                : 'text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-800'
            ]"
          >
            <div class="flex items-center space-x-2">
              <span>{{ getFileIcon(path) }}</span>
              <span class="truncate">{{ getFileName(path) }}</span>
            </div>
          </button>
        </div>
      </div>

      <!-- Code Display -->
      <div class="flex-1 bg-gray-900 rounded-lg overflow-hidden">
        <div class="bg-gray-800 px-4 py-2 flex items-center justify-between">
          <span class="text-gray-300 text-sm font-mono">{{ selectedFile }}</span>
          <button
            @click="copyCode"
            class="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-gray-200 rounded text-sm transition-colors"
          >
            {{ copied ? '✓ Copied' : 'Copy' }}
          </button>
        </div>
        <div class="overflow-x-auto">
          <pre class="p-4"><code :class="codeLanguage" v-html="highlightedCode"></code></pre>
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-4 gap-4">
      <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
        <p class="text-sm text-gray-600 dark:text-gray-400">Total Files</p>
        <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ Object.keys(files).length }}</p>
      </div>
      <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
        <p class="text-sm text-gray-600 dark:text-gray-400">Lines of Code</p>
        <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ totalLines }}</p>
      </div>
      <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
        <p class="text-sm text-gray-600 dark:text-gray-400">Total Size</p>
        <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ formatSize(totalSize) }}</p>
      </div>
      <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
        <p class="text-sm text-gray-600 dark:text-gray-400">File Types</p>
        <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ fileTypes.size }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import Prism from 'prismjs'
import 'prismjs/components/prism-javascript'
import 'prismjs/components/prism-typescript'
import 'prismjs/components/prism-python'
import 'prismjs/components/prism-jsx'
import 'prismjs/components/prism-css'
import 'prismjs/components/prism-json'
import 'prismjs/components/prism-markdown'

const props = defineProps({
  files: {
    type: Object,
    required: true
  }
})

const selectedFile = ref(Object.keys(props.files)[0] || '')
const copied = ref(false)

const currentFileContent = computed(() => {
  return props.files[selectedFile.value] || ''
})

const codeLanguage = computed(() => {
  const ext = selectedFile.value.split('.').pop()
  const languageMap = {
    'js': 'language-javascript',
    'jsx': 'language-jsx',
    'ts': 'language-typescript',
    'tsx': 'language-tsx',
    'py': 'language-python',
    'vue': 'language-markup',
    'html': 'language-markup',
    'css': 'language-css',
    'json': 'language-json',
    'md': 'language-markdown'
  }
  return languageMap[ext] || 'language-markup'
})

const highlightedCode = computed(() => {
  const lang = codeLanguage.value.replace('language-', '')
  if (Prism.languages[lang]) {
    return Prism.highlight(currentFileContent.value, Prism.languages[lang], lang)
  }
  return currentFileContent.value
})

const totalLines = computed(() => {
  return Object.values(props.files).reduce((sum, content) => {
    return sum + content.split('\n').length
  }, 0)
})

const totalSize = computed(() => {
  return Object.values(props.files).reduce((sum, content) => {
    return sum + new Blob([content]).size
  }, 0)
})

const fileTypes = computed(() => {
  const types = new Set()
  Object.keys(props.files).forEach(path => {
    const ext = path.split('.').pop()
    types.add(ext)
  })
  return types
})

const selectFile = (path) => {
  selectedFile.value = path
}

const getFileName = (path) => {
  return path.split('/').pop()
}

const getFileIcon = (path) => {
  const ext = path.split('.').pop()
  const icons = {
    'js': '📜',
    'jsx': '⚛️',
    'ts': '📘',
    'tsx': '⚛️',
    'py': '🐍',
    'vue': '💚',
    'html': '🌐',
    'css': '🎨',
    'json': '📋',
    'md': '📝',
    'txt': '📄'
  }
  return icons[ext] || '📄'
}

const formatSize = (bytes) => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

const copyCode = async () => {
  try {
    await navigator.clipboard.writeText(currentFileContent.value)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy:', err)
  }
}

watch(() => props.files, () => {
  if (!selectedFile.value || !props.files[selectedFile.value]) {
    selectedFile.value = Object.keys(props.files)[0] || ''
  }
})
</script>
