# classify_routes.py
import random
import re
import time

from fastapi import *
from sqlalchemy.orm import Session
import os
from datetime import datetime
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
    if not is_valid_phone(login_request.Phone):
        return error_response(ErrorCode.ErrValidation, "手机号格式有误！")

    user = db.query(TbUser).filter(TbUser.Phone == login_request.Phone).first()
    if not user:
        return error_response(ErrorCode.ErrValidation, "用户不存在！")

    if user.Password != login_request.Password:
        return error_response(ErrorCode.ErrValidation, "密码错误！")
    
    if user.IsBanned == 1:
        return error_response(ErrorCode.ErrValidation, "账号已被封禁，请联系管理员！")

    try:
        token = generate_token(user.Phone)
    except Exception as e:
        return error_response(ErrorCode.ErrUnknown, "生成 Token 失败")

    return success_response({
        "token": token,
        "userInfo": {
            "id": user.ID,
            "phone": user.Phone,
            "is_admin": user.IsAdmin
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
    now = datetime.now()
    new_user = TbUser(
        Phone=register_request.phone,
        Password=register_request.password,
        CreateTime=now,
        UpdateTime=now
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


@user_router.get("/users", summary="获取用户列表（仅管理员）")
async def get_users(
        current_user_id: int = Query(..., description="当前管理员ID"),
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(10, ge=1, le=100, description="每页数量"),
        keyword: str = Query(None, description="搜索关键词（手机号）"),
        db: Session = Depends(get_db)
):
    try:
        # 验证当前用户是否为管理员
        current_user = db.query(TbUser).filter(TbUser.ID == current_user_id).first()
        if not current_user or current_user.IsAdmin != 1:
            raise HTTPException(status_code=403, detail="无权限访问")
        
        # 构建查询
        query = db.query(TbUser)
        
        # 关键词搜索
        if keyword:
            query = query.filter(TbUser.Phone.like(f"%{keyword}%"))
        
        # 查询总数
        total = query.count()
        
        # 分页查询
        offset = (page - 1) * page_size
        users = query.order_by(TbUser.ID.desc()).offset(offset).limit(page_size).all()
        
        # 格式化数据
        user_list = []
        for user in users:
            create_time = format_datetime(user.CreateTime)
            user_list.append({
                "id": user.ID,
                "phone": user.Phone,
                "is_admin": user.IsAdmin,
                "is_banned": user.IsBanned,
                "create_time": create_time
            })
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "list": user_list,
                "total": total,
                "page": page,
                "page_size": page_size
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户列表失败：{str(e)}")


@user_router.put("/users/{user_id}", summary="修改用户信息（仅管理员）")
async def update_user(
        user_id: int,
        current_user_id: int = Query(..., description="当前管理员ID"),
        phone: str = Body(None, description="手机号"),
        password: str = Body(None, description="密码"),
        is_banned: int = Body(None, description="是否封禁"),
        db: Session = Depends(get_db)
):
    try:
        # 验证当前用户是否为管理员
        current_user = db.query(TbUser).filter(TbUser.ID == current_user_id).first()
        if not current_user or current_user.IsAdmin != 1:
            raise HTTPException(status_code=403, detail="无权限访问")
        
        # 查询要修改的用户
        user = db.query(TbUser).filter(TbUser.ID == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 防止管理员修改自己的权限
        if user_id == current_user_id and is_banned is not None:
            raise HTTPException(status_code=400, detail="不能封禁自己")
        
        # 更新手机号
        if phone:
            if not is_valid_phone(phone):
                raise HTTPException(status_code=400, detail="手机号格式有误")
            
            # 检查手机号是否已存在
            existing = db.query(TbUser).filter(TbUser.Phone == phone, TbUser.ID != user_id).first()
            if existing:
                raise HTTPException(status_code=400, detail="手机号已被使用")
            
            user.Phone = phone
        
        # 更新密码
        if password:
            if len(password) < 6 or len(password) > 20:
                raise HTTPException(status_code=400, detail="密码长度必须在6-20位之间")
            user.Password = password
        
        # 更新封禁状态
        if is_banned is not None:
            user.IsBanned = is_banned
        
        try:
            db.commit()
            db.refresh(user)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"更新失败：{str(e)}")
        
        return {
            "code": 200,
            "message": "更新成功",
            "data": {
                "id": user.ID,
                "phone": user.Phone,
                "is_admin": user.IsAdmin,
                "is_banned": user.IsBanned
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新用户失败：{str(e)}")


@user_router.get("/users/{user_id}", summary="获取用户详情（仅管理员）")
async def get_user_detail(
        user_id: int,
        current_user_id: int = Query(..., description="当前管理员ID"),
        db: Session = Depends(get_db)
):
    try:
        # 验证当前用户是否为管理员
        current_user = db.query(TbUser).filter(TbUser.ID == current_user_id).first()
        if not current_user or current_user.IsAdmin != 1:
            raise HTTPException(status_code=403, detail="无权限访问")
        
        user = db.query(TbUser).filter(TbUser.ID == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "id": user.ID,
                "phone": user.Phone,
                "is_admin": user.IsAdmin,
                "is_banned": user.IsBanned,
                "create_time": format_datetime(user.CreateTime)
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户详情失败：{str(e)}")


@user_router.put("/users/{user_id}/ban", summary="封禁/解封用户（仅管理员）")
async def ban_user(
        user_id: int,
        current_user_id: int = Query(..., description="当前管理员ID"),
        is_banned: int = Body(..., description="是否封禁：1-封禁，0-解封"),
        db: Session = Depends(get_db)
):
    try:
        # 验证当前用户是否为管理员
        current_user = db.query(TbUser).filter(TbUser.ID == current_user_id).first()
        if not current_user or current_user.IsAdmin != 1:
            raise HTTPException(status_code=403, detail="无权限访问")
        
        user = db.query(TbUser).filter(TbUser.ID == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 防止管理员封禁自己
        if user_id == current_user_id:
            raise HTTPException(status_code=400, detail="不能封禁自己")
        
        user.IsBanned = is_banned
        
        try:
            db.commit()
            db.refresh(user)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"操作失败：{str(e)}")
        
        action = "封禁" if is_banned == 1 else "解封"
        return {
            "code": 200,
            "message": f"{action}成功",
            "data": {
                "id": user.ID,
                "is_banned": user.IsBanned
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"操作失败：{str(e)}")


@user_router.put("/users/{user_id}/password", summary="修改用户密码")
async def change_password(
        user_id: int,
        current_user_id: int = Query(..., description="当前用户ID"),
        password: str = Body(..., description="新密码"),
        db: Session = Depends(get_db)
):
    try:
        user = db.query(TbUser).filter(TbUser.ID == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        if len(password) < 6 or len(password) > 20:
            raise HTTPException(status_code=400, detail="密码长度必须在6-20位之间")
        
        user.Password = password
        user.UpdateTime = datetime.now()
        
        try:
            db.commit()
            db.refresh(user)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"修改失败：{str(e)}")
        
        return {
            "code": 200,
            "message": "密码修改成功，请重新登录",
            "data": {}
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"修改密码失败：{str(e)}")


def format_datetime(dt):
    """
    安全地格式化 datetime 对象
    """
    if dt is None:
        return "未知"
    
    # 检查是否是无效的日期时间
    if dt.year == 0 or dt.month == 0 or dt.day == 0:
        return "未知"
    
    try:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "未知"


@user_router.get("/user/info", summary="获取当前用户信息")
async def get_current_user_info(
        db: Session = Depends(get_db),
        authorization: str = Header(None)
):
    """
    从 JWT Token 中获取当前用户信息
    """
    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="未授权")
        
        # 提取 token
        if authorization.startswith("Bearer "):
            token = authorization[7:]
        else:
            raise HTTPException(status_code=401, detail="Token 格式错误")
        
        # 这里需要导入 JWT 解码函数
        from core.jwt import decode_token
        payload = decode_token(token)
        
        if not payload:
            raise HTTPException(status_code=401, detail="Token 无效或已过期")
        
        # 修复：JWT 中使用的是 "sub" 字段存储手机号
        phone = payload.get("phone")
        if not phone:
            raise HTTPException(status_code=401, detail="Token 内容无效")
        
        # 查询用户信息
        user = db.query(TbUser).filter(TbUser.Phone == phone).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 格式化时间
        create_time = format_datetime(user.CreateTime)
        update_time = format_datetime(user.UpdateTime)
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "id": user.ID,
                "phone": user.Phone,
                "is_admin": user.IsAdmin,
                "is_banned": user.IsBanned,
                "create_time": create_time,
                "update_time": update_time
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户信息失败：{str(e)}")


@user_router.post("/logout", summary="退出登录")
async def logout():
    """
    退出登录（前端清除 token 即可）
    """
    return {
        "code": 200,
        "message": "退出成功",
        "data": {}
    }
