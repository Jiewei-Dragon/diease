<template>
  <div class="main-page">
    <!-- 顶部导航栏 -->
    <header class="header">
      <div class="header-content">
        <div class="header-left">
          <svg class="logo-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span class="app-name">葡萄叶部病害识别系统</span>
        </div>
        <div class="header-right">
          <div class="user-info" @click="goToProfile" title="点击修改密码">
            <svg class="user-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 21C20 19.6044 20 18.9067 19.8278 18.3389C19.44 17.0605 18.4395 16.06 17.1611 15.6722C16.5933 15.5 15.8956 15.5 14.5 15.5H9.5C8.10444 15.5 7.40665 15.5 6.83886 15.6722C5.56045 16.06 4.56004 17.0605 4.17224 18.3389C4 18.9067 4 19.6044 4 21M16.5 7.5C16.5 9.98528 14.4853 12 12 12C9.51472 12 7.5 9.98528 7.5 7.5C7.5 5.01472 9.51472 3 12 3C14.4853 3 16.5 5.01472 16.5 7.5Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span class="user-phone">{{ userPhone }}</span>
            <svg class="edit-indicator" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V20C2 20.5304 2.21071 21.0391 2.58579 21.4142C2.96086 21.7893 3.46957 22 4 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V13M18.5 2.50001C18.8978 2.10219 19.4374 1.87869 20 1.87869C20.5626 1.87869 21.1022 2.10219 21.5 2.50001C21.8978 2.89784 22.1213 3.4374 22.1213 4.00001C22.1213 4.56262 21.8978 5.10219 21.5 5.50001L12 15L8 16L9 12L18.5 2.50001Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <button
            v-if="isAdmin"
            @click="goToUsers"
            class="btn-users btn-primary"
          >
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21M23 21V19C22.9993 18.1137 22.7044 17.2528 22.1614 16.5523C21.6184 15.8519 20.8581 15.3516 20 15.13M16 3.13C16.8604 3.35031 17.623 3.85071 18.1676 4.55232C18.7122 5.25392 19.0078 6.11683 19.0078 7.005C19.0078 7.89318 18.7122 8.75608 18.1676 9.45769C17.623 10.1593 16.8604 10.6597 16 10.88C15.1396 11.1003 14.377 10.6007 13.8324 9.89909C13.2878 9.1975 12.9922 8.3346 12.9922 7.445C12.9922 6.5554 13.2878 5.6925 13.8324 4.99091C14.377 4.28932 15.1396 3.78972 16 3.57M13 7C13 9.20914 11.2091 11 9 11C6.79086 11 5 9.20914 5 7C5 4.79086 6.79086 3 9 3C11.2091 3 13 4.79086 13 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            用户管理
          </button>
          <button @click="goToRecords" class="btn-records btn-primary">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15M9 5C9 6.10457 9.89543 7 11 7H13C14.1046 7 15 6.10457 15 5M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            识别记录
          </button>
          <button @click="logout" class="btn-logout btn-secondary">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9M16 17L21 12M21 12L16 7M21 12H9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            退出登录
          </button>
        </div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="main-content">
      <div class="content-wrapper">
        <!-- 上传区域 -->
        <section class="upload-section card">
          <h2 class="section-title">上传图片进行识别</h2>
          <p class="section-subtitle">支持 JPG、PNG、JPEG 格式，建议图片大小不超过 10MB</p>
          
          <div 
            class="upload-area" 
            :class="{ 'dragging': isDragging, 'has-image': uploadedImage }"
            @click="uploadImage"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleDrop"
          >
            <input 
              type="file" 
              ref="fileInput" 
              @change="onFileChange" 
              accept="image/*" 
              hidden 
            />
            <input
              type="file"
              ref="cameraInput"
              @change="onCameraCapture"
              accept="image/*"
              capture="environment"
              hidden
            />

            <div v-if="!uploadedImage" class="upload-placeholder">
              <svg class="upload-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15M17 8L12 3M12 3L7 8M12 3V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <p class="upload-text">点击或拖拽图片到此区域</p>
              <p class="upload-hint">支持单张图片上传</p>
              <button @click.stop="openCamera" class="btn-camera">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M23 19C23 19.5304 22.7893 20.0391 22.4142 20.4142C22.0391 20.7893 21.5304 21 21 21H3C2.46957 21 1.96086 20.7893 1.58579 20.4142C1.21071 20.0391 1 19.5304 1 19V8C1 7.46957 1.21071 6.96086 1.58579 6.58579C1.96086 6.21071 2.46957 6 3 6H7L9 3H15L17 6H21C21.5304 6 22.0391 6.21071 22.4142 6.58579C22.7893 6.96086 23 7.46957 23 8V19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M12 17C14.2091 17 16 15.2091 16 13C16 10.7909 14.2091 9 12 9C9.79086 9 8 10.7909 8 13C8 15.2091 9.79086 17 12 17Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                拍照上传
              </button>
            </div>

            <div v-else class="image-preview">
              <img :src="uploadedImage" alt="上传的图片" />
              <button @click.stop="clearImage" class="btn-clear">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </div>
          </div>

          <button 
            v-if="uploadedImage && !isRecognizing" 
            @click="startRecognition" 
            class="btn-recognize btn-primary"
          >
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            开始识别
          </button>
        </section>

        <!-- 识别结果区域 -->
        <transition name="slide-fade">
          <section v-if="isRecognizing || recognitionResult" class="results-section">
            <!-- 识别中状态 -->
            <div v-if="isRecognizing" class="card recognition-loading">
              <div class="loading-spinner"></div>
              <h3>正在识别中...</h3>
              <p>AI 正在分析您的图片，请稍候</p>
            </div>

            <!-- 识别结果 -->
            <div v-else-if="recognitionResult" class="results-grid">
              <!-- 热力图 -->
              <div class="card heatmap-card">
                <h3 class="card-title">热力图分析</h3>
                <div class="heatmap-container">
                  <img v-if="heatmapImage" :src="heatmapImage" alt="热力图" />
                  <div v-else class="no-heatmap">暂无热力图数据</div>
                </div>
              </div>

              <!-- 识别结果详情 -->
              <div class="card result-card">
                <h3 class="card-title">识别结果</h3>
                <div class="result-content">
                  <div class="result-status">
                    <svg class="status-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <span>识别完成</span>
                  </div>
                  <div class="result-detail">
                    <p>{{ recognitionResult }}</p>
                  </div>
                  
                  <div class="result-actions">
                    <button @click="saveRecord" class="btn-save btn-primary" :disabled="isSaving">
                      <span v-if="!isSaving">
                        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                          <path d="M19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H16L21 8V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                          <path d="M17 21V13H7V21M7 3V8H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        保存记录
                      </span>
                      <span v-else class="saving-text">
                        <span class="saving-spinner"></span>
                        保存中...
                      </span>
                    </button>
                    <button @click="continueRecognition" class="btn-continue btn-secondary" :disabled="isSaving">
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M4 4V9H4.58152M19.9381 11C19.446 7.05369 16.0796 4 12 4C8.64262 4 5.76829 6.06817 4.58152 9M4.58152 9H9M20 20V15H19.4185M19.4185 15C18.2317 17.9318 15.3574 20 12 20C7.92038 20 4.55399 16.9463 4.06189 13M19.4185 15H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                      继续识别
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </transition>
      </div>
    </main>

    <!-- 保存成功弹窗 -->
    <transition name="fade">
      <div v-if="showSuccessDialog" class="dialog-overlay" @click.self="closeSuccessDialog">
        <div class="dialog-container">
          <div class="dialog-header">
            <svg class="success-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <h3 class="dialog-title">保存成功</h3>
          </div>
          <div class="dialog-body">
            <p class="dialog-message">记录已保存成功！可以在"识别记录"页面查看</p>
          </div>
          <div class="dialog-footer">
            <button @click="closeSuccessDialog" class="btn-dialog btn-secondary">
              确定
            </button>
            <button @click="goToRecordPage" class="btn-dialog btn-primary">
              去查看
            </button>
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
      userPhone: '',
      userId: null,
      isAdmin: false,
      uploadedImage: '',
      heatmapImage: '',
      recognitionResult: '',

      recognitionData: {
        disease_type: 0,
        disease_name: '',
        confidence: 0.0,
        heatmapImage: '',
        all_predictions: {}
      },

      isRecognizing: false,
      isSaving: false,
      isDragging: false,
      selectedFile: null,
      currentRecordId: null,
      showSuccessDialog: false
    };
  },
  mounted() {
    this.loadUserInfo();
  },
  methods: {
    async loadUserInfo() {
      try {
        const userInfo = localStorage.getItem('userInfo');
        if (userInfo) {
          const user = JSON.parse(userInfo);
          this.userPhone = user.phone || '未登录';
          this.userId = user.id || null;
          this.isAdmin = user.is_admin === 1;
        } else {
          const response = await this.$api.getUserInfo();
          if (response.data) {
            this.userPhone = response.data.phone || '未登录';
            this.userId = response.data.id || null;
            this.isAdmin = response.data.is_admin === 1;
            localStorage.setItem('userInfo', JSON.stringify(response.data));
          }
        }
      } catch (error) {
        console.error('Failed to load user info:', error);
        this.userPhone = '未登录';
        this.userId = null;
        this.isAdmin = false;
      }
    },
    async logout() {
      try {
        await this.$api.logout();
      } catch (error) {
        console.error('Logout error:', error);
      } finally {
        localStorage.removeItem('token');
        localStorage.removeItem('userInfo');
        this.$router.push('/login');
      }
    },
    goToUsers() {
      this.$router.push('/users');
    },
    goToRecords() {
      this.$router.push('/record');
    },
    goToProfile() {
      this.$router.push('/profile');
    },
    uploadImage() {
      this.$refs.fileInput.click();
    },
    openCamera() {
      this.$refs.cameraInput.click();
    },
    onCameraCapture(event) {
      const file = event.target.files[0];
      if (file) {
        this.handleFile(file);
      }
    },
    onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.handleFile(file);
      }
    },
    handleDrop(event) {
      this.isDragging = false;
      const file = event.dataTransfer.files[0];
      if (file && file.type.startsWith('image/')) {
        this.handleFile(file);
      }
    },
    handleFile(file) {
      const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
      const maxSize = 10 * 1024 * 1024;

      if (!validTypes.includes(file.type)) {
        alert('请上传 JPG、PNG 或 JPEG 格式的图片');
        return;
      }

      if (file.size > maxSize) {
        alert('图片大小不能超过 10MB');
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        this.uploadedImage = e.target.result;
      };
      reader.readAsDataURL(file);

      this.selectedFile = file;
    },
    clearImage() {
      this.uploadedImage = '';
      this.heatmapImage = '';
      this.recognitionResult = '';
      this.selectedFile = null;
      this.$refs.fileInput.value = '';
    },
    async startRecognition() {
      if (!this.selectedFile) {
        alert('请先上传图片');
        return;
      }

      this.isRecognizing = true;
      this.recognitionResult = '';
      this.heatmapImage = '';
      this.currentRecordId = null;

      const formData = new FormData();
      formData.append('image', this.selectedFile);

      try {
        const response = await this.$api.uploadImage(formData);
        
        if (response.code === 200 && response.data) {
          this.recognitionData = {
            disease_type: response.data.disease_type,
            disease_name: response.data.disease_name,
            confidence: response.data.confidence,
            heatmapImage: response.data.heatmapImage,
            all_predictions: response.data.all_predictions
          };
          this.currentRecordId = response.data.id;
          this.recognitionResult = response.data.disease_name || '未检测到病害';
          
          if (response.data.heatmapUrl) {
            this.heatmapImage = this.$api.getImageUrl(response.data.heatmapUrl);
          } else if (response.data.heatmapImage) {
            this.heatmapImage = response.data.heatmapImage;
          } else {
            this.heatmapImage = '';
          }

          if (response.data.confidence) {
            this.recognitionResult += ` (置信度: ${(response.data.confidence * 100).toFixed(2)}%)`;
          }
        } else {
          throw new Error(response.message || '识别失败');
        }
      } catch (error) {
        const errorMsg = error.response?.data?.message || error.message || '识别失败，请重试';
        alert(errorMsg);
        console.error('Recognition error:', error);
      } finally {
        this.isRecognizing = false;
      }
    },
    async saveRecord() {
      if (!this.selectedFile) {
        alert('没有可保存的识别记录');
        return;
      }

      if (!this.userId) {
        alert('用户未登录，请先登录');
        return;
      }

      this.isSaving = true;

      try {
        const originImageBase64 = await this.fileToBase64(this.selectedFile);

        const recordData = {
          user_id: this.userId,
          disease_type: this.recognitionData.disease_type,
          disease_name: this.recognitionData.disease_name,
          origin_image: originImageBase64,
          heatmap_image: this.recognitionData.heatmapImage,
          confidence: this.recognitionData.confidence,
        };

        const response = await this.$api.addRecord(recordData);

        this.isSaving = false;

        if (response.code === 200) {
          this.showSuccessDialog = true;
        } else {
          alert(`保存失败：${response.message || '服务器返回异常'}`);
        }
      } catch (error) {
        this.isSaving = false;
        const errorMsg = error.response?.data?.detail ||
                         error.response?.data?.message ||
                         error.message ||
                         '保存失败，请检查网络或重试';
        alert(`保存失败：${errorMsg}`);
        console.error('Save error:', error);
      }
    },
    goToRecordPage() {
      this.showSuccessDialog = false;
      this.$router.push('/record');
    },
    closeSuccessDialog() {
      this.showSuccessDialog = false;
    },
    fileToBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
      });
    },
    continueRecognition() {
      this.clearImage();
    }
  }
};
</script>

