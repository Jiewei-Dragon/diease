import base64
import os
import sys
import uuid
from io import BytesIO

import torch
import torchvision.transforms
from PIL import Image
from config import *
from resource import *
from PIL import Image
import matplotlib.pyplot as plt
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam import *
import numpy as np

# 确定推理设备
if INFERENCE_DEVICE == "auto":
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
else:
    device = torch.device(INFERENCE_DEVICE)

# 确保目录存在，避免报错
if os.path.exists(MODEL_DIR):
    sys.path.append(MODEL_DIR)
else:
    raise FileNotFoundError(f"找不到模型权重文件所在目录：{MODEL_DIR}")

def classifyAndHeat_from_image(image_path: str):
    try:
        # 1. 图片预处理
        img_original = Image.open(image_path).convert('RGB')
        transforms = torchvision.transforms.Compose([
            torchvision.transforms.Resize(IMAGE_SIZE_RESIZE),
            torchvision.transforms.CenterCrop(IMAGE_SIZE_CROP),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize(IMAGE_NORMALIZE_MEAN, IMAGE_NORMALIZE_STD)
        ])
        img_tensor = transforms(img_original).to(device)
        input_tensor = torch.unsqueeze(img_tensor, dim=0)

        img_vis = img_original.resize((IMAGE_SIZE_RESIZE, IMAGE_SIZE_RESIZE))
        width, height = img_vis.size
        left = (width - IMAGE_SIZE_CROP) // 2
        top = (height - IMAGE_SIZE_CROP) // 2
        img_vis_cropped = img_vis.crop((left, top, left + IMAGE_SIZE_CROP, top + IMAGE_SIZE_CROP))
        img_vis_np = np.array(img_vis_cropped, dtype=np.uint8)



        # 2. 模型加载
        model = torch.load(MODEL_PTH_PATH, map_location=device, weights_only=False)
        model = model.to(device)
        # 设置目标层
        target_layers = [model.features[-1]]

        # 3. 图像分类
        model.eval()
        with torch.no_grad():
            output = model(input_tensor)

        # 4. 解析结果（返回字典，适配接口解析逻辑）
        pred_idx = output.argmax().cpu().item()  # 预测类别索引（整数）
        disease_name = DISEASE_CLASSES[pred_idx]  # 预测类别名称

        # 5. 生成热力图
        with torch.no_grad():
            outputs = model(input_tensor)
            _, predicted = torch.max(outputs.data, 1)
            target_category = predicted.item()
        cam = GradCAM(model=model, target_layers=target_layers)
        grayscale_cam = cam(input_tensor=input_tensor)
        grayscale_cam = grayscale_cam[0, :]
        # 4.3 合并热力图到原图
        visualization = show_cam_on_image(
            img_vis_np.astype(np.float32) / 255.,
            grayscale_cam,
            use_rgb=True,
            image_weight=0.6  # 原图权重，平衡热力图显示效果
        )

        # 5.1 将numpy数组转为PIL图片
        heatmap_img = Image.fromarray(visualization)
        # 5.2 写入BytesIO（内存中）
        buffer = BytesIO()
        heatmap_img.save(buffer, format='PNG', quality=90)
        # 5.3 编码为Base64字符串
        heatmap_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        # 5.4 构造前端可直接展示的URL
        heatmap_url = f"data:image/png;base64,{heatmap_base64}"

        # 计算置信度（softmax归一化）
        confidence = torch.softmax(output, dim=1)[0][pred_idx].cpu().item()

        # 计算所有类别的置信度（可选）
        all_predictions = {
            DISEASE_CLASSES[i]: round(torch.softmax(output, dim=1)[0][i].cpu().item(), 4)
            for i in range(len(DISEASE_CLASSES))
        }

        # 关键修改：返回字典而非字符串
        return {
            "disease_type": pred_idx,
            "disease_name": disease_name,
            "confidence": round(confidence, 4),
            "all_predictions": all_predictions,
            "heatmap_url": heatmap_url
        }
    except Exception as e:
        raise Exception(f"模型推理或热力图核心函数异常：{str(e)}")

