import { createRouter, createWebHistory } from 'vue-router'
import Login from '../../html/Login.vue'
import Register from '../../html/Register.vue'
import Index from '../../html/Index.vue'
import Record from '../../html/Record.vue'
import Profile from '../../html/Profile.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false }
  },
  {
    path: '/index',
    name: 'Index',
    component: Index,
    meta: { requiresAuth: true }
  },
  {
    path: '/record',
    name: 'Record',
    component: Record,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 导航守卫：检查登录状态
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  // 如果路由需要认证
  if (to.meta.requiresAuth) {
    if (!token) {
      // 未登录，提示并跳转到登录页
      alert('请先登录')
      next('/login')
    } else {
      // 已登录，允许访问
      next()
    }
  } else {
    // 不需要认证的路由（如登录、注册），直接访问
    next()
  }
})

export default router