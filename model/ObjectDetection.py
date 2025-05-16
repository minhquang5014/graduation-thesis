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
    def predict(self):
        return self.model(self.frame)
    
    def plot_boxes(self, results):
        xyxys = []
        confidence = []
        class_ids = []

        for result in results[0]:
            class_id = result.boxes.cls.cpu().numpy().astype(int)
            if class_id == 0:
                # get the coordinate
                xyxys.append(result.boxes.xyxy.cpu().numpy())

                # get the confidence score
                confidence.append(result.boxes.conf.cpu().numpy())

                class_ids.append(result.boxes.cls.cpu().numpy().astype(int))
                
        detections = Detections(
                xyxy=results[0].boxes.xyxy.cpu().numpy(),
                confidence=results[0].boxes.conf.cpu().numpy(),
                class_id=results[0].boxes.cls.cpu().numpy().astype(int)
        )
        for bbox, confidence, class_id in zip(detections.xyxy, detections.confidence, detections.class_id):
            # if confidence 
            self.labels = [f"{self.CLASS_NAMES_DICT[class_id]}"]
            
            #crappu code by the way
            x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
            
            # print(x1, y1, x2, y2)
            cv2.rectangle(self.frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 255), 2)

            # frame = self.box_annotator.annotate(scene = frame, detections=detections)
            cv2.putText(self.frame, f"{self.labels[0]}, conf: {confidence:0.2f}", (int(x1), int(y1-20)),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return self.frame
    def __call__(self):
        start_time = time()
        results = self.predict(self.frame)
        self.frame = self.plot_boxes(results)
        end_time = time()

        if start_time - end_time != 0:
            fps = 1/np.round(end_time - start_time, 2)
        cv2.putText(self.frame, f'FPS: {int(fps)}', (500, 20), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
        return self.frame
    