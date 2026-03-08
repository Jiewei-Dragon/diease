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
          // 未授权，清除 token 并跳转到登录页
          localStorage.removeItem('token');
          localStorage.removeItem('userInfo');
          window.location.href = '/login';
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
  return http.post('/api/user/logout');
};

/**
 * 获取当前用户信息
 * @returns {Promise}
 */
export const getUserInfo = () => {
  return http.get('/api/user/info');
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
 * @param {number} params.page - 页码（默认1）
 * @param {number} params.pageSize - 每页数量（默认10）
 * @param {string} params.diseaseType - 疾病类型（可选）
 * @param {string} params.startDate - 开始日期（可选）
 * @param {string} params.endDate - 结束日期（可选）
 * @returns {Promise}
 */
export const getRecordList = (params) => {
  return http.get('/records', { params });
};

/**
 * 获取单条识别记录详情
 * @param {string} id - 记录ID
 * @returns {Promise}
 */
export const getRecordDetail = (id) => {
  return http.get(`/records/${id}`);
};

/**
 * 新增记录
 * @param {Object} data - 保存的记录数据
 * @returns {Promise}
 */
export const addRecord = (data) => { // 修正语法：=> 改为 =，并接收参数data
  return http.post(`/record/add`, data); // 传递请求体参数
};

/**
 * 删除识别记录
 * @param {string} id - 记录ID
 * @returns {Promise}
 */
export const deleteRecord = (id) => {
  return http.delete(`/records/${id}`);
};

/**
 * 批量删除识别记录
 * @param {Object} data - 删除信息
 * @param {Array<string>} data.ids - 记录ID数组
 * @returns {Promise}
 */
export const batchDeleteRecords = (data) => {
  return http.post('/api/records/batch-delete', data);
};


/**
 * 获取统计数据
 * @param {Object} params - 查询参数
 * @param {string} params.startDate - 开始日期（可选）
 * @param {string} params.endDate - 结束日期（可选）
 * @returns {Promise}
 */
export const getStatistics = (params) => {
  return http.get('/api/records/statistics', { params });
};


// 导出 http 实例供其他地方使用
export default http;