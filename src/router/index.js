import { createRouter, createWebHistory } from 'vue-router'
import Login from '../../html/Login.vue'
import Register from '../../html/Register.vue'
import Index from '../../html/Index.vue'
import Record from '../../html/Record.vue'
import Profile from '../../html/Profile.vue'
import Users from '../../html/Users.vue'

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
  },
  {
    path: '/users',
    name: 'Users',
    component: Users,
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth) {
    if (!token) {
      alert('请先登录')
      next('/login')
    } else {
      const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
      if (to.meta.requiresAdmin && userInfo.is_admin !== 1) {
        alert('无权限访问')
        next('/index')
      } else {
        next()
      }
    }
  } else {
    next()
  }
})

export default router