<style scoped>
.main-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, var(--ultra-light-blue) 0%, var(--white) 100%);
}

/* 顶部导航栏 */
.header {
  background: var(--white);
  box-shadow: var(--shadow-md);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 16px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 32px;
  height: 32px;
  color: var(--primary-blue);
}

.app-name {
  font-size: 20px;
  font-weight: 700;
  color: var(--gray-900);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--ultra-light-blue);
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  transition: var(--transition);
  user-select: none;
}

.user-info:hover {
  background: var(--light-blue);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.user-info:active {
  transform: translateY(0);
}

.user-icon {
  width: 20px;
  height: 20px;
  color: var(--primary-blue);
}

.user-phone {
  font-size: 14px;
  color: var(--gray-700);
  font-weight: 500;
}

.edit-indicator {
  width: 16px;
  height: 16px;
  color: var(--primary-blue);
  opacity: 0.6;
  transition: var(--transition);
}

.user-info:hover .edit-indicator {
  opacity: 1;
  transform: translateX(2px);
}

.btn-records {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  font-size: 14px;
}

.btn-records svg {
  width: 18px;
  height: 18px;
}

.btn-users {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  font-size: 14px;
}

.btn-users svg {
  width: 18px;
  height: 18px;
}

.btn-logout {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
}

.btn-logout svg {
  width: 18px;
  height: 18px;
}

/* 主要内容区域 */
.main-content {
  flex: 1;
  padding: 40px 32px;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
}

/* 上传区域 */
.upload-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--gray-900);
  margin-bottom: 8px;
}

