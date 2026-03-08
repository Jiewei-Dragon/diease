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
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 确保目录存在，避免报错
if os.path.exists(model_dir):
    sys.path.append(model_dir)
else:
    raise FileNotFoundError(f"找不到 effiientNet 模块所在目录：{model_dir}")

def classifyAndHeat_from_image(image_path: str):
    try:
        # 1. 图片预处理
        img_original = Image.open(image_path).convert('RGB')
        transforms = torchvision.transforms.Compose([
            torchvision.transforms.Resize(256),
            torchvision.transforms.CenterCrop(224),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        img_tensor = transforms(img_original).to(device)
        input_tensor = torch.unsqueeze(img_tensor, dim=0)  # (1, 3, 224, 224)

        img_vis = img_original.resize((256, 256))  # PIL图片的resize
        width, height = img_vis.size  # PIL图片的size
        left = (width - 224) // 2
        top = (height - 224) // 2
        img_vis_cropped = img_vis.crop((left, top, left + 224, top + 224))  # PIL图片的crop
        img_vis_np = np.array(img_vis_cropped, dtype=np.uint8)  # 转为numpy数组



        # 2. 模型加载
        model = torch.load(model_pth_path, map_location='cuda', weights_only=False)
        model = model.to('cuda')  # 确保模型在GPU上
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

