<template>
  <div class="users-page">
    <header class="header">
      <div class="header-content">
        <div class="header-left">
          <button @click="goBack" class="btn-back">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            返回
          </button>
          <h1 class="page-title">用户管理</h1>
        </div>
      </div>
    </header>

    <main class="main-content">
      <div class="content-wrapper">
        <div class="users-section card">
          <div class="section-header">
            <h2 class="section-title">用户列表</h2>
            <div class="section-actions">
              <div class="search-box">
                <input 
                  v-model="searchKeyword" 
                  @keyup.enter="handleSearch"
                  type="text" 
                  placeholder="搜索手机号..."
                  class="search-input"
                />
                <button @click="handleSearch" class="btn-search">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 21L16.65 16.65M19 11C19 15.4183 15.4183 19 11 19C6.58172 19 3 15.4183 3 11C3 6.58172 6.58172 3 11 3C15.4183 3 19 6.58172 19 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
              <button @click="refreshUsers" class="btn-icon" title="刷新">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M4 4V9H4.58152M19.9381 11C19.446 7.05369 16.0796 4 12 4C8.64262 4 5.76829 6.06817 4.58152 9M4.58152 9H9M20 20V15H19.4185M19.4185 15C18.2317 17.9318 15.3574 20 12 20C7.92038 20 4.55399 16.9463 4.06189 13M19.4185 15H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </div>
          </div>

          <div v-if="loading" class="loading-state">
            <div class="loading-spinner"></div>
            <p>加载中...</p>
          </div>

          <div v-else-if="users.length === 0" class="empty-state">
            <svg class="empty-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21M23 21V19C22.9993 18.1137 22.7044 17.2528 22.1614 16.5523C21.6184 15.8519 20.8581 15.3516 20 15.13M16 3.13C16.8604 3.35031 17.623 3.85071 18.1676 4.55232C18.7122 5.25392 19.0078 6.11683 19.0078 7.005C19.0078 7.89318 18.7122 8.75608 18.1676 9.45769C17.623 10.1593 16.8604 10.6597 16 10.88C15.1396 11.1003 14.377 10.6007 13.8324 9.89909C13.2878 9.1975 12.9922 8.3346 12.9922 7.445C12.9922 6.5554 13.2878 5.6925 13.8324 4.99091C14.377 4.28932 15.1396 3.78972 16 3.57M13 7C13 9.20914 11.2091 11 9 11C6.79086 11 5 9.20914 5 7C5 4.79086 6.79086 3 9 3C11.2091 3 13 4.79086 13 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <p class="empty-text">暂无用户数据</p>
          </div>

          <div v-else class="table-container">
            <table class="users-table">
              <thead>
                <tr>
                  <th>序号</th>
                  <th>手机号</th>
                  <th>角色</th>
                  <th>状态</th>
                  <th>注册时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(user, index) in users" :key="user.id" class="table-row">
                  <td>{{ (currentPage - 1) * pageSize + index + 1 }}</td>
                  <td>{{ user.phone }}</td>
                  <td>
                    <span
                      :class="['role-badge', user.is_admin ? 'role-admin' : 'role-user']"
                      @click="toggleRole(user)"
                      style="cursor: pointer;"
                      :title="user.is_admin ? '点击设为普通用户' : '点击设为管理员'"
                    >
                      {{ user.is_admin ? '管理员' : '普通用户' }}
                    </span>
                  </td>
                  <td>
                    <span :class="['status-badge', user.is_banned ? 'status-banned' : 'status-normal']">
                      {{ user.is_banned ? '已封禁' : '正常' }}
                    </span>
                  </td>
                  <td>{{ user.create_time }}</td>
                  <td>
                    <div class="action-buttons">
                      <button @click="editUser(user)" class="btn-action btn-edit" title="编辑">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V20C2 20.5304 2.21071 21.0391 2.58579 21.4142C2.96086 21.7893 3.46957 22 4 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V13M18.5 2.50001C18.8978 2.10219 19.4374 1.87869 20 1.87869C20.5626 1.87869 21.1022 2.10219 21.5 2.50001C21.8978 2.89784 22.1213 3.4374 22.1213 4.00001C22.1213 4.56262 21.8978 5.10219 21.5 5.50001L12 15L8 16L9 12L18.5 2.50001Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                      </button>
                      <button 
                        @click.stop="toggleBan(user)"
                        :class="['btn-action', user.is_banned ? 'btn-unban' : 'btn-ban']"
                        :title="user.is_banned ? '解封' : '封禁'"
                      >
                        <svg v-if="user.is_banned" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <svg v-else viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M12 15C10.3431 15 9 13.6569 9 12C9 10.3431 10.3431 9 12 9C13.6569 9 15 10.3431 15 12C15 13.6569 13.6569 15 12 15Z M12 2C7.58172 2 4 5.58172 4 10V12C4 16.4183 7.58172 20 12 20C16.4183 20 20 16.4183 20 12V10C20 5.58172 16.4183 2 12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-if="users.length > 0" class="pagination">
            <button 
              @click="changePage(currentPage - 1)" 
              :disabled="currentPage === 1"
              class="btn-page"
            >
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
            
            <div class="page-numbers">
              <button 
                v-for="page in visiblePages" 
                :key="page"
                @click="changePage(page)"
                :class="['btn-page', { 'active': page === currentPage }]"
              >
                {{ page }}
              </button>
            </div>

            <button 
              @click="changePage(currentPage + 1)" 
              :disabled="currentPage === totalPages"
              class="btn-page"
            >
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- 编辑用户弹窗 -->
    <transition name="modal">
      <div v-if="showEditModal" class="modal-overlay" @click="closeEditModal">
        <div class="modal-content card" @click.stop>
          <div class="modal-header">
            <h3>编辑用户</h3>
            <button @click="closeEditModal" class="btn-close">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
                    <div class="modal-body">
            <div class="form-group">
              <label>手机号：</label>
              <input
                v-model="editForm.phone"
                type="text"
                placeholder="请输入手机号"
                class="form-input"
              />
            </div>
            <div class="form-group">
              <label>新密码（留空不修改）：</label>
              <input
                v-model="editForm.password"
                type="password"
                placeholder="请输入新密码"
                class="form-input"
              />
            </div>
            <div class="modal-footer">
              <button @click="closeEditModal" class="btn-dialog btn-secondary">
                取消
              </button>
              <button @click="saveUser" class="btn-dialog btn-primary" :disabled="isSaving">
                {{ isSaving ? '保存中...' : '保存' }}
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
      users: [],
      currentPage: 1,
      pageSize: 10,
      totalUsers: 0,
      loading: false,
      searchKeyword: '',
      showEditModal: false,
      isSaving: false,
      editForm: {
        id: null,
        phone: '',
        password: ''
      }
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalUsers / this.pageSize);
    },
    visiblePages() {
      const pages = [];
      const maxVisible = 5;
      let start = Math.max(1, this.currentPage - Math.floor(maxVisible / 2));
      let end = Math.min(this.totalPages, start + maxVisible - 1);
      
      if (end - start < maxVisible - 1) {
        start = Math.max(1, end - maxVisible + 1);
      }
      
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    }
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    goBack() {
      this.$router.push('/index');
    },
    async fetchUsers(page = 1) {
      this.loading = true;
      this.currentPage = page;
      
      try {
        const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}');
        if (!userInfo.id) {
          throw new Error('未找到用户ID');
        }
        
        const params = {
          current_user_id: userInfo.id,
          page: page,
          page_size: this.pageSize
        };
        
        if (this.searchKeyword) {
          params.keyword = this.searchKeyword;
        }
        
        const response = await this.$api.getUserList(params);
        
        if (response.code === 200 && response.data) {
          this.users = response.data.list || [];
          this.totalUsers = response.data.total || 0;
        } else {
          throw new Error(response.message || '获取用户列表失败');
        }
      } catch (error) {
        const errorMsg = error.response?.data?.detail || 
                        error.response?.data?.message || 
                        error.message || 
                        '获取用户列表失败';
        console.error('获取用户列表失败:', error);
        alert(errorMsg);
      } finally {
        this.loading = false;
      }
    },
    handleSearch() {
      this.fetchUsers(1);
    },
    async refreshUsers() {
      this.searchKeyword = '';
      await this.fetchUsers(this.currentPage);
    },
    changePage(page) {
      if (page < 1 || page > this.totalPages) return;
      this.fetchUsers(page);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    editUser(user) {
      this.editForm = {
        id: user.id,
        phone: user.phone,
        password: ''
      };
      this.showEditModal = true;
    },
    closeEditModal() {
      this.showEditModal = false;
      this.editForm = { id: null, phone: '', password: '' };
    },
    async saveUser() {
      if (!this.editForm.phone) {
        alert('请输入手机号');
        return;
      }
      
      const phoneRegex = /^1[3-9]\d{9}$/;
      if (!phoneRegex.test(this.editForm.phone)) {
        alert('请输入正确的手机号');
        return;
      }
      
      if (this.editForm.password && this.editForm.password.length < 6) {
        alert('密码长度不能少于6位');
        return;
      }
      
      this.isSaving = true;
      
      try {
        const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}');
        
        const data = {
          phone: this.editForm.phone
        };
        
        if (this.editForm.password) {
          data.password = this.editForm.password;
        }
        
        const response = await this.$api.updateUser(this.editForm.id, userInfo.id, data);
        
        if (response.code === 200) {
          alert('保存成功');
          this.closeEditModal();
          this.fetchUsers(this.currentPage);
        } else {
          throw new Error(response.message || '保存失败');
        }
      } catch (error) {
        const errorMsg = error.response?.data?.detail || 
                        error.response?.data?.message || 
                        error.message || 
                        '保存失败';
        console.error('保存失败:', error);
        alert(errorMsg);
      } finally {
        this.isSaving = false;
      }
    },
    async toggleBan(user) {
      const action = user.is_banned ? '解封' : '封禁';
      if (!confirm(`确定要${action}该用户吗？`)) {
        return;
      }
      
      try {
        const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}');
        const newStatus = user.is_banned ? 0 : 1;
        
        const response = await this.$api.banUser(user.id, userInfo.id, newStatus);
        
        if (response.code === 200) {
          alert(`${action}成功`);
          this.fetchUsers(this.currentPage);
        } else {
          throw new Error(response.message || `${action}失败`);
        }
      } catch (error) {
        const errorMsg = error.response?.data?.detail || 
                        error.response?.data?.message || 
                        error.message || 
                        `${action}失败`;
        console.error(`${action}失败:`, error);
        alert(errorMsg);
      }
    },
    async toggleRole(user) {
      const currentUser = JSON.parse(localStorage.getItem('userInfo') || '{}');

      // 防止修改自己的角色
      if (user.id === currentUser.id) {
        alert('不能修改自己的角色');
        return;
      }

      const action = user.is_admin ? '降级为普通用户' : '提升为管理员';
      if (!confirm(`确定要${action}吗？`)) {
        return;
      }

      try {
        const response = await this.$api.toggleUserRole(user.id, currentUser.id);

        if (response.code === 200) {
          alert(response.message || '角色切换成功');
          this.fetchUsers(this.currentPage);
        } else {
          throw new Error(response.message || '角色切换失败');
        }
      } catch (error) {
        const errorMsg = error.response?.data?.detail ||
                        error.response?.data?.message ||
                        error.message ||
                        '角色切换失败';
        console.error('角色切换失败:', error);
        alert(errorMsg);
      }
    }
  }
};
</script>

