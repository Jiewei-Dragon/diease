<template>
  <div class="records-page">
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
          <h1 class="page-title">识别记录</h1>
        </div>
      </div>
    </header>

    <!-- 主要内容 -->
    <main class="main-content">
      <div class="content-wrapper">
        <!-- 统计卡片 -->
        <div class="stats-grid">
          <div class="stat-card card">
            <div class="stat-icon" style="background: var(--ultra-light-blue);">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15M9 5C9 6.10457 9.89543 7 11 7H13C14.1046 7 15 6.10457 15 5M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="stat-content">
              <p class="stat-label">总识别次数</p>
              <p class="stat-value">{{ totalRecords }}</p>
            </div>
          </div>

          <div class="stat-card card">
            <div class="stat-icon" style="background: #dcfce7;">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="var(--success)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="stat-content">
              <p class="stat-label">今日识别</p>
              <p class="stat-value">{{ todayRecords }}</p>
            </div>
          </div>

          <div class="stat-card card">
            <div class="stat-icon" style="background: #fef3c7;">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 8V12L15 15M21 12C21 16.9706 16.0796 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="var(--warning)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="stat-content">
              <p class="stat-label">最近识别</p>
              <p class="stat-value">{{ recentTime }}</p>
            </div>
          </div>
        </div>

        <!-- 记录列表 -->
        <div class="records-section card">
          <div class="section-header">
            <h2 class="section-title">历史记录</h2>
            <div class="section-actions">
              <div class="search-box">
                <input
                  v-model="searchKeyword"
                  @keyup.enter="handleSearch"
                  type="text"
                  placeholder="搜索疾病名称或序号..."
                  class="search-input"
                />
                <button @click="handleSearch" class="btn-search" :disabled="loading">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M21 12C21 16.9706 16.0796 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
              <select v-model="sortBy" @change="handleSort" class="sort-select">
                <option value="time_desc">时间倒序（最新）</option>
                <option value="time_asc">时间正序（最早）</option>
                <option value="result">识别结果（A-Z）</option>
              </select>
              <button @click="refreshRecords" class="btn-icon" title="刷新">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M4 4V9H4.58152M19.9381 11C19.446 7.05369 16.0796 4 12 4C8.64262 4 5.76829 6.06817 4.58152 9M4.58152 9H9M20 20V15H19.4185M19.4185 15C18.2317 17.9318 15.3574 20 12 20C7.92038 20 4.55399 16.9463 4.06189 13M19.4185 15H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- 加载状态 -->
          <div v-if="loading" class="loading-state">
            <div class="loading-spinner"></div>
            <p>加载中...</p>
          </div>

          <!-- 空状态 -->
          <div v-else-if="records.length === 0" class="empty-state">
            <svg class="empty-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 7H4C2.89543 7 2 7.89543 2 9V19C2 20.1046 2.89543 21 4 21H20C21.1046 21 22 20.1046 22 19V9C22 7.89543 21.1046 7 20 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M16 21V5C16 4.46957 15.7893 3.96086 15.4142 3.58579C15.0391 3.21071 14.5304 3 14 3H10C9.46957 3 8.96086 3.21071 8.58579 3.58579C8.21071 3.96086 8 4.46957 8 5V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <p class="empty-text">暂无识别记录</p>
            <p class="empty-hint">开始上传图片进行识别吧</p>
          </div>

          <!-- 记录表格 -->
          <div v-else class="table-container">
            <table class="records-table">
              <thead>
                <tr>
                  <th>序号</th>
                  <th>原图</th>
                  <th>识别时间</th>
                  <th>识别结果</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(record, index) in records" :key="record.id" class="table-row">
                  <td>{{ (currentPage - 1) * pageSize + index + 1 }}</td>
                  <td>
                    <div class="thumbnail-cell">
                      <img
                        v-if="record.origin_map_url"
                        :src="getImageUrl(record.origin_map_url)"
                        :alt="'记录' + ((currentPage - 1) * pageSize + index + 1)"
                        class="thumbnail"
                        @click="viewDetail(record)"
                      />
                      <div v-else class="no-thumbnail">无图</div>
                    </div>
                  </td>
                  <td>
                    <div class="time-cell">
                      <svg class="time-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 8V12L15 15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                      {{ record.create_time }}
                    </div>
                  </td>
                  <td>
                    <span class="result-badge">{{ record.disease_name }}</span>
                  </td>
                  <td>
                    <div class="action-buttons">
                      <button @click="deleteRecord(index, record.id)" class="btn-action btn-delete" title="删除">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M19 7L18.1327 19.1425C18.0579 20.1891 17.187 21 16.1378 21H7.86224C6.81296 21 5.94208 20.1891 5.86732 19.1425L5 7M10 11V17M14 11V17M15 7V4C15 3.44772 14.5523 3 14 3H10C9.44772 3 9 3.44772 9 4V7M4 7H20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 分页 -->
          <div v-if="records.length > 0" class="pagination">
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

    <!-- 详情弹窗 -->
    <transition name="modal">
      <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal-content card" @click.stop>
          <div class="modal-header">
            <h3>识别详情</h3>
            <button @click="closeModal" class="btn-close">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <div class="detail-item">
              <label>识别时间：</label>
              <span>{{ selectedRecord?.create_time }}</span>
            </div>
            <div class="detail-item">
              <label>识别结果：</label>
              <span class="result-badge">{{ selectedRecord?.disease_name }}</span>
            </div>
            <div class="detail-item">
              <label>置信度：</label>
              <span>{{ selectedRecord?.confidence ? (selectedRecord.confidence * 100).toFixed(2) + '%' : '--' }}</span>
            </div>
            <div v-if="selectedRecord?.origin_map_url" class="detail-image">
              <label>原图：</label>
              <img :src="getImageUrl(selectedRecord.origin_map_url)" alt="原图" />
            </div>
            <div v-if="selectedRecord?.heatmap_url" class="detail-image">
              <label>热力图：</label>
              <img :src="getImageUrl(selectedRecord.heatmap_url)" alt="热力图" />
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
      records: [],
      totalRecords: 0,
      todayRecords: 0,
      recentTime: '--',
      currentPage: 1,
      pageSize: 10,
      loading: false,
      showModal: false,
      selectedRecord: null,
      searchKeyword: '',
      sortBy: 'time_desc'
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalRecords / this.pageSize);
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
    this.fetchRecords();
    this.fetchStatistics();
  },
  methods: {
    goBack() {
      this.$router.push('/index');
    },
    async fetchStatistics() {
      try {
        const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}');
        if (!userInfo.id) {
          console.error('未找到用户ID');
          return;
        }

        const response = await this.$api.getStatistics({
          user_id: userInfo.id
        });
        if (response.code === 200 && response.data) {
          this.totalRecords = response.data.total_count || 0;
          this.todayRecords = response.data.today_count || 0;
          
          if (response.data.latest_time) {
            this.recentTime = this.formatTime(response.data.latest_time);
          }
        }
      } catch (error) {
        console.error('获取统计数据失败:', error);
      }
    },
    async fetchRecords(page = 1) {
      this.loading = true;
      this.currentPage = page;
      
      try {
        const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}');
        if (!userInfo.id) {
          throw new Error('未找到用户ID，请重新登录');
        }

        const params = {
          user_id: userInfo.id,
          page: page,
          page_size: this.pageSize
        };

        // 添加搜索关键词
        if (this.searchKeyword && this.searchKeyword.trim()) {
          params.keyword = this.searchKeyword.trim();
        }

        // 添加排序方式
        if (this.sortBy) {
          params.sort_by = this.sortBy;
        }

        const response = await this.$api.getRecordList(params);
        
        if (response.code === 200 && response.data) {
          this.records = response.data.list || [];
          this.totalRecords = response.data.total || 0;
          
          if (this.records.length > 0) {
            this.recentTime = this.formatTime(this.records[0].create_time);
          }
        } else {
          throw new Error(response.message || '获取记录失败');
        }
      } catch (error) {
        const errorMsg = error.response?.data?.detail ||
                        error.response?.data?.message ||
                        error.message ||
                        '获取记录失败';
        console.error('获取记录失败:', error);
        alert(errorMsg);
      } finally {
        this.loading = false;
      }
    },
    handleSearch() {
      this.fetchRecords(1);
    },
    handleSort() {
      this.fetchRecords(1);
    },
    async deleteRecord(index, recordId) {
      if (!confirm('确定要删除这条记录吗？')) {
        return;
      }
      
      try {
        const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}');
        if (!userInfo.id) {
          throw new Error('未找到用户ID，请重新登录');
        }

        const response = await this.$api.deleteRecord(recordId, userInfo.id);
        
        if (response.code === 200) {
          this.records.splice(index, 1);
          this.totalRecords--;
          alert('删除成功');
          
          if (this.records.length === 0 && this.currentPage > 1) {
            this.changePage(this.currentPage - 1);
          } else {
            this.fetchStatistics();
          }
        }
      } catch (error) {
        const errorMsg = error.response?.data?.detail ||
                        error.response?.data?.message ||
                        '删除失败，请重试';
        console.error('删除失败:', error);
        alert(errorMsg);
      }
    },
    async viewDetail(record) {
      try {
        const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}');
        if (!userInfo.id) {
          throw new Error('未找到用户ID，请重新登录');
        }

        const response = await this.$api.getRecordDetail(record.id, userInfo.id);
        
        if (response.code === 200 && response.data) {
          this.selectedRecord = response.data;
        } else {
          this.selectedRecord = record;
        }
      } catch (error) {
        console.error('获取详情失败:', error);
        this.selectedRecord = record;
      }
      
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedRecord = null;
    },
    changePage(page) {
      if (page < 1 || page > this.totalPages) return;
      this.fetchRecords(page);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    async refreshRecords() {
      await this.fetchRecords(this.currentPage);
      await this.fetchStatistics();
    },
    getImageUrl(imagePath) {
      if (!imagePath) return '';
      if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
        return imagePath;
      }
      const baseURL = window.location.origin;
      return `${baseURL}${imagePath}`;
    },
    formatTime(time) {
      if (!time) return '--';

      // 确保时间字符串格式正确
      let timeStr = time;
      if (typeof time === 'string') {
        // 将 "YYYY-MM-DD HH:mm:ss" 转换为 "YYYY-MM-DDTHH:mm:ss"
        timeStr = time.replace(' ', 'T');
      }

      const date = new Date(timeStr);

      // 检查日期是否有效
      if (isNaN(date.getTime())) {
        return time; // 如果解析失败，返回原始字符串
      }

      const now = new Date();
      const diff = now - date;
      
      if (diff < 60000) {
        return '刚刚';
      }
      if (diff < 3600000) {
        return `${Math.floor(diff / 60000)}分钟前`;
      }
      if (diff < 86400000) {
        return `${Math.floor(diff / 3600000)}小时前`;
      }
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  }
};
</script>

