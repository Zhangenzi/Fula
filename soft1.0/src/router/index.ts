import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/auth/Login.vue'
import Register from '../views/auth/Register.vue'
import Home from '../views/interview/Home.vue'
import Interview from '../views/interview/Interview.vue'
import History from '../views/interview/History.vue'
import Profile from '../views/user/Profile.vue'
import Analysis from '../views/user/Analysis.vue'
import Tips from '../views/user/Tips.vue'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { requiresGuest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: { requiresGuest: true }
    },
    {
      path: '/home',
      name: 'home',
      component: Home,
      meta: { requiresAuth: true }
    },
    {
      path: '/interview/:id',
      name: 'interview',
      component: Interview,
      meta: { requiresAuth: true }
    },
    {
      path: '/history',
      name: 'history',
      component: History,
      meta: { requiresAuth: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
      meta: { requiresAuth: true }
    },
    {
      path: '/analysis',
      name: 'analysis',
      component: Analysis,
      meta: { requiresAuth: true }
    },
    {
      path: '/tips',
      name: 'tips',
      component: Tips,
      meta: { requiresAuth: true }
    }
  ]
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  // 初始化认证状态
  if (userStore.token && !userStore.isLoggedIn) {
    await userStore.initializeAuth()
  }

  // 检查需要认证的路由
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
    return
  }

  // 检查需要游客状态的路由（登录、注册页面）
  if (to.meta.requiresGuest && userStore.isLoggedIn) {
    next('/home')
    return
  }

  next()
})

export default router