<style scoped>
.users-page {
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
  max-width: 1400px;
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
  max-width: 1400px;
  margin: 0 auto;
}

.users-section {
  padding: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid var(--gray-100);
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--gray-900);
  margin: 0;
}

.section-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-input {
  padding: 8px 16px;
  border: 2px solid var(--gray-200);
  border-radius: var(--border-radius-sm);
  font-size: 14px;
  width: 250px;
  transition: var(--transition);
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-blue);
}

.btn-search {
  padding: 8px 16px;
  background: var(--primary-blue);
  color: var(--white);
  border: none;
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: var(--transition);
}

.btn-search:hover {
  background: var(--primary-blue-hover);
}

.btn-search svg {
  width: 18px;
  height: 18px;
}

.btn-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--border-radius-sm);
  background: var(--white);
  border: 2px solid var(--gray-200);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
  color: var(--gray-700);
}

.btn-icon:hover {
  border-color: var(--primary-blue);
  color: var(--primary-blue);
}

.btn-icon svg {
  width: 18px;
  height: 18px;
}

.loading-state {
  text-align: center;
  padding: 64px 32px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 16px;
  border: 4px solid var(--light-blue);
  border-top-color: var(--primary-blue);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 64px 32px;
}

.empty-icon {
  width: 80px;
  height: 80px;
  color: var(--gray-300);
  margin-bottom: 16px;
}