<style scoped>
.records-page {
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

/* 主要内容 */
.main-content {
  padding: 32px;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--border-radius);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg {
  width: 28px;
  height: 28px;
  color: var(--primary-blue);
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: var(--gray-500);
  margin: 0 0 4px 0;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--gray-900);
  margin: 0;
}

/* 记录部分 */
.records-section {
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
  gap: 12px;
  align-items: center;
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

.sort-select {
  padding: 8px 16px;
  border: 2px solid var(--gray-200);
  border-radius: var(--border-radius-sm);
  font-size: 14px;
  background: var(--white);
  color: var(--gray-700);
  cursor: pointer;
  transition: var(--transition);
  min-width: 160px;
}

.sort-select:focus {
  outline: none;
  border-color: var(--primary-blue);
}

.btn-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--border-radius-sm);
  background: var(--ultra-light-blue);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}

.btn-icon:hover {
  background: var(--light-blue);
}

.btn-icon svg {
  width: 18px;
  height: 18px;
  color: var(--primary-blue);
}

/* 加载状态 */
.loading-state {
  text-align: center;
  padding: 64px 32px;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  margin: 0 auto 16px;
  border: 4px solid var(--light-blue);
  border-top-color: var(--primary-blue);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 空状态 */
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
  margin: 0 0 8px 0;
}

