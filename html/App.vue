<template>
  <div id="app">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script>
export default {
  name: "App"
};
</script>

<style>
/* 全局重置样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  /* 蓝白色主题色定义 */
  --primary-blue: #2563eb;
  --primary-blue-hover: #1d4ed8;
  --primary-blue-light: #3b82f6;
  --secondary-blue: #60a5fa;
  --accent-blue: #93c5fd;
  --light-blue: #dbeafe;
  --ultra-light-blue: #eff6ff;
  --white: #ffffff;
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
  --success: #10b981;
  --warning: #f59e0b;
  --error: #ef4444;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  --border-radius: 12px;
  --border-radius-lg: 16px;
  --border-radius-sm: 8px;
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  background: linear-gradient(135deg, var(--ultra-light-blue) 0%, var(--white) 100%);
  min-height: 100vh;
  color: var(--gray-800);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  width: 100%;
  min-height: 100vh;
}

/* 通用按钮样式 */
button {
  font-family: inherit;
  cursor: pointer;
  border: none;
  outline: none;
  transition: var(--transition);
  font-size: 14px;
  font-weight: 500;
}

.btn-primary {
  background: var(--primary-blue);
  color: var(--white);
  padding: 12px 24px;
  border-radius: var(--border-radius-sm);
  box-shadow: var(--shadow-md);
}

.btn-primary:hover {
  background: var(--primary-blue-hover);
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.btn-primary:active {
  transform: translateY(0);
  box-shadow: var(--shadow-sm);
}

.btn-secondary {
  background: var(--white);
  color: var(--primary-blue);
  border: 2px solid var(--primary-blue);
  padding: 12px 24px;
  border-radius: var(--border-radius-sm);
}

.btn-secondary:hover {
  background: var(--ultra-light-blue);
  transform: translateY(-2px);
}

.btn-danger {
  background: var(--error);
  color: var(--white);
  padding: 8px 16px;
  border-radius: var(--border-radius-sm);
}

.btn-danger:hover {
  background: #dc2626;
  transform: translateY(-1px);
}

/* 通用输入框样式 */
input[type="text"],
input[type="tel"],
input[type="password"],
input[type="email"] {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid var(--gray-200);
  border-radius: var(--border-radius-sm);
  font-size: 14px;
  transition: var(--transition);
  background: var(--white);
}

input:focus {
  border-color: var(--primary-blue);
  outline: none;
  box-shadow: 0 0 0 3px var(--light-blue);
}

input::placeholder {
  color: var(--gray-400);
}

/* 卡片样式 */
.card {
  background: var(--white);
  border-radius: var(--border-radius);
  padding: 24px;
  box-shadow: var(--shadow-md);
  transition: var(--transition);
}

.card:hover {
  box-shadow: var(--shadow-lg);
}

/* 页面过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* 加载动画 */
.loading {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid var(--light-blue);
  border-radius: 50%;
  border-top-color: var(--primary-blue);
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--gray-100);
}

::-webkit-scrollbar-thumb {
  background: var(--gray-400);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--gray-500);
}

/* 响应式断点 */
@media (max-width: 768px) {
  .card {
    padding: 16px;
  }
  
  button {
    font-size: 13px;
  }
}
</style>