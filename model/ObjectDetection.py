import torch
import numpy as np
from ultralytics import YOLO
from time import time
from supervision.draw.color import ColorPalette, Color
from supervision import Detections, BoxAnnotator
import cv2
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
    # def predict(self):
    #     return self.model(self.frame)
    
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
            class_ids. append(class_id)
        # if len(boxes) != 0:
        #     for (x1, y1, x2, y2), class_id in boxes:
        #         if class_id == 0:
        #             continue
        #         w1 = x2 - x1
        #         h1 = y2 - y1
        #         ROI = frame[y1:y2, x1:x2]

        #         # convert the ROI to HSV color format
        #         hsv_roi = cv2.cvtColor(ROI, cv2.COLOR_BGR2HSV)

        #         masked_red = cv2.inRange(hsv_roi, self.lower_red, self.upper_red)
        #         masked_blue = cv2.inRange(hsv_roi, self.lower_blue, self.upper_blue)
        #         masked_green = cv2.inRange(hsv_roi, self.lower_green, self.upper_green)

        #         contours_red, _ = cv2.findContours(masked_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #         contours_blue, _ = cv2.findContours(masked_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #         contours_green, _ = cv2.findContours(masked_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
        #         for contour in contours_red:
        #             if cv2.contourArea(contour) > 1/4 * w1 * h1:
        #                 x, y, w, h = cv2.boundingRect(contour)
        #                 cv2.rectangle(frame, (x + x1, y + y1), (x + x1 + w, y + y1 + h), (76, 153, 0), 3)  # Draw rectangle
        #                 cv2.putText(frame, "red", (x + x1, y + y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        #         for contour in contours_blue:
        #             if cv2.contourArea(contour) > 1/4 * w1 * h1:
        #                 x, y, w, h = cv2.boundingRect(contour)
        #                 cv2.rectangle(frame, (x + x1, y + y1), (x + x1 + w, y + y1 + h), (76, 153, 0), 3)  # Draw rectangle
        #                 cv2.putText(frame, "blue", (x + x1, y + y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        #         for contour in contours_green:
        #             if cv2.contourArea(contour) > 1/4 * w1 * h1:
        #                 x, y, w, h = cv2.boundingRect(contour)
        #                 cv2.rectangle(frame, (x + x1, y + y1), (x + x1 + w, y + y1 + h), (76, 153, 0), 3)  # Draw rectangle
        #                 cv2.putText(frame, "green", (x + x1, y + y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # end_time = time()

        # if start_time - end_time != 0:
        #     fps = 1/np.round(end_time - start_time, 2)
        # cv2.putText(frame, f'FPS: {int(fps)}', (500, 20), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
        return frame, xyxys, class_ids

    def video(self):
        cap = cv2.VideoCapture(2)
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

    detector.video()