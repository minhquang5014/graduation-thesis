import torch
import cv2
import random
import time
import pathlib
from ultralytics import YOLO
try:
    import model.utils as utils
except ModuleNotFoundError:
    import utils
import numpy as np
# from modules.autobackend import AutoBackend
import yaml

CONF_THRESHOLD = 0.85
class TensorRTDetection:
    def __init__ (self, video_capture, model_path:str, yaml_path:str):
        self.lower_red = np.array([0, 100, 100])
        self.upper_red = np.array([12, 255, 255])
        self.lower_green = np.array([30, 100, 100])
        self.upper_green = np.array([92, 255, 255])
        self.lower_blue = np.array([95, 120, 120])
        self.upper_blue = np.array([130, 255, 255])

        self.video_capture = video_capture
        self.model_path = model_path
        self.yaml_path = yaml_path
        self.model = YOLO(model_path)
        self.label_map = self.load_class_names_from_yaml()
        self.color = [[random.randint(0, 255) for _ in range(3)] for _ in self.label_map]

    def load_class_names_from_yaml(self):
        with open(self.yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        return data['names']

    def get_detection_result(self, frame):
        # Update object localizer
        results = self.model.predict(frame, imgsz=640, conf=0.5, verbose=False)
        result = results[0].cpu()

        # Get information from result
        box = result.boxes.xyxy.numpy()
        conf = result.boxes.conf.numpy()
        cls = result.boxes.cls.numpy().astype(int)

        return cls, conf, box

    def detection(self, frame):
        start_time = time.time()
        cls, conf, box = self.get_detection_result(frame)

        class_ids = []
        confidence = []
        xyxys = []
        boxes_out = []

        for class_id, conf_score, xyxy in zip(cls, conf, box):
            if conf_score < CONF_THRESHOLD:
                continue
            xyxys.append(xyxy)
            confidence.append(conf_score)
            class_ids.append(class_id)
        
        detection_output = list(zip(class_ids, confidence, xyxys))
        frame = utils.draw_box(frame, detection_output, self.label_map, self.color)

        return frame, start_time, xyxys, class_ids

    def detection_webcam(self):
        cap = cv2.VideoCapture(self.video_capture)
        while cap.isOpened():
            ret, frame = cap.read()
            start_time = time.time()
            cls, conf, box = self.get_detection_result(frame)

            class_ids = []
            confidence = []
            xyxys = []
            boxes_out = []

            for class_id, conf_score, xyxy in zip(cls, conf, box):
                if conf_score < CONF_THRESHOLD:
                    continue
                xyxys.append(xyxy)
                confidence.append(conf_score)
                class_ids.append(class_id)
            
            detection_output = list(zip(class_ids, confidence, xyxys))
            frame = utils.draw_box(frame, detection_output, self.label_map, self.color)

            # Draw boxes and prepare for ROI processing
            for bbox, conf_score, class_id in zip(xyxys, confidence, class_ids):
                x1, y1, x2, y2 = bbox.astype(int)
                boxes_out.append(((x1, y1, x2, y2), class_id))

                if class_id == 0:
                    continue  # Skip if class_id is 0

                w1, h1 = x2 - x1, y2 - y1
                ROI = frame[y1:y2, x1:x2]
                hsv_roi = cv2.cvtColor(ROI, cv2.COLOR_BGR2HSV)

                # Apply color masks
                masked_red = cv2.inRange(hsv_roi, self.lower_red, self.upper_red)
                masked_blue = cv2.inRange(hsv_roi, self.lower_blue, self.upper_blue)
                masked_green = cv2.inRange(hsv_roi, self.lower_green, self.upper_green)

                # Find contours and annotate
                for mask, color_name, color_bgr in [
                    (masked_red, "red", (0, 0, 255)),
                    (masked_blue, "blue", (255, 0, 0)),
                    (masked_green, "green", (0, 255, 0))
                ]:
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    for contour in contours:
                        if cv2.contourArea(contour) > 0.25 * w1 * h1:
                            x, y, w, h = cv2.boundingRect(contour)
                            cv2.rectangle(frame, (x + x1, y + y1), (x + x1 + w, y + y1 + h), (76, 153, 0), 3)
                            cv2.putText(frame, color_name, (x + x1, y + y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_bgr, 2)

            end_time = time.time()
            if (end_time - start_time) > 0:
                fps = 1 / (end_time - start_time)

            image_output = utils.draw_fps(fps, frame)
            cv2.imshow("YOLOv8 Webcam Detection", image_output)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    tensorRT = TensorRTDetection(video_capture=2, model_path = "model/custom_train_yolov10s_3.engine", yaml_path="model/data.yaml")
    tensorRT.detection_webcam()