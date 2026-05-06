import axios from 'axios';

// 创建 axios 实例
const http = axios.create({
  baseURL: '/api', // API 基础路径
  timeout: 30000, // 请求超时时间
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
http.interceptors.request.use(
  config => {
    // 从 localStorage 获取 token
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器
http.interceptors.response.use(
  response => {
    return response.data;
  },
  error => {
    // 处理错误响应
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 未授权，清除 token
          localStorage.removeItem('token');
          localStorage.removeItem('userInfo');
          // 只在当前不在登录页时才跳转
          if (window.location.pathname !== '/login') {
            alert('登录已过期，请重新登录');
            window.location.href = '/login';
          }
          break;
        case 403:
          // alert('没有权限访问');
          break;
        case 404:
          // alert('请求的资源不存在');
          break;
        case 500:
          // alert('服务器错误');
          break;
          // default:
          // alert(error.response.data.message || '请求失败');
      }
    } else if (error.request) {
      // 只在真正的网络错误时才弹出提示（没有收到响应）
      alert('网络错误，请检查您的网络连接');
    }
    // 移除了"请求配置错误"的alert，因为这类错误应该由具体业务处理
    return Promise.reject(error);
  }
);

// ==================== 用户认证相关接口 ====================

/**
 * 用户登录
 * @param {Object} data - 登录信息
 * @param {string} data.phone - 手机号
 * @param {string} data.password - 密码
 * @returns {Promise}
 */
export const login = (data) => {
  return http.post('/login', data);
};

/**
 * 发送注册验证码
 * @param {Object} data - 手机号信息
 * @param {string} data.phone - 手机号
 * @returns {Promise}
 */
export const sendRegisterCode = (data) => {
  return http.post('/send-code', data);
};

/**
 * 用户注册
 * @param {Object} data - 注册信息
 * @param {string} data.phone - 手机号
 * @param {string} data.code - 验证码
 * @param {string} data.password - 密码
 * @returns {Promise}
 */
export const register = (data) => {
  return http.post('/register', data);
};

/**
 * 退出登录
 * @returns {Promise}
 */
export const logout = () => {
  return http.post('/logout');
};

/**
 * 获取当前用户信息
 * @returns {Promise}
 */
export const getUserInfo = () => {
  return http.get('/user/info');
};


// ==================== 疾病识别相关接口 ====================
/**
 * 上传图片进行疾病识别
 * @param {FormData} formData - 包含图片文件的 FormData
 * @returns {Promise}
 */
export const uploadImage = (formData) => {
  return http.post('/heatmap/generate', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};

// ==================== 识别记录管理接口 ====================

/**
 * 获取识别记录列表
 * @param {Object} params - 查询参数
 * @param {number} params.user_id - 用户ID（必填）
 * @param {number} params.page - 页码（默认1）
 * @param {number} params.page_size - 每页数量（默认10）
 * @returns {Promise}
 */
export const getRecordList = (params) => {
  return http.get('/records', { params });
};

/**
 * 获取单条识别记录详情
 * @param {number} id - 记录ID
 * @param {number} user_id - 用户ID
 * @returns {Promise}
 */
export const getRecordDetail = (id, user_id) => {
  return http.get(`/records/${id}`, { params: { user_id } });
};

/**
 * 新增记录
 * @param {Object} data - 保存的记录数据
 * @returns {Promise}
 */
export const addRecord = (data) => {
  return http.post('/record/add', data);
};

/**
 * 删除识别记录
 * @param {number} id - 记录ID
 * @param {number} user_id - 用户ID
 * @returns {Promise}
 */
export const deleteRecord = (id, user_id) => {
  return http.delete(`/records/${id}`, { params: { user_id } });
};

/**
 * 获取统计数据
 * @param {Object} params - 查询参数
 * @param {number} params.user_id - 用户ID（必填）
 * @returns {Promise}
 */
export const getStatistics = (params) => {
  return http.get('/records/statistics', { params });
};

// ==================== 用户管理接口 ====================

/**
 * 获取用户列表（仅管理员）
 * @param {Object} params - 查询参数
 * @param {number} params.current_user_id - 当前管理员ID
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @param {string} params.keyword - 搜索关键词
 * @returns {Promise}
 */
export const getUserList = (params) => {
  return http.get('/users', { params });
};

/**
 * 获取用户详情（仅管理员）
 * @param {number} userId - 用户ID
 * @param {number} current_user_id - 当前管理员ID
 * @returns {Promise}
 */
export const getUserDetail = (userId, current_user_id) => {
  return http.get(`/users/${userId}`, { params: { current_user_id } });
};

/**
 * 更新用户信息（仅管理员）
 * @param {number} userId - 用户ID
 * @param {number} current_user_id - 当前管理员ID
 * @param {Object} data - 更新数据
 * @returns {Promise}
 */
export const updateUser = (userId, current_user_id, data) => {
  return http.put(`/users/${userId}`, data, { params: { current_user_id } });
};

/**
 * 修改用户密码
 * @param {Object} data - 修改数据
 * @param {number} data.user_id - 用户ID
 * @param {string} data.password - 新密码
 * @returns {Promise}
 */
export const updatePassword = (data) => {
  return http.put(`/users/${data.user_id}/password`, { password: data.password }, { params: { current_user_id: data.user_id } });
};

/**
 * 封禁/解封用户（仅管理员）
 * @param {number} userId - 用户ID
 * @param {number} current_user_id - 当前管理员ID
 * @param {number} is_banned - 是否封禁：1-封禁，0-解封
 * @returns {Promise}
 */
export const banUser = (userId, current_user_id, is_banned) => {
  return http.put(`/users/${userId}/ban`, { is_banned }, { params: { current_user_id } });
};

/**
 * 切换用户角色（仅管理员）
 * @param {number} userId - 用户ID
 * @param {number} current_user_id - 当前管理员ID
 * @returns {Promise}
 */
export const toggleUserRole = (userId, current_user_id) => {
  return http.put(`/users/${userId}/role`, {}, { params: { current_user_id } });
};

/**
 * 获取图片完整URL
 * @param {string} imagePath - 图片相对路径
 * @returns {string} 完整的图片URL
 */
export const getImageUrl = (imagePath) => {
  if (!imagePath) return '';
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
    return imagePath;
  }
  const baseURL = http.defaults.baseURL.replace('/api', '');
  return `${baseURL}${imagePath}`;
};


// 导出 http 实例供其他地方使用
export default http;