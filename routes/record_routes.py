import json
from datetime import datetime

from fastapi.params import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter, Body

from core.db import get_db
from models.record import TbRecord
from schemas.record import RecordAddRequest

record_router = APIRouter(prefix="/api", tags=["记录相关接口"])


@record_router.post("/record/add", summary="图片病害分类识别")
async def record_add(
        request_data: RecordAddRequest = Body(...),  # 自动校验前端传入的参数
        db: Session = Depends(get_db)
):
    try:
        # 1. 校验预测结果JSON格式（可选，增强鲁棒性）
        try:
            json.loads(request_data.all_predictions)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="all_predictions格式错误，需为JSON字符串")

        # 2. 保存到数据库
        new_record = TbRecord(
            HeatmapUrl=request_data.heatmap_image,
            Confidence=request_data.confidence,
            DieaseType=request_data.disease_type,
            DieaseName=request_data.disease_name,
            CreateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        # 3. 数据库操作（异常提示修正为“保存记录”）
        try:
            db.add(new_record)
            db.commit()
            db.refresh(new_record)  # 刷新后可获取数据库生成的自增ID
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"保存记录失败，请稍后重试：{str(e)}")

        # 4. 返回成功响应（返回自增ID）
        return {
            "code": 200,
            "message": "记录保存成功",
            "data": {
                "record_id": new_record.id,  # 数据库生成的自增ID
                "create_time": new_record.CreateTime.strftime("%Y-%m-%d %H:%M:%S")
            }
        }

    except HTTPException:
        raise  # 主动抛出的异常直接返回
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="保存失败，服务器内部错误"  # 生产环境隐藏具体异常
        )