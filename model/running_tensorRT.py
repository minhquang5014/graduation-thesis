import torch
import cv2
import random
import time
import pathlib
from ultralytics import YOLO
import model.utils as utils
import numpy as np
# from modules.autobackend import AutoBackend
import yaml

CONF_THRESHOLD = 0.6
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

        # class_ids = []
        # confidence = []
        # xyxys = []
        # for class_id, conf, xyxy in zip(cls, conf, box):
        #     if conf < CONF_THRESHOLD:
        #         continue
        #     xyxys.append(xyxy)
        #     confidence.append(conf)
        #     class_ids.append(class_id)
        # boxes_out = []
        # for bbox, conf, class_id in zip(xyxys, confidence, class_ids):
        #     x1, y1, x2, y2 = bbox.astype(int)
        #     label = self.CLASS_NAMES_DICT.get(class_id, str(class_id))

        #     # Draw rectangle
        #     cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 255), 2)

        #     # Draw label with confidence
        #     cv2.putText(frame, f"{label}, conf: {conf:.2f}", (int(x1), int(y1) - 10),
        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        #     boxes_out.append(((x1, y1, x2, y2), class_id))
        # return frame, boxes_out

    def detection(self, frame):
        frame_count = 0
        total_fps = 0
        start = time.time()
        cls, conf, box = self.get_detection_result(frame)
        class_ids = []
        confidence = []
        xyxys = []
        for class_id, conf, xyxy in zip(cls, conf, box):
            if conf < CONF_THRESHOLD:
                continue
            xyxys.append(xyxy)
            confidence.append(conf)
            class_ids.append(class_id)

        
        detection_output = list(zip(class_ids, confidence, xyxys))
        frame = utils.draw_box(frame, detection_output, self.label_map, self.color)

        end = time.time()
        if (end - start) != 0:
            fps = 1 / (end - start)
        # total_fps += fps
        # frame_count += 1
        # avg_fps = total_fps / frame_count

        return frame, fps

    def detection_webcam(self):
        self.model = YOLO(self.model_path)
        label_map = self.load_class_names_from_yaml()
        COLORS = [[random.randint(0, 255) for _ in range(3)] for _ in label_map]

        cap = cv2.VideoCapture(self.video_capture)  # 0 = default webcam

        frame_count = 0
        total_fps = 0

        while True:
            ret, self.frame = cap.read()
            if not ret:
                break
            self.frame = cv2.flip(self.frame, 1)
            start = time.time()
            cls, conf, box = self.get_detection_result()
            class_ids = []
            confidence = []
            xyxys = []
            for class_id, conf, xyxy in zip(cls, conf, box):
                if conf < CONF_THRESHOLD:
                    continue
                xyxys.append(xyxy)
                confidence.append(conf)
                class_ids.append(class_id)
            detection_output = list(zip(class_ids, confidence, xyxys))
            self.frame = utils.draw_box(self.frame, detection_output, label_map, COLORS)

            end = time.time()
            if (end - start) != 0:
                fps = 1 / (end - start)
                print(fps)
            total_fps += fps
            frame_count += 1
            avg_fps = total_fps / frame_count

            cv2.putText(self.frame, f'FPS: {int(fps)}', (500, 20), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)

            return self.frame

        #     image_output = utils.draw_fps(avg_fps, image_output)

        #     cv2.imshow("YOLOv8 Webcam Detection", image_output)

        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break

        # cap.release()
        # cv2.destroyAllWindows()

# tensorRT = TensorRTDetection(video_capture="video/1.avi", model_path = "model/custom_train_yolov10s_3.engine", yaml_path="model/data.yaml")
# tensorRT.detection_webcam()