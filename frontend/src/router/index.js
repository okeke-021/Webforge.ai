import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Home from '../views/Home.vue'
import Generator from '../views/Generator.vue'
import Results from '../views/Results.vue'
import Dashboard from '../views/Dashboard.vue'
import Pricing from '../views/Pricing.vue'
import DebugRepository from '../views/DebugRepository.vue'
import AuthCallback from '../components/auth/AuthCallback.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: false }
  },
  {
    path: '/generator',
    name: 'Generator',
    component: Generator,
    meta: { requiresAuth: true }
  },
  {
    path: '/results/:projectId',
    name: 'Results',
    component: Results,
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/debug',
    name: 'DebugRepository',
    component: DebugRepository,
    meta: { requiresAuth: true, requiresEnterprise: true }
  },
  {
    path: '/pricing',
    name: 'Pricing',
    component: Pricing,
    meta: { requiresAuth: false }
  },
  {
    path: '/auth/callback',
    name: 'AuthCallback',
    component: AuthCallback,
    meta: { requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0 }
  }
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  if (!authStore.initialized) {
    await authStore.checkAuth()
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Home', query: { redirect: to.fullPath } })
  } else if (to.meta.requiresEnterprise && authStore.subscription !== 'enterprise') {
    next({ name: 'Pricing' })
  } else {
    next()
  }
})

export default router
