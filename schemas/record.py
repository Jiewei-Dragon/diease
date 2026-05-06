import re

from pydantic import BaseModel, Field, field_validator

class RecordAddRequest(BaseModel):
    """保存识别记录的请求参数模型"""
    user_id: int = Field(..., description="用户ID")
    disease_type: int = Field(..., description="病害类型编码（如3=Rust）")
    disease_name: str = Field(..., max_length=50, description="病害名称（如Rust）")
    origin_image: str = Field(..., description="原图Base64字符串")
    heatmap_image: str = Field(..., description="热力图Base64字符串")
    confidence: float = Field(..., ge=0, le=1, description="识别置信度（0-1）")