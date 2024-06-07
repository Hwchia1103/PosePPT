import torch
from ultralytics import YOLO

# 检查CUDA是否可用
use_cuda = torch.cuda.is_available()
print("CUDA is available:", use_cuda)

# 加载YOLOv8模型
model = YOLO('yolov8n.pt')

# 使用GPU进行检测，如果CUDA可用
device = 'cuda' if use_cuda else 'cpu'
print(f"Using device: {device}")

# 进行摄像头检测
model.predict(source=0, device=device, show=True)
