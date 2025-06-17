import torch
import numpy as np
from ultralytics import YOLO
from time import time
from supervision.draw.color import ColorPalette, Color
from supervision import Detections, BoxAnnotator
import cv2
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from PLC.plc_connection import PLCConnection
    print(f"import PLC module successfully")
except Exception as e:
    print(f"import errro: {e}")

colors=[Color(r=255, g=64, b=64), Color(r=255, g=161, b=160)]

class ObjectDetection:
    def __init__(self, model):
        self.lower_red = np.array([0, 100, 100])
        self.upper_red = np.array([12, 255, 255])
        self.lower_green = np.array([30, 100, 100])
        self.upper_green = np.array([92, 255, 255])
        self.lower_blue = np.array([95, 120, 120])
        self.upper_blue = np.array([130, 255, 255])

        self.device = 'cuda' if torch.cuda.is_available() else "cpu"
        self.model = YOLO(model)
        self.model.fuse()
        self.model.to(self.device)
        self.CLASS_NAMES_DICT = self.model.model.names
        self.box_annotator = BoxAnnotator(color=ColorPalette(colors=colors), thickness=3)
        self.plc_connection_status = False
    def connect_plc(self):
        self.call_out_PLC_object = PLCConnection()  # no need to specify the ip address and port, let's just put the default value there
        self.plc_connection_status = self.call_out_PLC_object.connectPLC()
        return self.plc_connection_status
    def plot_boxes(self, results, frame, conf_threshold = 0.8):
        xyxys = []
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
        boxes_out = []
        for bbox, conf, class_id in zip(xyxys, confidence, class_ids):
            x1, y1, x2, y2 = bbox.astype(int)
            label = self.CLASS_NAMES_DICT.get(class_id, str(class_id))

            # Draw rectangle
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 255), 2)

            # Draw label with confidence
            cv2.putText(frame, f"{label}, conf: {conf:.2f}", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            boxes_out.append(((x1, y1, x2, y2), class_id))
        return frame, boxes_out
    
    def webcam(self, frame):
        results = self.model(frame)
        frame, boxes = self.plot_boxes(results, frame)
        xyxys = []
        class_ids = []
        for ((x1, y1, x2, y2), class_id) in boxes:
            xyxys.append((x1, y1, x2, y2))
            class_ids.append(class_id)
        
        return frame, xyxys, class_ids

    def video(self):
        cap = cv2.VideoCapture(2)
        last_update_time = time()
        update_interval = 0.4
        assert cap.isOpened()
        fps = 0
        # set the resolution for the frame
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while True:
            start_time = time()
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            if not ret:
                break
            results = self.model(frame)
            frame, boxes_out = self.plot_boxes(results, frame)
            register_state = [0, 0, 0, 0]
            for ((x1, y1, x2, y2), class_id) in boxes_out:
                if class_id == 0:
                    register_state[3] = 1
                elif class_id == 4:
                    register_state[0] = 1
                elif class_id == 3:
                    register_state[1] = 1
                elif class_id == 2:
                    register_state[2] = 1
                else:
                    continue
            if time() - last_update_time >= update_interval:
                for i in range(4):
                    self.call_out_PLC_object.write(i, register_state[i]) if self.plc_connection_status != False else print("Cannot send signal to PLC")
                last_update_time = time()

            end_time = time()
            if end_time - start_time != 0:
                fps = 1/np.round(end_time - start_time, 2)
            # print(fps)
            cv2.putText(frame, f'FPS: {int(fps)}', (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            cv2.imshow('YOLOv8 Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        
        cap.release()
        cv2.destroyAllWindows()
if __name__ == '__main__':
    # detector = ObjectDetection(capture_index=0)
    detector = ObjectDetection(model = "model/training_with_6classes.pt")
    connect_plc = detector.connect_plc()
    detector.video()