.section-subtitle {
  font-size: 14px;
  color: var(--gray-500);
  margin-bottom: 24px;
}

.upload-area {
  border: 3px dashed var(--gray-300);
  border-radius: var(--border-radius);
  padding: 48px;
  text-align: center;
  cursor: pointer;
  transition: var(--transition);
  background: var(--gray-50);
  position: relative;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-area:hover {
  border-color: var(--primary-blue);
  background: var(--ultra-light-blue);
}

.upload-area.dragging {
  border-color: var(--primary-blue);
  background: var(--light-blue);
  transform: scale(1.02);
}

.upload-area.has-image {
  border-style: solid;
  background: var(--white);
  padding: 0;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.upload-icon {
  width: 64px;
  height: 64px;
  color: var(--primary-blue);
}

.upload-text {
  font-size: 18px;
  font-weight: 600;
  color: var(--gray-700);
  margin: 0;
}

.upload-hint {
  font-size: 14px;
  color: var(--gray-500);
  margin: 0;
}

.image-preview {
  width: 100%;
  height: 100%;
  position: relative;
  border-radius: var(--border-radius);
  overflow: hidden;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  max-height: 500px;
}

.btn-clear {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--white);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-lg);
  transition: var(--transition);
}

.btn-clear:hover {
  background: var(--error);
  transform: scale(1.1);
}

