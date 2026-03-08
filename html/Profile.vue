<template>
  <div class="profile-page">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="header-content">
        <div class="header-left">
          <button @click="goBack" class="btn-back">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            返回
          </button>
          <h1 class="page-title">个人中心</h1>
        </div>
      </div>
    </header>

    <!-- 主要内容 -->
    <main class="main-content">
      <div class="content-wrapper">
        <!-- 用户信息卡片 -->
        <div class="user-card card">
          <div class="user-avatar">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 21C20 19.6044 20 18.9067 19.8278 18.3389C19.44 17.0605 18.4395 16.06 17.1611 15.6722C16.5933 15.5 15.8956 15.5 14.5 15.5H9.5C8.10444 15.5 7.40665 15.5 6.83886 15.6722C5.56045 16.06 4.56004 17.0605 4.17224 18.3389C4 18.9067 4 19.6044 4 21M16.5 7.5C16.5 9.98528 14.4853 12 12 12C9.51472 12 7.5 9.98528 7.5 7.5C7.5 5.01472 9.51472 3 12 3C14.4853 3 16.5 5.01472 16.5 7.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="user-info">
            <h2>{{ userInfo.phone }}</h2>
            <p>注册时间：{{ formatTime(userInfo.createdAt) }}</p>
          </div>
        </div>

        <!-- 修改密码区域 -->
        <div class="change-password-section card">
          <h3 class="section-title">修改密码</h3>
          
          <form @submit.prevent="changePassword" class="password-form">
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
                  v-model="passwordForm.phone" 
                  placeholder="请输入手机号" 
                  required 
                  pattern="^1[3-9]\d{9}$"
                  :disabled="loading"
                  @input="validatePhone"
                />
              </div>
              <span v-if="phoneError" class="error-message">{{ phoneError }}</span>
            </div>

            <div class="form-group">
              <label for="code">验证码</label>
              <div class="input-wrapper code-wrapper">
                <svg class="input-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 12H15M9 16H15M17 21H7C5.89543 21 5 20.1046 5 19V5C5 3.89543 5.89543 3 7 3H12.5858C12.851 3 13.1054 3.10536 13.2929 3.29289L18.7071 8.70711C18.8946 8.89464 19 9.149 19 9.41421V19C19 20.1046 18.1046 21 17 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <input 
                  id="code"
                  type="text" 
                  v-model="passwordForm.code" 
                  placeholder="请输入验证码" 
                  required 
                  maxlength="6"
                  pattern="\d{6}"
                  :disabled="loading"
                />
                <button 
                  type="button" 
                  class="btn-code"
                  @click="sendCode"
                  :disabled="!canSendCode || countdown > 0 || loading"
                >
                  {{ countdown > 0 ? `${countdown}秒后重试` : '获取验证码' }}
                </button>
              </div>
              <span v-if="codeError" class="error-message">{{ codeError }}</span>
            </div>

            <div class="form-group">
              <label for="newPassword">新密码</label>
              <div class="input-wrapper">
                <svg class="input-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 14.5V16.5M7 10.0288C7.47142 10 8.05259 10 8.8 10H15.2C15.9474 10 16.5286 10 17 10.0288M7 10.0288C6.41168 10.0647 5.99429 10.1455 5.63803 10.327C5.07354 10.6146 4.6146 11.0735 4.32698 11.638C4 12.2798 4 13.1198 4 14.8V16.2C4 17.8802 4 18.7202 4.32698 19.362C4.6146 19.9265 5.07354 20.3854 5.63803 20.673C6.27976 21 7.11984 21 8.8 21H15.2C16.8802 21 17.7202 21 18.362 20.673C18.9265 20.3854 19.3854 19.9265 19.673 19.362C20 18.7202 20 17.8802 20 16.2V14.8C20 13.1198 20 12.2798 19.673 11.638C19.3854 11.0735 18.9265 10.6146 18.362 10.327C18.0057 10.1455 17.5883 10.0647 17 10.0288M7 10.0288V8C7 5.23858 9.23858 3 12 3C14.7614 3 17 5.23858 17 8V10.0288" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <input 
                  id="newPassword"
                  type="password" 
                  v-model="passwordForm.newPassword" 
                  placeholder="请输入新密码（至少6位）" 
                  required 
                  minlength="6"
                  :disabled="loading"
                  @input="validatePassword"
                />
              </div>
              <span v-if="passwordError" class="error-message">{{ passwordError }}</span>
            </div>

            <div class="form-group">
              <label for="confirmPassword">确认新密码</label>
              <div class="input-wrapper">
                <svg class="input-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 14.5V16.5M7 10.0288C7.47142 10 8.05259 10 8.8 10H15.2C15.9474 10 16.5286 10 17 10.0288M7 10.0288C6.41168 10.0647 5.99429 10.1455 5.63803 10.327C5.07354 10.6146 4.6146 11.0735 4.32698 11.638C4 12.2798 4 13.1198 4 14.8V16.2C4 17.8802 4 18.7202 4.32698 19.362C4.6146 19.9265 5.07354 20.3854 5.63803 20.673C6.27976 21 7.11984 21 8.8 21H15.2C16.8802 21 17.7202 21 18.362 20.673C18.9265 20.3854 19.3854 19.9265 19.673 19.362C20 18.7202 20 17.8802 20 16.2V14.8C20 13.1198 20 12.2798 19.673 11.638C19.3854 11.0735 18.9265 10.6146 18.362 10.327C18.0057 10.1455 17.5883 10.0647 17 10.0288M7 10.0288V8C7 5.23858 9.23858 3 12 3C14.7614 3 17 5.23858 17 8V10.0288" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <input 
                  id="confirmPassword"
                  type="password" 
                  v-model="passwordForm.confirmPassword" 
                  placeholder="请再次输入新密码" 
                  required 
                  minlength="6"
                  :disabled="loading"
                  @input="validateConfirmPassword"
                />
              </div>
              <span v-if="confirmPasswordError" class="error-message">{{ confirmPasswordError }}</span>
            </div>

            <button type="submit" class="btn-submit btn-primary" :disabled="loading || !isFormValid">
              <span v-if="!loading">确认修改</span>
              <span v-else class="loading-text">
                <span class="loading"></span>
                修改中...
              </span>
            </button>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userInfo: {
        phone: '',
        createdAt: ''
      },
      passwordForm: {
        phone: '',
        code: '',
        newPassword: '',
        confirmPassword: ''
      },
      loading: false,
      countdown: 0,
      phoneError: '',
      codeError: '',
      passwordError: '',
      confirmPasswordError: ''
    };
  },
  computed: {
    canSendCode() {
      const phoneRegex = /^1[3-9]\d{9}$/;
      return phoneRegex.test(this.passwordForm.phone);
    },
    isFormValid() {
      return (
        this.canSendCode &&
        this.passwordForm.code.length === 6 &&
        this.passwordForm.newPassword.length >= 6 &&
        this.passwordForm.newPassword === this.passwordForm.confirmPassword &&
        !this.phoneError &&
        !this.codeError &&
        !this.passwordError &&
        !this.confirmPasswordError
      );
    }
  },
  mounted() {
    this.loadUserInfo();
  },
  methods: {
    goBack() {
      this.$router.push('/main');
    },
    async loadUserInfo() {
      try {
        const userInfoStr = localStorage.getItem('userInfo');
        if (userInfoStr) {
          const userInfo = JSON.parse(userInfoStr);
          this.userInfo = userInfo;
          this.passwordForm.phone = userInfo.phone || '';
        } else {
          // 尝试从服务器获取
          const response = await this.$api.getUserInfo();
          if (response.code === 200 && response.data) {
            this.userInfo = response.data;
            this.passwordForm.phone = response.data.phone || '';
            localStorage.setItem('userInfo', JSON.stringify(response.data));
          }
        }
      } catch (error) {
        console.error('获取用户信息失败:', error);
      }
    },
    validatePhone() {
      const phoneRegex = /^1[3-9]\d{9}$/;
      if (this.passwordForm.phone && !phoneRegex.test(this.passwordForm.phone)) {
        this.phoneError = '请输入正确的手机号';
      } else {
        this.phoneError = '';
      }
    },
    validatePassword() {
      if (this.passwordForm.newPassword && this.passwordForm.newPassword.length < 6) {
        this.passwordError = '密码至少需要6位';
      } else {
        this.passwordError = '';
      }
      // 同时验证确认密码
      if (this.passwordForm.confirmPassword) {
        this.validateConfirmPassword();
      }
    },
    validateConfirmPassword() {
      if (this.passwordForm.confirmPassword && this.passwordForm.confirmPassword !== this.passwordForm.newPassword) {
        this.confirmPasswordError = '两次输入的密码不一致';
      } else {
        this.confirmPasswordError = '';
      }
    },
    async sendCode() {
      if (!this.canSendCode || this.countdown > 0 || this.loading) return;

      this.loading = true;
      this.codeError = '';

      try {
        await this.$api.sendPasswordCode({ 
          phone: this.passwordForm.phone 
        });
        
        // 开始倒计时
        this.countdown = 60;
        const timer = setInterval(() => {
          this.countdown--;
          if (this.countdown <= 0) {
            clearInterval(timer);
          }
        }, 1000);
        
        alert('验证码已发送，请查收短信');
      } catch (error) {
        this.codeError = error.response?.data?.message || '验证码发送失败，请稍后重试';
        alert(this.codeError);
      } finally {
        this.loading = false;
      }
    },
    async changePassword() {
      if (this.loading || !this.isFormValid) return;

      this.loading = true;
      try {
        await this.$api.changePassword({ 
          phone: this.passwordForm.phone, 
          code: this.passwordForm.code,
          newPassword: this.passwordForm.newPassword 
        });
        
        alert('密码修改成功！请重新登录');
        
        // 清除登录信息
        localStorage.removeItem('token');
        localStorage.removeItem('userInfo');
        
        // 跳转到登录页
        setTimeout(() => {
          this.$router.push('/login');
        }, 1000);
      } catch (error) {
        const errorMsg = error.response?.data?.message || '修改失败，请检查您的信息';
        alert(errorMsg);
      } finally {
        this.loading = false;
      }
    },
    formatTime(time) {
      if (!time) return '未知';
      const date = new Date(time);
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      });
    }
  }
};
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--ultra-light-blue) 0%, var(--white) 100%);
}

