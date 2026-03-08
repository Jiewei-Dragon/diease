# classify_routes.py
import random
import re
import time

from fastapi import *
from sqlalchemy.orm import Session
import os
from handle.classify import classifyAndHeat_from_image
from config import *
from core.db import engine, Base, get_db
from core.response import success_response, error_response, ErrorCode
from core.jwt import generate_token
from models.user import TbUser
from schemas.user import LoginRequest, RegisterRequest

user_router = APIRouter(prefix="/api", tags=["用户相关接口"])

# 手机号校验函数（复刻原Go的isValidPhone）
def is_valid_phone(phone: str) -> bool:
    # 中国大陆手机号正则
    pattern = r"^1[3-9]\d{9}$"
    return re.match(pattern, phone) is not None

@user_router.post("/login", summary="用户登录接口")
async def login(
        login_request: LoginRequest,
        db: Session = Depends(get_db)
):
    # 1. 手机号格式校验
    if not is_valid_phone(login_request.Phone):
        return error_response(ErrorCode.ErrValidation, "手机号格式有误！")

    # 2. 数据库校验（对应原Go第二步）
    user = db.query(TbUser).filter(TbUser.Phone == login_request.Phone).first()
    if not user:
        return error_response(ErrorCode.ErrValidation, "用户不存在！")

    # 密码校验
    if user.Password != login_request.Password:
        return error_response(ErrorCode.ErrValidation, "密码错误！")

    # 3. 生成JWT Token
    try:
        token = generate_token(user.Phone)
    except Exception as e:
        return error_response(ErrorCode.ErrUnknown, "生成 Token 失败")

    # 4. 返回响应
    return success_response({
        "token": token,
        "userInfo": {
            "id": user.ID,
            "phone": user.Phone
        }
    })


@user_router.post("/send-code", summary="发送登录验证码")
def SendVerifyCode():
    # 生成6位随机验证码
    # Python 的 random 无需手动设置种子，内部已做优化
    code = random.randint(100000, 999999)
    # 3. 返回成功响应
    return {
        "msg": "验证码发送成功",
        "code": code  # 注意：生产环境不要返回真实验证码！
    }

# ---------------------- 注册接口 ----------------------
@user_router.post("/register", summary="用户注册接口")
def register(
        register_request: RegisterRequest,
        db: Session = Depends(get_db)
):
    # 1. 检查手机号是否已注册
    existing_user = db.query(TbUser).filter(TbUser.Phone == register_request.phone).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="该手机号已被注册！")

    # 2. 创建新用户
    new_user = TbUser(
        Phone=register_request.phone,
        Password=register_request.password
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # 刷新获取完整的用户对象
    except Exception as e:
        db.rollback()  # 出错时回滚
        raise HTTPException(status_code=500, detail=f"注册失败，请稍后重试：{str(e)}")

    # 3. 返回成功响应
    return {"code": 200, "msg": "注册成功！", "data": {}}