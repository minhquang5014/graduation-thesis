import numpy as np
import cv2
import torch
from ultralytics import YOLO

from supervision.draw.color import ColorPalette, Color
from supervision import Detections, BoxAnnotator

colors=[Color(r=255, g=64, b=64), Color(r=255, g=161, b=160)]

# Load YOLO model
model = YOLO("model/custom_train_yolov10s.pt")

# Auto device selection
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using {device} for running YOLO inference")

# Load image
# img = cv2.imread("images/photo_0605_10h20m53s.jpg")

# # Run inference
# results = model(img)[0]  # get first (and only) result

# # Convert YOLO results to Supervision Detections
# detections = Detections.from_ultralytics(results)

# # Create annotator
# box_annotator = BoxAnnotator(color=ColorPalette(colors=colors), thickness=3)

# # Annotate image
# annotated_img = box_annotator.annotate(scene=img.copy(), detections=detections)

# # Display result
# cv2.imshow("Object Detection", annotated_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

model.to(device)
print(model.predict())