/* 顶部导航栏 */
.header {
  background: var(--white);
  box-shadow: var(--shadow-md);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 16px 32px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--white);
  color: var(--primary-blue);
  border: 2px solid var(--primary-blue);
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  transition: var(--transition);
  font-weight: 500;
}

.btn-back:hover {
  background: var(--ultra-light-blue);
}

.btn-back svg {
  width: 20px;
  height: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--gray-900);
  margin: 0;
}

/* 主要内容 */
.main-content {
  padding: 32px;
}

.content-wrapper {
  max-width: 700px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 用户信息卡片 */
.user-card {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 32px;
}

.user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.user-avatar svg {
  width: 40px;
  height: 40px;
  color: var(--white);
}

.user-info h2 {
  font-size: 24px;
  font-weight: 700;
  color: var(--gray-900);
  margin: 0 0 8px 0;
}

.user-info p {
  font-size: 14px;
  color: var(--gray-500);
  margin: 0;
}

/* 修改密码区域 */
.change-password-section {
  padding: 32px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--gray-900);
  margin: 0 0 24px 0;
  padding-bottom: 16px;
  border-bottom: 2px solid var(--gray-100);
}

.password-form {
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

.code-wrapper input {
  padding-right: 130px;
}

.btn-code {
  position: absolute;
  right: 8px;
  padding: 8px 16px;
  background: var(--white);
  color: var(--primary-blue);
  border: 1px solid var(--primary-blue);
  border-radius: var(--border-radius-sm);
  font-size: 13px;
  font-weight: 500;
  white-space: nowrap;
  transition: var(--transition);
}

.btn-code:hover:not(:disabled) {
  background: var(--ultra-light-blue);
}

.btn-code:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: var(--gray-50);
  border-color: var(--gray-300);
  color: var(--gray-500);
}

.error-message {
  font-size: 12px;
  color: var(--error);
  margin-top: -4px;
}

.btn-submit {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  margin-top: 8px;
}

.btn-submit:disabled {
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

/* 响应式设计 */
@media (max-width: 768px) {
  .main-content {
    padding: 16px;
  }

  .user-card {
    padding: 24px;
  }

  .change-password-section {
    padding: 24px;
  }

  .code-wrapper input {
    padding-right: 120px;
  }

  .btn-code {
    font-size: 12px;
    padding: 6px 12px;
  }
}
</style>