.empty-text {
  font-size: 16px;
  font-weight: 600;
  color: var(--gray-600);
  margin: 0;
}

.table-container {
  overflow-x: auto;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table thead tr {
  background: var(--gray-50);
}

.users-table th {
  padding: 16px;
  text-align: center;
  font-size: 14px;
  font-weight: 600;
  color: var(--gray-700);
  border-bottom: 2px solid var(--gray-200);
}

.users-table td {
  padding: 12px 16px;
  font-size: 14px;
  color: var(--gray-800);
  border-bottom: 1px solid var(--gray-100);
  vertical-align: middle;
  text-align: center;
}

.table-row {
  transition: var(--transition);
}

.table-row:hover {
  background: var(--ultra-light-blue);
}

.role-badge,
.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: var(--border-radius-sm);
  font-weight: 500;
  font-size: 13px;
}

.role-admin {
  background: #fef3c7;
  color: #92400e;
  transition: var(--transition);
}

.role-admin:hover {
  background: #fde68a;
  transform: scale(1.05);
}

.role-user {
  background: var(--ultra-light-blue);
  color: var(--primary-blue);
  transition: var(--transition);
}

.role-user:hover {
  background: var(--light-blue);
  transform: scale(1.05);
}

.status-normal {
  background: #dcfce7;
  color: #166534;
}