.btn-clear svg {
  width: 20px;
  height: 20px;
  color: var(--gray-700);
}

.btn-clear:hover svg {
  color: var(--white);
}

.btn-recognize {
  width: 100%;
  margin-top: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px;
  font-size: 16px;
}

.btn-recognize svg {
  width: 20px;
  height: 20px;
}

.btn-camera {
  margin-top: 16px;
  padding: 10px 20px;
  background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
  color: var(--white);
  border: none;
  border-radius: var(--border-radius-sm);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: var(--transition);
  box-shadow: var(--shadow-md);
}

.btn-camera:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn-camera svg {
  width: 18px;
  height: 18px;
}

/* 识别结果区域 */
.results-section {
  margin-top: 32px;
}

.recognition-loading {
  text-align: center;
  padding: 64px 32px;
}

.loading-spinner {
  width: 64px;
  height: 64px;
  margin: 0 auto 24px;
  border: 4px solid var(--light-blue);
  border-top-color: var(--primary-blue);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.recognition-loading h3 {
  font-size: 20px;
  color: var(--gray-900);
  margin-bottom: 8px;
}

.recognition-loading p {
  font-size: 14px;
  color: var(--gray-500);
}

.results-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--gray-900);
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid var(--gray-100);
}

.heatmap-container {
  border-radius: var(--border-radius-sm);
  overflow: hidden;
  background: var(--gray-50);
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.heatmap-container img {
  width: 100%;
  height: auto;
  display: block;
}

.no-heatmap {
  color: var(--gray-400);
  font-size: 14px;
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.result-status {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: var(--ultra-light-blue);
  border-radius: var(--border-radius-sm);
  border-left: 4px solid var(--primary-blue);
}

.status-icon {
  width: 24px;
  height: 24px;
  color: var(--success);
}

.result-status span {
  font-size: 16px;
  font-weight: 600;
  color: var(--gray-900);
}

.result-detail {
  padding: 20px;
  background: var(--gray-50);
  border-radius: var(--border-radius-sm);
  border: 1px solid var(--gray-200);
}

.result-detail p {
  font-size: 15px;
  line-height: 1.6;
  color: var(--gray-700);
  margin: 0;
}

.result-actions {
  display: flex;
  gap: 12px;
}

.result-actions button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
}

.result-actions svg {
  width: 18px;
  height: 18px;
}

.saving-text {
  display: flex;
  align-items: center;
  gap: 8px;
}

.saving-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: var(--white);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.btn-save:disabled,
.btn-continue:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none !important;
}

