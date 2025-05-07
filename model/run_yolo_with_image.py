import numpy as np
import cv2
from ultralytics import YOLO
import torch

# Load YOLOv10s model
model = YOLO("model/yolov10s.pt")

# Choose device
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)

# Read image
img = cv2.imread("images/photo_0605_10h20m53s.jpg")

# Inference (img is a NumPy array, which is fine)
results = model(img)

# Show image
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Print results
print(results)
