import re

from pydantic import BaseModel, Field, field_validator


class LoginRequest(BaseModel):
    """登录请求体"""
    Phone: str = Field(..., description="手机号")
    Password: str = Field(..., description="密码")

    # Pydantic v2 配置（兼容字段名大小写，和Go保持一致）
    model_config = {
        "populate_by_name": True,
        "alias_generator": lambda x: x  # 保留原始字段名（Phone而非phone）
    }


class RegisterRequest(BaseModel):
    code: str = Field(..., description="验证码（必填）")  # binding:"required" 对应 ...
    phone: str = Field(..., description="手机号（必填）")  # binding:"required" 对应 ...
    password: str = Field(None, min_length=6, max_length=20, description="密码（可选，6-20位）")  # binding:"omitempty,min=6,max=20"
    repeat_password: str = Field(None, min_length=6, max_length=20, description="重复密码（可选，6-20位）")  # binding:"omitempty,min=6,max=20"

    # 1. 手机号格式校验（和 Go 端 isValidPhone 逻辑一致）
    @field_validator('phone')
    def validate_phone_format(cls, v):
        pattern = r'^1[3-9]\d{9}$'
        if not re.match(pattern, v):
            raise ValueError("手机号格式有误！")
        return v

    # 2. 密码一致性校验（仅当密码字段存在时校验）
    @field_validator('repeat_password')
    def validate_password_match(cls, v, values):
        # 获取已校验的 password 字段值
        password = values.data.get('password')
        # 只有当 password 存在时，才校验一致性
        if password is not None and v != password:
            raise ValueError("密码不一致！")
        return v
