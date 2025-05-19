import torch
import numpy as np
from ultralytics import YOLO
from time import time
from supervision.draw.color import ColorPalette, Color
from supervision import Detections, BoxAnnotator
import cv2
colors=[Color(r=255, g=64, b=64), Color(r=255, g=161, b=160)]


class ObjectDetection:
    def __init__(self, frame, model):
        self.device = 'cuda' if torch.cuda.is_available() else "cpu"
        self.frame = frame
        self.model = YOLO(model)
        self.model.fuse()
        self.model.to(self.device)
        self.CLASS_NAMES_DICT = self.model.model.names
        self.box_annotator = BoxAnnotator(color=ColorPalette(colors=colors), thickness=3)
    # def predict(self):
    #     return self.model(self.frame)
    
    def plot_boxes(self, results, conf_threshold = 0.5):
        xyxys =[]
        confidence = []
        class_ids = []

        boxes = results[0].boxes
        class_array = boxes.cls.cpu().numpy().astype(int)
        conf_array = boxes.conf.cpu().numpy()
        xyxy_array = boxes.xyxy.cpu().numpy()

        for class_id, conf, xyxy in zip(class_array, conf_array, xyxy_array):
            if conf < conf_threshold:
                continue
            xyxys.append(xyxy)
            confidence.append(conf)
            class_ids.append(class_id)

        for bbox, conf, class_id in zip(xyxys, confidence, class_ids):
            x1, y1, x2, y2 = bbox
            label = self.CLASS_NAMES_DICT.get(class_id, str(class_id))

            # Draw rectangle
            cv2.rectangle(self.frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 255), 2)

            # Draw label with confidence
            cv2.putText(self.frame, f"{label}, conf: {conf:.2f}", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        return self.frame
    
    def __call__(self):
        start_time = time()
        results = self.model(self.frame)
        self.frame = self.plot_boxes(results)
        end_time = time()

        if start_time - end_time != 0:
            fps = 1/np.round(end_time - start_time, 2)
        cv2.putText(self.frame, f'FPS: {int(fps)}', (500, 20), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
        return self.frame
    