.empty-hint {
  font-size: 14px;
  color: var(--gray-400);
  margin: 0;
}

/* 表格样式 */
.table-container {
  overflow-x: auto;
}

.records-table {
  width: 100%;
  border-collapse: collapse;
}

.records-table thead tr {
  background: var(--gray-50);
}

.records-table th {
  padding: 16px;
  text-align: center;
  font-size: 14px;
  font-weight: 600;
  color: var(--gray-700);
  border-bottom: 2px solid var(--gray-200);
}

.records-table th:nth-child(3) {
  text-align: left;
}

.records-table td {
  padding: 12px 16px;
  font-size: 14px;
  color: var(--gray-800);
  border-bottom: 1px solid var(--gray-100);
  vertical-align: middle;
  text-align: center;
}

.records-table td:nth-child(3) {
  text-align: left;
}

.table-row {
  transition: var(--transition);
}

.table-row:hover {
  background: var(--ultra-light-blue);
}

.time-cell {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: flex-start;
}

.time-icon {
  width: 16px;
  height: 16px;
  color: var(--gray-400);
  flex-shrink: 0;
}

.thumbnail-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.thumbnail {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  transition: var(--transition);
  border: 2px solid var(--gray-200);
  display: block;
  margin: 0 auto;
}

.thumbnail:hover {
  border-color: var(--primary-blue);
  transform: scale(1.05);
}

