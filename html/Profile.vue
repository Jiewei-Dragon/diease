<template>
  <div class="profile-page">
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

    <main class="main-content">
      <div class="content-wrapper">
        <div class="user-card card" @click="openPasswordModal">
          <div class="user-avatar">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 21C20 19.6044 20 18.9067 19.8278 18.3389C19.44 17.0605 18.4395 16.06 17.1611 15.6722C16.5933 15.5 15.8956 15.5 14.5 15.5H9.5C8.10444 15.5 7.40665 15.5 6.83886 15.6722C5.56045 16.06 4.56004 17.0605 4.17224 18.3389C4 18.9067 4 19.6044 4 21M16.5 7.5C16.5 9.98528 14.4853 12 12 12C9.51472 12 7.5 9.98528 7.5 7.5C7.5 5.01472 9.51472 3 12 3C14.4853 3 16.5 5.01472 16.5 7.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="user-info">
            <h2>{{ userInfo.phone }}</h2>
            <p>注册时间：{{ formatTime(userInfo.create_time) }}</p>
            <p v-if="userInfo.update_time">最后修改：{{ formatTime(userInfo.update_time) }}</p>
            <p class="click-hint">点击修改密码</p>
          </div>
          <div class="edit-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V20C2 20.5304 2.21071 21.0391 2.58579 21.4142C2.96086 21.7893 3.46957 22 4 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V13M18.5 2.50001C18.8978 2.10219 19.4374 1.87869 20 1.87869C20.5626 1.87869 21.1022 2.10219 21.5 2.50001C21.8978 2.89784 22.1213 3.4374 22.1213 4.00001C22.1213 4.56262 21.8978 5.10219 21.5 5.50001L12 15L8 16L9 12L18.5 2.50001Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>
      </div>
    </main>

    <!-- 修改密码弹窗 -->
    <transition name="modal">
      <div v-if="showPasswordModal" class="modal-overlay" @click="closePasswordModal">
        <div class="modal-content card" @click.stop>
          <div class="modal-header">
            <h3>修改密码</h3>
            <button @click="closePasswordModal" class="btn-close">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label>手机号</label>
              <input
                v-model="userInfo.phone"
                type="text"
                disabled
                class="form-input"
              />
            </div>
            <div class="form-group">
              <label>新密码</label>
              <input
                v-model="passwordForm.newPassword"
                type="password"
                placeholder="请输入新密码（至少6位）"
                class="form-input"
                @input="validatePassword"
              />
              <span v-if="passwordError" class="error-message">{{ passwordError }}</span>
            </div>
            <div class="form-group">
              <label>确认新密码</label>
              <input
                v-model="passwordForm.confirmPassword"
                type="password"
                placeholder="请再次输入新密码"
                class="form-input"
                @input="validateConfirmPassword"
              />
              <span v-if="confirmPasswordError" class="error-message">{{ confirmPasswordError }}</span>
            </div>
            <div class="modal-footer">
              <button @click="closePasswordModal" class="btn-dialog btn-secondary">
                取消
              </button>
              <button @click="changePassword" class="btn-dialog btn-primary" :disabled="loading || !isFormValid">
                {{ loading ? '修改中...' : '确认修改' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userInfo: {
        id: null,
        phone: '',
        create_time: '',
        update_time: ''
      },
      passwordForm: {
        newPassword: '',
        confirmPassword: ''
      },
      loading: false,
      showPasswordModal: false,
      passwordError: '',
      confirmPasswordError: ''
    };
  },
  computed: {
    isFormValid() {
      return (
        this.passwordForm.newPassword.length >= 6 &&
        this.passwordForm.newPassword === this.passwordForm.confirmPassword &&
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
      this.$router.push('/index');
    },
    openPasswordModal() {
      console.log('点击了用户卡片');
      this.showPasswordModal = true;
    },
    async loadUserInfo() {
      try {
        const userInfoStr = localStorage.getItem('userInfo');
        const token = localStorage.getItem('token');

        if (userInfoStr) {
          const userInfo = JSON.parse(userInfoStr);
          this.userInfo = { ...this.userInfo, ...userInfo };

          // 如果本地存储没有时间信息，从API获取
          if ((!userInfo.create_time || !userInfo.update_time) && token) {
            await this.fetchUserInfoFromAPI();
          }
        } else if (token) {
          await this.fetchUserInfoFromAPI();
        } else {
          console.warn('未找到用户信息和token');
        }
      } catch (error) {
        console.error('获取用户信息失败:', error);
        // 不弹出提示，避免干扰用户体验
      }
    },

    async fetchUserInfoFromAPI() {
      try {
        const response = await this.$api.getUserInfo();
        if (response.code === 200 && response.data) {
          this.userInfo = { ...this.userInfo, ...response.data };
          localStorage.setItem('userInfo', JSON.stringify(response.data));
        }
      } catch (error) {
        // 静默处理错误，避免触发401跳转
        console.error('从API获取用户信息失败:', error);
      }
    },

    closePasswordModal() {
      this.showPasswordModal = false;
      this.passwordForm = {
        newPassword: '',
        confirmPassword: ''
      };
      this.passwordError = '';
      this.confirmPasswordError = '';
    },
    validatePassword() {
      if (this.passwordForm.newPassword && this.passwordForm.newPassword.length < 6) {
        this.passwordError = '密码至少需要6位';
      } else {
        this.passwordError = '';
      }
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
    async changePassword() {
      if (this.loading || !this.isFormValid) return;

      if (!this.userInfo.id) {
        alert('用户信息不完整，请重新登录');
        return;
      }

      this.loading = true;
      try {
        const response = await this.$api.updatePassword({
          user_id: this.userInfo.id,
          password: this.passwordForm.newPassword
        });

        if (response.code === 200) {
          alert('密码修改成功！请重新登录');
          localStorage.removeItem('token');
          localStorage.removeItem('userInfo');
          setTimeout(() => {
            this.$router.push('/login');
          }, 1000);
        } else {
          throw new Error(response.message || '修改失败');
        }
      } catch (error) {
        const errorMsg = error.response?.data?.detail ||
                        error.response?.data?.message ||
                        error.message ||
                        '修改失败，请重试';
        console.error('修改密码失败:', error);
        alert(errorMsg);
      } finally {
        this.loading = false;
      }
    },
    formatTime(time) {
      if (!time) return '未知';

      // 如果已经是格式化后的字符串，直接返回
      if (typeof time === 'string') {
        return time;
      }

      // 如果是日期对象，进行格式化
      try {
        const date = new Date(time);
        if (isNaN(date.getTime())) {
          return '未知';
        }

        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');

        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
      } catch (error) {
        console.error('时间格式化失败:', error);
        return '未知';
      }
    }
  }
};
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--ultra-light-blue) 0%, var(--white) 100%);
}

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

