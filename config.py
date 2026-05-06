import os

# ==================== 基础路径配置 ====================
# 获取项目根目录（main.py 所在目录）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==================== 数据库配置 ====================
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/diease"

# ==================== JWT 配置 ====================
JWT_SECRET_KEY = "your-secret-key-here"  # 替换为随机字符串（建议32位以上）
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ==================== 服务器配置 ====================
# FastAPI 后端服务配置
API_HOST = "0.0.0.0"
API_PORT = 8000

# Vite 前端开发服务器配置
VITE_HOST = "0.0.0.0"
VITE_PORT = 3000

# 后端地址（开发环境）
VITE_API_TARGET = "http://localhost:8000"

# ==================== 模型配置 ====================
# 模型文件路径
MODEL_DIR = os.path.join(BASE_DIR, "resource")
MODEL_PTH_PATH = os.path.join(MODEL_DIR, "LayerScale2d+ECA.pth")

# 病害类别（按文件夹顺序）
DISEASE_CLASSES = ['Healthy', 'Rot', 'Rust', 'Scab']

# 图像预处理参数
IMAGE_SIZE_RESIZE = 256        # 先缩放到这个尺寸
IMAGE_SIZE_CROP = 224          # 然后中心裁剪到这个尺寸
IMAGE_NORMALIZE_MEAN = [0.485, 0.456, 0.406]  # ImageNet 均值
IMAGE_NORMALIZE_STD = [0.229, 0.224, 0.225]   # ImageNet 标准差

# 推理设备配置 ("cuda", "cpu", 或 "auto" 自动选择)
INFERENCE_DEVICE = "cuda"

# ==================== 文件上传配置 ====================
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
ORIGIN_IMAGE_DIR = os.path.join(UPLOAD_DIR, "origin")
HEATMAP_IMAGE_DIR = os.path.join(UPLOAD_DIR, "heatmap")

# ==================== 其他配置 ====================
# 允许的图片来源（CORS 配置，如果需要的话）
ALLOWED_ORIGINS = ["*"]  # 生产环境建议指定具体域名
