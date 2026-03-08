from fastapi import FastAPI, UploadFile, File, HTTPException, Query, APIRouter
from fastapi.responses import JSONResponse
import torch
import tempfile
import os
import uuid
from config import *
from handle.classify import classifyAndHeat_from_image

model_router = APIRouter(prefix="/api", tags=["模型相关接口"])


@model_router.post("/heatmap/generate", summary="图片病害分类识别")
async def classify(
        # 核心必选参数：前端上传的图片文件
        image: UploadFile = File(..., description="上传的病害图片（支持JPG/PNG/JPEG，≤10MB）"),
        # 可选参数：是否返回置信度
        return_confidence: bool = Query(True, description="是否返回置信度，默认True")
):
    # 初始化临时文件路径（避免异常时变量未定义）
    temp_file_path = None
    try:
        # 1. 验证文件类型和大小
        valid_types = ["image/jpeg", "image/jpg", "image/png"]
        max_size = 10 * 1024 * 1024  # 10MB

        # 修复：处理 image.size 为 None 的情况
        if image.content_type not in valid_types:
            raise HTTPException(status_code=400, detail="仅支持JPG/PNG/JPEG格式的图片")
        if image.size and image.size > max_size:
            raise HTTPException(status_code=400, detail="图片大小不能超过10MB")

        # 2. 创建临时文件（适配你的 image_path 入参）
        temp_filename = f"{uuid.uuid4()}.jpg"
        temp_file_path = os.path.join(tempfile.gettempdir(), temp_filename)

        # 保存上传的图片到临时文件
        with open(temp_file_path, "wb") as f:
            f.write(await image.read())

        # 3. 调用模型分类函数（现在返回字典）
        result = classifyAndHeat_from_image(temp_file_path)

        # 4. 清理临时文件（避免磁盘占用）
        os.unlink(temp_file_path)

        # 5. 构造响应（对齐前端需求）
        response_data = {
            "code": 200,
            "message": "分类并生成热力图成功",
            "data": {
                "id": str(uuid.uuid4()),  # 唯一请求ID
                "disease_type": result["disease_type"],
                "disease_name": DISEASE_CLASSES[result["disease_type"]],
                "heatmapImage": result["heatmap_url"],
                "GPU": str(torch.cuda.get_device_properties(0).name) if torch.cuda.is_available() else "CPU"
            }
        }

        # 根据可选参数决定是否返回置信度
        if return_confidence:
            response_data["data"]["confidence"] = result["confidence"]
            response_data["data"]["all_predictions"] = result["all_predictions"]

        return JSONResponse(response_data)

    except HTTPException:
        raise  # 主动抛出的验证错误，直接返回
    except Exception as e:
        # 异常时清理临时文件（关键：避免文件残留）
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        raise HTTPException(
            status_code=500,
            detail=f"接口函数异常：{str(e)}",
            headers={"X-Error": "ModelInferenceError"}
        )
