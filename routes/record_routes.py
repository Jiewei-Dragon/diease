import json
import base64
import os
import uuid
from datetime import datetime

from fastapi.params import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter, Body, Query

from core.db import get_db
from models.record import TbRecord
from schemas.record import RecordAddRequest
from config import UPLOAD_DIR, ORIGIN_IMAGE_DIR, HEATMAP_IMAGE_DIR, BASE_DIR

record_router = APIRouter(prefix="/api", tags=["记录相关接口"])

# 确保目录存在
os.makedirs(ORIGIN_IMAGE_DIR, exist_ok=True)
os.makedirs(HEATMAP_IMAGE_DIR, exist_ok=True)


def save_base64_image(base64_string: str, save_dir: str, filename: str = None) -> str:
    """
    将Base64图片保存到服务器
    :param base64_string: Base64字符串（可能包含data:image/png;base64,前缀）
    :param save_dir: 保存目录
    :param filename: 文件名（可选，不传则自动生成）
    :return: 相对路径
    """
    # 移除Base64前缀（如果有）
    if ',' in base64_string:
        base64_string = base64_string.split(',', 1)[1]
    
    # 解码Base64
    image_data = base64.b64decode(base64_string)
    
    # 生成文件名
    if not filename:
        filename = f"{uuid.uuid4()}.png"
    
    # 完整路径
    filepath = os.path.join(save_dir, filename)
    
    # 保存文件
    with open(filepath, 'wb') as f:
        f.write(image_data)
    
    # 返回相对路径（用于数据库存储和前端访问）
    return f"/uploads/{os.path.basename(save_dir)}/{filename}"


@record_router.post("/record/add", summary="保存识别记录")
async def record_add(
        request_data: RecordAddRequest = Body(...),
        db: Session = Depends(get_db)
):
    try:
        # 1. 保存原图
        origin_filename = f"origin_{uuid.uuid4()}.png"
        origin_path = save_base64_image(request_data.origin_image, ORIGIN_IMAGE_DIR, origin_filename)
        
        # 2. 保存热力图
        heatmap_filename = f"heatmap_{uuid.uuid4()}.png"
        heatmap_path = save_base64_image(request_data.heatmap_image, HEATMAP_IMAGE_DIR, heatmap_filename)
        
        # 3. 创建记录
        new_record = TbRecord(
            UserId=request_data.user_id,
            OriginMapUrl=origin_path,
            HeatmapUrl=heatmap_path,
            Confidence=request_data.confidence,
            DieaseType=request_data.disease_type,
            DieaseName=request_data.disease_name,
            CreateTime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # 4. 保存到数据库
        try:
            db.add(new_record)
            db.commit()
            db.refresh(new_record)
        except Exception as e:
            db.rollback()
            # 删除已保存的图片（回滚）
            for path in [origin_path, heatmap_path]:
                full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), path.lstrip('/'))
                if os.path.exists(full_path):
                    os.remove(full_path)
            raise HTTPException(status_code=500, detail=f"保存记录失败：{str(e)}")
        
        # 5. 返回成功响应
        return {
            "code": 200,
            "message": "记录保存成功",
            "data": {
                "record_id": new_record.id,
                "user_id": new_record.UserId,
                "origin_url": origin_path,
                "heatmap_url": heatmap_path,
                "create_time": new_record.CreateTime
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"保存失败：{str(e)}"
        )


@record_router.get("/records/statistics", summary="获取用户统计数据")
async def get_statistics(
        user_id: int = Query(..., description="用户ID"),
        db: Session = Depends(get_db)
):
    try:
        from sqlalchemy import func
        from datetime import date
        
        today = date.today().strftime("%Y-%m-%d")
        
        # 总记录数
        total_count = db.query(func.count(TbRecord.id))\
            .filter(TbRecord.UserId == user_id)\
            .scalar()
        
        # 今日记录数
        today_count = db.query(func.count(TbRecord.id))\
            .filter(
                TbRecord.UserId == user_id,
                TbRecord.CreateTime.like(f"{today}%")
            )\
            .scalar()
        
        # 最近识别时间
        latest_record = db.query(TbRecord)\
            .filter(TbRecord.UserId == user_id)\
            .order_by(TbRecord.id.desc())\
            .first()
        
        latest_time = latest_record.CreateTime if latest_record else None
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "total_count": total_count,
                "today_count": today_count,
                "latest_time": latest_time
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取统计数据失败：{str(e)}"
        )


@record_router.get("/records", summary="获取用户识别记录列表")
async def get_records(
        user_id: int = Query(..., description="用户ID"),
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(10, ge=1, le=100, description="每页数量"),
        db: Session = Depends(get_db)
):
    try:
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 查询总数
        total = db.query(TbRecord).filter(TbRecord.UserId == user_id).count()
        
        # 分页查询（按时间倒序）
        records = db.query(TbRecord)\
            .filter(TbRecord.UserId == user_id)\
            .order_by(TbRecord.id.desc())\
            .offset(offset)\
            .limit(page_size)\
            .all()
        
        # 格式化数据
        record_list = []
        for record in records:
            record_list.append({
                "id": record.id,
                "user_id": record.UserId,
                "origin_map_url": record.OriginMapUrl,
                "heatmap_url": record.HeatmapUrl,
                "confidence": record.Confidence,
                "disease_type": record.DieaseType,
                "disease_name": record.DieaseName,
                "create_time": record.CreateTime
            })
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "list": record_list,
                "total": total,
                "page": page,
                "page_size": page_size
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取记录失败：{str(e)}"
        )


@record_router.get("/records/{record_id}", summary="获取单条记录详情")
async def get_record_detail(
        record_id: int,
        user_id: int = Query(..., description="用户ID"),
        db: Session = Depends(get_db)
):
    try:
        # 查询记录（确保只能查看自己的记录）
        record = db.query(TbRecord)\
            .filter(TbRecord.id == record_id, TbRecord.UserId == user_id)\
            .first()
        
        if not record:
            raise HTTPException(status_code=404, detail="记录不存在或无权访问")
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": {
                "id": record.id,
                "user_id": record.UserId,
                "origin_map_url": record.OriginMapUrl,
                "heatmap_url": record.HeatmapUrl,
                "confidence": record.Confidence,
                "disease_type": record.DieaseType,
                "disease_name": record.DieaseName,
                "create_time": record.CreateTime
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取详情失败：{str(e)}"
        )


@record_router.delete("/records/{record_id}", summary="删除识别记录")
async def delete_record(
        record_id: int,
        user_id: int = Query(..., description="用户ID"),
        db: Session = Depends(get_db)
):
    try:
        # 查询记录
        record = db.query(TbRecord)\
            .filter(TbRecord.id == record_id, TbRecord.UserId == user_id)\
            .first()
        
        if not record:
            raise HTTPException(status_code=404, detail="记录不存在或无权删除")
        
        # 删除图片文件
        for image_path in [record.OriginMapUrl, record.HeatmapUrl]:
            if image_path:
                full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), image_path.lstrip('/'))
                if os.path.exists(full_path):
                    os.remove(full_path)
        
        # 删除数据库记录
        db.delete(record)
        db.commit()
        
        return {
            "code": 200,
            "message": "删除成功",
            "data": {}
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"删除失败：{str(e)}"
        )
