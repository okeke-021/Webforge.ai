<template>
  <div id="app" :class="{ 'dark': isDark }">
    <Header />
    <main class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      <RouterView />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { RouterView } from 'vue-router'
import { useThemeStore } from './stores/theme'
import Header from './components/common/Header.vue'
import Footer from './components/common/Footer.vue'

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

// Initialize theme from localStorage
themeStore.initTheme()
</script>

<style>
@import 'prismjs/themes/prism-tomorrow.css';

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
