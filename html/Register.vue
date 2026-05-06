<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <div class="logo-wrapper">
          <svg class="logo-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h1 class="register-title">葡萄叶部病害识别系统</h1>
        <p class="register-subtitle">注册新账号,开始使用</p>
      </div>

      <form @submit.prevent="register" class="register-form">
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
              v-model="phone" 
              placeholder="请输入手机号" 
              required 
              pattern="^1[3-9]\d{9}$"
              :disabled="loading"
              @input="validatePhone"
            />
          </div>
          <span v-if="phoneError" class="error-message">{{ phoneError }}</span>
        </div>

        <!-- Deleted:<div class="form-group"> -->
        <!-- Deleted:<label for="code">验证码</label> -->
        <!-- Deleted:<div class="input-wrapper code-wrapper"> -->
        <!-- Deleted:<svg class="input-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"> -->
        <!-- Deleted:<path d="M9 12H15M9 16H15M17 21H7C5.89543 21 5 20.1046 5 19V5C5 3.89543 5.89543 3 7 3H12.5858C12.851 3 13.1054 3.10536 13.2929 3.29289L18.7071 8.70711C18.8946 8.89464 19 9.149 19 9.41421V19C19 20.1046 18.1046 21 17 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/> -->
        <!-- Deleted:</svg> -->
        <!-- Deleted:<input  -->
        <!-- Deleted:id="code" -->
        <!-- Deleted:type="text"  -->
        <!-- Deleted:v-model="code"  -->
        <!-- Deleted:placeholder="请输入验证码"  -->
        <!-- Deleted:required  -->
        <!-- Deleted:maxlength="6" -->
        <!-- Deleted:pattern="\d{6}" -->
        <!-- Deleted::disabled="loading" -->
        <!-- Deleted:/> -->
        <!-- Deleted:<button  -->
        <!-- Deleted:type="button"  -->
        <!-- Deleted:class="btn-code" -->
        <!-- Deleted:@click="sendCode" -->
        <!-- Deleted::disabled="!canSendCode || countdown > 0 || loading" -->
        <!-- Deleted:> -->
        <!-- Deleted:{{ countdown > 0 ? `${countdown}秒后重试` : '获取验证码' }} -->
        <!-- Deleted:</button> -->
        <!-- Deleted:</div> -->
        <!-- Deleted:<span v-if="codeError" class="error-message">{{ codeError }}</span> -->
        <!-- Deleted:</div> -->

        <div class="form-group">
          <label for="password">密码</label>
          <div class="input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 14.5V16.5M7 10.0288C7.47142 10 8.05259 10 8.8 10H15.2C15.9474 10 16.5286 10 17 10.0288M7 10.0288C6.41168 10.0647 5.99429 10.1455 5.63803 10.327C5.07354 10.6146 4.6146 11.0735 4.32698 11.638C4 12.2798 4 13.1198 4 14.8V16.2C4 17.8802 4 18.7202 4.32698 19.362C4.6146 19.9265 5.07354 20.3854 5.63803 20.673C6.27976 21 7.11984 21 8.8 21H15.2C16.8802 21 17.7202 21 18.362 20.673C18.9265 20.3854 19.3854 19.9265 19.673 19.362C20 18.7202 20 17.8802 20 16.2V14.8C20 13.1198 20 12.2798 19.673 11.638C19.3854 11.0735 18.9265 10.6146 18.362 10.327C18.0057 10.1455 17.5883 10.0647 17 10.0288M7 10.0288V8C7 5.23858 9.23858 3 12 3C14.7614 3 17 5.23858 17 8V10.0288" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <input
              id="password"
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="请输入密码（至少6位）"
              required
              minlength="6"
              :disabled="loading"
              @input="validatePassword"
            />
            <button
              type="button"
              class="btn-toggle-password"
              @click="showPassword = !showPassword"
              :disabled="loading"
            >
              <svg v-if="!showPassword" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M15 12C15 13.6569 13.6569 15 12 15C10.3431 15 9 13.6569 9 12C9 10.3431 10.3431 9 12 9C13.6569 9 15 10.3431 15 12Z" stroke="currentColor" stroke-width="2"/>
                <path d="M12 5C7 5 2.73 8.11 1 12.5C2.73 16.89 7 20 12 20C17 20 21.27 16.89 23 12.5C21.27 8.11 17 5 12 5Z" stroke="currentColor" stroke-width="2"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 3L21 21M10.5 10.677C10.0332 11.1233 9.75 11.7369 9.75 12.4167C9.75 13.8584 10.9499 15.0417 12.4286 15.0417C13.1173 15.0417 13.7383 14.7628 14.1906 14.3047M7.36205 7.5238C5.68007 8.6894 4.27665 10.3037 3.27148 12.2329C4.87837 15.5433 8.40204 17.8333 12.4286 17.8333C14.0067 17.8333 15.4943 17.4383 16.8095 16.7353M19.8739 16.9429C21.0688 15.7337 22.0242 14.2735 22.6571 12.6425C21.05 9.33194 17.5264 7.04167 13.5 7.04167C12.8916 7.04167 12.2959 7.09583 11.7188 7.19917" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <span v-if="passwordError" class="error-message">{{ passwordError }}</span>
        </div>

        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <div class="input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 14.5V16.5M7 10.0288C7.47142 10 8.05259 10 8.8 10H15.2C15.9474 10 16.5286 10 17 10.0288M7 10.0288C6.41168 10.0647 5.99429 10.1455 5.63803 10.327C5.07354 10.6146 4.6146 11.0735 4.32698 11.638C4 12.2798 4 13.1198 4 14.8V16.2C4 17.8802 4 18.7202 4.32698 19.362C4.6146 19.9265 5.07354 20.3854 5.63803 20.673C6.27976 21 7.11984 21 8.8 21H15.2C16.8802 21 17.7202 21 18.362 20.673C18.9265 20.3854 19.3854 19.9265 19.673 19.362C20 18.7202 20 17.8802 20 16.2V14.8C20 13.1198 20 12.2798 19.673 11.638C19.3854 11.0735 18.9265 10.6146 18.362 10.327C18.0057 10.1455 17.5883 10.0647 17 10.0288M7 10.0288V8C7 5.23858 9.23858 3 12 3C14.7614 3 17 5.23858 17 8V10.0288" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <input
              id="confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              v-model="confirmPassword"
              placeholder="请再次输入密码"
              required
              minlength="6"
              :disabled="loading"
              @input="validateConfirmPassword"
            />
            <button
              type="button"
              class="btn-toggle-password"
              @click="showConfirmPassword = !showConfirmPassword"
              :disabled="loading"
            >
              <svg v-if="!showConfirmPassword" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M15 12C15 13.6569 13.6569 15 12 15C10.3431 15 9 13.6569 9 12C9 10.3431 10.3431 9 12 9C13.6569 9 15 10.3431 15 12Z" stroke="currentColor" stroke-width="2"/>
                <path d="M12 5C7 5 2.73 8.11 1 12.5C2.73 16.89 7 20 12 20C17 20 21.27 16.89 23 12.5C21.27 8.11 17 5 12 5Z" stroke="currentColor" stroke-width="2"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 3L21 21M10.5 10.677C10.0332 11.1233 9.75 11.7369 9.75 12.4167C9.75 13.8584 10.9499 15.0417 12.4286 15.0417C13.1173 15.0417 13.7383 14.7628 14.1906 14.3047M7.36205 7.5238C5.68007 8.6894 4.27665 10.3037 3.27148 12.2329C4.87837 15.5433 8.40204 17.8333 12.4286 17.8333C14.0067 17.8333 15.4943 17.4383 16.8095 16.7353M19.8739 16.9429C21.0688 15.7337 22.0242 14.2735 22.6571 12.6425C21.05 9.33194 17.5264 7.04167 13.5 7.04167C12.8916 7.04167 12.2959 7.09583 11.7188 7.19917" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <span v-if="confirmPasswordError" class="error-message">{{ confirmPasswordError }}</span>
        </div>

        <button type="submit" class="btn-register btn-primary" :disabled="loading || !isFormValid">
          <span v-if="!loading">注册</span>
          <span v-else class="loading-text">
            <span class="loading"></span>
            注册中...
          </span>
        </button>

        <div class="register-footer">
          <span class="footer-text">已有账号？</span>
          <router-link to="/login" class="login-link">立即登录</router-link>
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
      phone: "",
      password: "",
      confirmPassword: "",
      loading: false,
      phoneError: "",
      passwordError: "",
      confirmPasswordError: "",
      showPassword: false,
      showConfirmPassword: false
    };
  },
  computed: {
    canSendCode() {
      const phoneRegex = /^1[3-9]\d{9}$/;
      return phoneRegex.test(this.phone);
    },
    isFormValid() {
      return (
        this.canSendCode &&
        this.password.length >= 6 &&
        this.password === this.confirmPassword &&
        !this.phoneError &&
        !this.passwordError &&
        !this.confirmPasswordError
      );
    }
  },
  methods: {
    validatePhone() {
      const phoneRegex = /^1[3-9]\d{9}$/;
      if (this.phone && !phoneRegex.test(this.phone)) {
        this.phoneError = "请输入有效的手机号";
      } else {
        this.phoneError = "";
      }
    },
    validatePassword() {
      if (this.password && this.password.length < 6) {
        this.passwordError = "密码至少需要6位";
      } else {
        this.passwordError = "";
      }
      // 同时验证确认密码
      if (this.confirmPassword) {
        this.validateConfirmPassword();
      }
    },
    validateConfirmPassword() {
      if (this.confirmPassword && this.confirmPassword !== this.password) {
        this.confirmPasswordError = "两次输入的密码不一致";
      } else {
        this.confirmPasswordError = "";
      }
    },
    async register() {
  if (this.loading || !this.isFormValid) return;

  this.loading = true;
  try {
    await this.$api.register({
      phone: this.phone,
      password: this.password,
      repeat_password: this.password
    });
    
    alert("注册成功！即将跳转到登录页");
    // 注册成功后跳转到登录页
    setTimeout(() => {
      this.$router.push('/login');
    }, 1000);
  } catch (error) {
    // 适配 FastAPI 不同的错误返回格式
    let errorMsg = "注册失败，请检查您的信息";
    
    // 1. 优先获取 FastAPI 直接返回的 detail 字段
    if (error.response?.data?.detail) {
      errorMsg = error.response.data.detail;
    }
    // 2. 兼容 Pydantic 校验的数组格式错误（如：手机号格式有误）
    else if (error.response?.data?.detail && Array.isArray(error.response.data.detail)) {
      errorMsg = error.response.data.detail[0]?.msg || errorMsg;
    }
    // 3. 兼容自定义的 message 字段（备用）
    else if (error.response?.data?.message) {
      errorMsg = error.response.data.message;
    }
    
    alert(errorMsg); // 此时会正确显示后端返回的失败原因
  } finally {
    this.loading = false;
  }
}
  }
};
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.register-card {
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

.register-header {
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

.register-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: 8px;
  letter-spacing: -0.5px;
}

.register-subtitle {
  font-size: 14px;
  color: var(--gray-500);
  margin: 0;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
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





.btn-toggle-password {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  padding: 4px;
  cursor: pointer;
  color: var(--gray-400);
  transition: var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-toggle-password svg {
  width: 20px;
  height: 20px;
}

.btn-toggle-password:hover:not(:disabled) {
  color: var(--primary-blue);
}

.btn-toggle-password:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-message {
  font-size: 12px;
  color: var(--error);
  margin-top: -4px;
}

.btn-register {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  margin-top: 8px;
}

.btn-register:disabled {
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

.register-footer {
  text-align: center;
  margin-top: 8px;
}

.footer-text {
  font-size: 14px;
  color: var(--gray-600);
}

.login-link {
  color: var(--primary-blue);
  text-decoration: none;
  font-weight: 500;
  margin-left: 4px;
  transition: var(--transition);
}

.login-link:hover {
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
  .register-card {
    padding: 32px 24px;
  }

  .register-title {
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