/* 过渡动画 */
.slide-fade-enter-active {
  transition: all 0.4s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s ease-in;
}

.slide-fade-enter-from {
  transform: translateY(20px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .results-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .header-content {
    padding: 12px 16px;
    flex-direction: column;
    gap: 12px;
  }

  .header-right {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px;
    width: 100%;
  }

  .user-info {
    order: -1;
    width: 100%;
    justify-content: center;
    padding: 10px 16px;
    margin-bottom: 4px;
  }

  .user-phone {
    font-size: 13px;
  }

  .edit-indicator {
    display: none;
  }

  .btn-users,
  .btn-records,
  .btn-logout {
    padding: 8px 12px;
    font-size: 13px;
    flex: 1;
    min-width: calc(33.333% - 6px);
    justify-content: center;
  }

  .btn-users svg,
  .btn-records svg,
  .btn-logout svg {
    width: 16px;
    height: 16px;
  }

  .main-content {
    padding: 24px 16px;
  }

  .upload-area {
    padding: 32px 16px;
    min-height: 250px;
  }

  .section-title {
    font-size: 20px;
  }

  .result-actions {
    flex-direction: column;
  }

  .btn-save,
  .btn-continue {
    width: 100%;
    justify-content: center;
  }
}

/* 小屏幕手机优化 */
@media (max-width: 480px) {
  .header-content {
    padding: 10px 12px;
  }

  .app-name {
    font-size: 16px;
  }

  .logo-icon {
    width: 28px;
    height: 28px;
  }

  .user-info {
    padding: 8px 12px;
  }

  .user-icon {
    width: 18px;
    height: 18px;
  }

  .user-phone {
    font-size: 12px;
  }

  .btn-users,
  .btn-records,
  .btn-logout {
    padding: 7px 10px;
    font-size: 12px;
    min-width: calc(33.333% - 6px);
  }

  .btn-users svg,
  .btn-records svg,
  .btn-logout svg {
    width: 14px;
    height: 14px;
  }

  .main-content {
    padding: 16px 12px;
  }

  .upload-area {
    padding: 24px 12px;
    min-height: 200px;
  }

  .upload-icon {
    width: 48px;
    height: 48px;
  }

  .upload-text {
    font-size: 16px;
  }

  .section-title {
    font-size: 18px;
  }

  .section-subtitle {
    font-size: 12px;
  }

  .btn-camera {
    padding: 8px 16px;
    font-size: 13px;
  }

  .btn-camera svg {
    width: 16px;
    height: 16px;
  }
}

/* 弹窗样式 */
.dialog-overlay {
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
  backdrop-filter: blur(4px);
}

.dialog-container {
  background: var(--white);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-xl);
  max-width: 420px;
  width: 90%;
  animation: dialogSlideIn 0.3s ease-out;
}

@keyframes dialogSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.dialog-header {
  padding: 24px 24px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid var(--gray-100);
}

.success-icon {
  width: 32px;
  height: 32px;
  color: var(--success);
}

.dialog-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--gray-900);
  margin: 0;
}

.dialog-body {
  padding: 24px;
}

.dialog-message {
  font-size: 15px;
  color: var(--gray-700);
  line-height: 1.6;
  margin: 0;
}

.dialog-footer {
  padding: 16px 24px 24px;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-dialog {
  padding: 10px 24px;
  font-size: 14px;
  font-weight: 500;
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  transition: var(--transition);
  border: none;
  outline: none;
}

.btn-dialog.btn-secondary {
  background: var(--gray-100);
  color: var(--gray-700);
}

.btn-dialog.btn-secondary:hover {
  background: var(--gray-200);
}

.btn-dialog.btn-primary {
  background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
  color: var(--white);
  box-shadow: var(--shadow-md);
}

.btn-dialog.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

/* 淡入淡出动画 */
.fade-enter-active {
  transition: opacity 0.3s ease-out;
}

.fade-leave-active {
  transition: opacity 0.2s ease-in;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>