.no-thumbnail {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gray-100);
  color: var(--gray-400);
  border-radius: var(--border-radius-sm);
  font-size: 12px;
}

.result-badge {
  display: inline-block;
  padding: 6px 12px;
  background: var(--ultra-light-blue);
  color: var(--primary-blue);
  border-radius: var(--border-radius-sm);
  font-weight: 500;
  font-size: 13px;
}

.action-buttons {
  display: flex;
  gap: 8px;
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

.btn-view {
  background: var(--ultra-light-blue);
  color: var(--primary-blue);
}

.btn-view:hover {
  background: var(--light-blue);
}

.btn-delete {
  background: #fee2e2;
  color: var(--error);
}

.btn-delete:hover {
  background: #fecaca;
}

/* 分页 */
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

/* 弹窗 */
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
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
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

.detail-item {
  margin-bottom: 16px;
}

.detail-item label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: var(--gray-700);
  margin-bottom: 8px;
}

.detail-item span {
  display: block;
  font-size: 14px;
  color: var(--gray-600);
  padding: 12px;
  background: var(--gray-50);
  border-radius: var(--border-radius-sm);
}

.detail-item .result-badge {
  display: inline-block;
  padding: 8px 16px;
  background: var(--ultra-light-blue);
  color: var(--primary-blue);
  border-radius: var(--border-radius-sm);
  font-weight: 500;
}

.detail-image {
  margin-top: 24px;
}

.detail-image label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: var(--gray-700);
  margin-bottom: 12px;
}

.detail-image img {
  width: 100%;
  max-height: 400px;
  object-fit: contain;
  border-radius: var(--border-radius-sm);
  border: 2px solid var(--gray-200);
  background: var(--gray-50);
}

/* 弹窗动画 */
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

/* 响应式设计 */
@media (max-width: 768px) {
  .main-content {
    padding: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
    margin-bottom: 16px;
    padding-bottom: 12px;
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

  .sort-select {
    flex: 1;
    min-width: 150px;
    padding: 10px 12px;
    font-size: 14px;
  }

  .btn-icon {
    width: 40px;
    height: 40px;
    flex-shrink: 0;
  }

  .table-container {
    overflow-x: scroll;
  }

  .records-table {
    min-width: 600px;
  }
}
</style>