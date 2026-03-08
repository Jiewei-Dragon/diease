import re

from pydantic import BaseModel, Field, field_validator

class RecordAddRequest(BaseModel):
    """保存识别记录的请求参数模型（和前端postData对应）"""
    # 基础配置（可选，解决特殊类型兼容问题）
    model_config = {
        "arbitrary_types_allowed": True  # 兜底：允许任意类型，避免schema生成错误
    }
    # 正确的字段定义：类型注解 + 可选Field描述（无错误参数）
    disease_type: int = Field(..., description="病害类型编码（如3=Rust）")
    disease_name: str = Field(..., max_length=50, description="病害名称（如Rust）")
    heatmap_image: str = Field(..., description="热力图Base64字符串")
    confidence: float = Field(..., ge=0, le=1, description="识别置信度（0-1）")