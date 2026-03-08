import { createApp } from 'vue'
import App from '../html/App.vue'
import router from './router'
import http, * as api from './api'

const app = createApp(App)

// 配置全局属性
app.config.globalProperties.$http = http
app.config.globalProperties.$api = api

app.use(router)
app.mount('#app')