.status-banned {
  background: #fee2e2;
  color: #991b1b;
}

.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.btn-action {
  width: 32px;
  height: 32px;
  border-radius: var(--border-radius-sm);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}

.btn-action svg {
  width: 16px;
  height: 16px;
}

.btn-edit {
  background: var(--ultra-light-blue);
  color: var(--primary-blue);
}

.btn-edit:hover {
  background: var(--light-blue);
}

.btn-ban {
  background: #fee2e2;
  color: var(--error);
}

.btn-ban:hover {
  background: #fecaca;
}

.btn-unban {
  background: #dcfce7;
  color: var(--success);
}

.btn-unban:hover {
  background: #bbf7d0;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--gray-100);
}

.btn-page {
  width: 36px;
  height: 36px;
  border-radius: var(--border-radius-sm);
  background: var(--white);
  border: 2px solid var(--gray-200);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
  font-weight: 500;
  color: var(--gray-700);
}

.btn-page:hover:not(:disabled) {
  border-color: var(--primary-blue);
  color: var(--primary-blue);
}

.btn-page.active {
  background: var(--primary-blue);
  border-color: var(--primary-blue);
  color: var(--white);
}

.btn-page:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-page svg {
  width: 18px;
  height: 18px;
}

.page-numbers {
  display: flex;
  gap: 4px;
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
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: var(--white);
  border-radius: var(--border-radius);
  max-width: 500px;
  width: 100%;
  padding: 0;
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

  .users-section {
    padding: 16px;
  }

  .section-header {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
    margin-bottom: 16px;
    padding-bottom: 12px;
  }

  .section-title {
    font-size: 18px;
  }

  .section-actions {
    flex-direction: row;
    flex-wrap: wrap;
    width: 100%;
    gap: 8px;
  }

  .search-box {
    flex: 1;
    min-width: 200px;
    display: flex;
    align-items: center;
  }

  .search-input {
    flex: 1;
    min-width: 0;
    padding: 10px 12px;
    font-size: 14px;
  }

  .btn-search {
    padding: 10px 14px;
    white-space: nowrap;
  }

  .btn-icon {
    width: 40px;
    height: 40px;
    flex-shrink: 0;
  }

  .table-container {
    overflow-x: scroll;
    -webkit-overflow-scrolling: touch;
  }

  .users-table {
    min-width: 700px;
    font-size: 13px;
  }

  .users-table th {
    padding: 12px 8px;
    font-size: 13px;
    white-space: nowrap;
  }

  .users-table td {
    padding: 10px 8px;
    font-size: 13px;
  }

  .role-badge,
  .status-badge {
    padding: 4px 8px;
    font-size: 12px;
  }

  .action-buttons {
    gap: 6px;
  }

  .btn-action {
    width: 28px;
    height: 28px;
  }

  .btn-action svg {
    width: 14px;
    height: 14px;
  }

  .pagination {
    gap: 6px;
    margin-top: 16px;
    padding-top: 16px;
  }

  .btn-page {
    width: 32px;
    height: 32px;
  }

  .page-numbers {
    display: none;
  }

  .modal-content {
    max-width: 95%;
    margin: 10px;
  }

  .modal-header {
    padding: 16px;
  }

  .modal-body {
    padding: 16px;
  }

  .form-group {
    margin-bottom: 16px;
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