.main-content {
  padding: 32px;
}

.content-wrapper {
  max-width: 700px;
  margin: 0 auto;
}

.user-card {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 32px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}

.user-card:hover {
  background: var(--ultra-light-blue);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.user-card:active {
  transform: translateY(0);
  opacity: 0.9;
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

.user-info {
  flex: 1;
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
  margin: 0 0 4px 0;
}

.click-hint {
  color: var(--primary-blue) !important;
  font-weight: 500;
  margin-top: 8px !important;
}

.edit-icon {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--ultra-light-blue);
  border-radius: var(--border-radius-sm);
  color: var(--primary-blue);
  transition: var(--transition);
}

.user-card:hover .edit-icon {
  background: var(--primary-blue);
  color: var(--white);
}

.edit-icon svg {
  width: 20px;
  height: 20px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
  pointer-events: auto;
}

.modal-content {
  background: var(--white);
  border-radius: var(--border-radius);
  max-width: 500px;
  width: 100%;
  padding: 0;
  pointer-events: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 2px solid var(--gray-100);
}

.modal-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: var(--gray-900);
  margin: 0;
}

.btn-close {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--gray-100);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}

.btn-close:hover {
  background: var(--gray-200);
}

.btn-close svg {
  width: 18px;
  height: 18px;
  color: var(--gray-600);
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: var(--gray-700);
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 2px solid var(--gray-200);
  border-radius: var(--border-radius-sm);
  font-size: 14px;
  transition: var(--transition);
}

.form-input:focus {
  outline: none;
  border-color: var(--primary-blue);
}

.form-input:disabled {
  background: var(--gray-50);
  cursor: not-allowed;
}

.error-message {
  font-size: 12px;
  color: var(--error);
  margin-top: 4px;
  display: block;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.btn-dialog {
  padding: 10px 24px;
  border-radius: var(--border-radius-sm);
  border: none;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: var(--transition);
}

.btn-dialog:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: var(--gray-200);
  color: var(--gray-700);
}

.btn-secondary:hover {
  background: var(--gray-300);
}

.btn-primary {
  background: var(--primary-blue);
  color: var(--white);
}

.btn-primary:hover {
  background: var(--primary-blue-hover);
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
  transition: transform 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-content {
  transform: scale(0.9);
}

.modal-leave-to .modal-content {
  transform: scale(0.9);
}

@media (max-width: 768px) {
  .header-content {
    padding: 12px 16px;
  }

  .page-title {
    font-size: 20px;
  }

  .btn-back {
    padding: 6px 12px;
    font-size: 13px;
  }

  .btn-back svg {
    width: 16px;
    height: 16px;
  }

  .main-content {
    padding: 12px;
  }

  .content-wrapper {
    max-width: 100%;
  }

  .user-card {
    padding: 20px;
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }

  .user-avatar {
    width: 60px;
    height: 60px;
  }

  .user-avatar svg {
    width: 30px;
    height: 30px;
  }

  .user-info h2 {
    font-size: 20px;
    margin-bottom: 12px;
  }

  .user-info p {
    font-size: 13px;
    margin-bottom: 6px;
  }

  .click-hint {
    margin-top: 12px !important;
  }

  .edit-icon {
    width: 32px;
    height: 32px;
  }

  .edit-icon svg {
    width: 18px;
    height: 18px;
  }

  .modal-content {
    max-width: 95%;
    margin: 10px;
  }

  .modal-header {
    padding: 16px;
  }

  .modal-header h3 {
    font-size: 18px;
  }

  .modal-body {
    padding: 16px;
  }

  .form-group {
    margin-bottom: 16px;
  }

  .form-group label {
    font-size: 13px;
  }

  .form-input {
    padding: 10px;
    font-size: 13px;
  }

  .modal-footer {
    gap: 8px;
    margin-top: 16px;
  }

  .btn-dialog {
    padding: 8px 16px;
    font-size: 13px;
  }
}
</style>