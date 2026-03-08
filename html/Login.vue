<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="logo-wrapper">
          <svg class="logo-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h1 class="login-title">葡萄叶部病害识别系统</h1>
        <p class="login-subtitle">欢迎登录，开始智能识别</p>
      </div>

      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="phone">手机号</label>
          <div class="input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 10.999H22C22 5.869 18.127 2 12.99 2V4C17.052 4 20 6.943 20 10.999Z" fill="currentColor"/>
              <path d="M13 8.00024C15.103 8.00024 16 8.89724 16 11.0002H18C18 7.77524 16.225 6.00024 13 6.00024V8.00024ZM16.422 13.4432C16.2299 13.2686 15.9774 13.1754 15.7178 13.1835C15.4583 13.1915 15.212 13.3001 15.031 13.4862L12.638 15.9472C12.062 15.8372 10.904 15.4762 9.71204 14.2872C8.52004 13.0942 8.15904 11.9332 8.05204 11.3612L10.511 8.96724C10.6975 8.78637 10.8062 8.54005 10.8142 8.2805C10.8222 8.02095 10.7289 7.76852 10.554 7.57624L6.85904 3.51324C6.68408 3.32059 6.44092 3.20374 6.18119 3.18725C5.92146 3.17076 5.66564 3.25591 5.46804 3.42424L3.29804 5.28724C3.12515 5.46075 3.02196 5.69169 3.00804 5.93624C2.99304 6.18624 2.70704 12.1082 7.29904 16.7022C11.305 20.7072 16.323 21.0002 17.705 21.0002C17.907 21.0002 18.031 20.9942 18.064 20.9922C18.3085 20.9786 18.5394 20.8747 18.712 20.7012L20.572 18.5302C20.7405 18.3328 20.8256 18.0772 20.8093 17.8177C20.7929 17.5581 20.6762 17.3151 20.484 17.1402L16.422 13.4432Z" fill="currentColor"/>
            </svg>
            <input 
              id="phone"
              type="tel" 
              v-model="Phone" 
              placeholder="请输入手机号" 
              required 
              :disabled="loading"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <div class="input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 14.5V16.5M7 10.0288C7.47142 10 8.05259 10 8.8 10H15.2C15.9474 10 16.5286 10 17 10.0288M7 10.0288C6.41168 10.0647 5.99429 10.1455 5.63803 10.327C5.07354 10.6146 4.6146 11.0735 4.32698 11.638C4 12.2798 4 13.1198 4 14.8V16.2C4 17.8802 4 18.7202 4.32698 19.362C4.6146 19.9265 5.07354 20.3854 5.63803 20.673C6.27976 21 7.11984 21 8.8 21H15.2C16.8802 21 17.7202 21 18.362 20.673C18.9265 20.3854 19.3854 19.9265 19.673 19.362C20 18.7202 20 17.8802 20 16.2V14.8C20 13.1198 20 12.2798 19.673 11.638C19.3854 11.0735 18.9265 10.6146 18.362 10.327C18.0057 10.1455 17.5883 10.0647 17 10.0288M7 10.0288V8C7 5.23858 9.23858 3 12 3C14.7614 3 17 5.23858 17 8V10.0288" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <input 
              id="password"
              type="password" 
              v-model="Password" 
              placeholder="请输入密码（至少6位）" 
              required 
              minlength="6"
              :disabled="loading"
            />
          </div>
        </div>

        <button type="submit" class="btn-login btn-primary" :disabled="loading">
          <span v-if="!loading">登录</span>
          <span v-else class="loading-text">
            <span class="loading"></span>
            登录中...
          </span>
        </button>

        <div class="login-footer">
          <span class="footer-text">还没有账号？</span>
          <router-link to="/register" class="register-link">立即注册</router-link>
        </div>
      </form>
    </div>

    <div class="background-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      Phone: "",
      Password: "",
      loading: false
    };
  },
  methods: {
    async login() {
      if (this.loading) return;
      
      // 验证手机号格式
      const phoneRegex = /^1[3-9]\d{9}$/;
      if (!phoneRegex.test(this.Phone)) {
        alert("请输入正确的手机号");
        return;
      }
      
      // 验证密码长度
      if (this.Password.length < 6) {
        alert("密码至少需要6位");
        return;
      }
      
      this.loading = true;
      try {
  // 注意：去掉拦截器的转换，直接获取后端原生响应
  const response = await this.$api.login({
    Phone: this.Phone,
    Password: this.Password
  });

  // 【关键修改】直接判断后端的 code 字段
  if (response.code !== 200) { // 后端 code=200 才是成功
    alert(response.msg || "登录失败");
    return;
  }

  // 保存 token 和用户信息（注意取 response.data 而非 response.data.data）
  if (response.data && response.data.token) {
    localStorage.setItem('token', response.data.token);
  }
  if (response.data && response.data.userInfo) {
    localStorage.setItem('userInfo', JSON.stringify(response.data.userInfo));
  }

  // 跳转到主页
  this.$router.push('/index');
} catch (error) {
  // 处理真正的请求错误（如网络错误、404、500 等）
  const errorMsg = error.response?.data?.msg || error.message || "登录失败，请检查您的账号和密码";
  alert(errorMsg);
} finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.login-card {
  background: var(--white);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-xl);
  padding: 48px;
  width: 100%;
  max-width: 440px;
  position: relative;
  z-index: 10;
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
  border-radius: var(--border-radius);
  margin-bottom: 20px;
  box-shadow: var(--shadow-lg);
}

.logo-icon {
  width: 36px;
  height: 36px;
  color: var(--white);
}

.login-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: 8px;
  letter-spacing: -0.5px;
}

.login-subtitle {
  font-size: 14px;
  color: var(--gray-500);
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: var(--gray-700);
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 14px;
  width: 20px;
  height: 20px;
  color: var(--gray-400);
  pointer-events: none;
  transition: var(--transition);
}

.input-wrapper input {
  padding-left: 44px;
}

.input-wrapper input:focus + .input-icon,
.input-wrapper:focus-within .input-icon {
  color: var(--primary-blue);
}

.input-wrapper input:disabled {
  background: var(--gray-50);
  cursor: not-allowed;
}

.btn-login {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  margin-top: 8px;
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none !important;
}

.loading-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.login-footer {
  text-align: center;
  margin-top: 8px;
}

.footer-text {
  font-size: 14px;
  color: var(--gray-600);
}

.register-link {
  color: var(--primary-blue);
  text-decoration: none;
  font-weight: 500;
  margin-left: 4px;
  transition: var(--transition);
}

.register-link:hover {
  color: var(--primary-blue-hover);
  text-decoration: underline;
}

/* 背景装饰 */
.background-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 1;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
  opacity: 0.1;
  animation: float 20s ease-in-out infinite;
}

.circle-1 {
  width: 300px;
  height: 300px;
  top: -150px;
  right: -100px;
  animation-delay: 0s;
}

.circle-2 {
  width: 200px;
  height: 200px;
  bottom: -100px;
  left: -50px;
  animation-delay: 3s;
}

.circle-3 {
  width: 150px;
  height: 150px;
  top: 50%;
  left: -75px;
  animation-delay: 6s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-30px) scale(1.05);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-card {
    padding: 32px 24px;
  }

  .login-title {
    font-size: 24px;
  }

  .circle-1 {
    width: 200px;
    height: 200px;
  }

  .circle-2 {
    width: 150px;
    height: 150px;
  }

  .circle-3 {
    width: 100px;
    height: 100px;
  }
}
</style>