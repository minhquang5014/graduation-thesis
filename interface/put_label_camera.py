import tkinter as tk
import cv2
from PIL import Image, ImageTk
from time import time
import datetime
import numpy as np

# from model.running_tensorRT import TensorRTDetection
# tensorRT = TensorRTDetection(video_capture = 2, model_path = "model/custom_train_yolov10s_4.engine", yaml_path="model/data.yaml")
register_state = [0, 0, 0, 0]
from model.ObjectDetection import ObjectDetection
detection = ObjectDetection("model/training_with_6classes.pt")

def label_to_put_video(frame, screen_width, screen_height, fixed_video_label=False, label_width=None, label_height=None):
    if fixed_video_label:
        label_width = 640
        label_height = 480
    else:
        label_width = screen_width / 1.953
        label_height = screen_height / 1.354
    video_label = tk.Label(frame, bg="black")
    video_label.place(x=0, y=0, relwidth=label_width/screen_width, relheight=label_height/screen_height)
    return video_label, label_width, label_height

def update_frame_hsv(capture:cv2.VideoCapture, video_label:label_to_put_video, 
                 root:tk.Tk, resized_width, resized_height, last_update_time, update_interval, write=None, read = None,enable_detection = False):
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([12, 255, 255])
    lower_green = np.array([30, 100, 100])
    upper_green = np.array([90, 255, 255])
    lower_blue = np.array([95, 120, 120])
    upper_blue = np.array([120, 255, 255])
    ret, frame = capture.read()
    fps = 0
    start_time = time()
    # write(0, 0)
    # write(1, 0)
    # write(2, 0)
    # write(3, 0)
    if ret:
        frame = cv2.flip(frame, 1)
            # instead of loading .pt model, we'll load the .engine file
            # from model.ObjectDetection import ObjectDetection
        # frame, fps = detection.__call__(frame)

        # frame, xyxys, class_ids = tensorRT.detection(frame)
        frame, xyxys, class_ids = detection.__call__(frame)
        for bbox, class_id in zip(xyxys, class_ids):
            x1, y1, x2, y2 = bbox
            if class_id == 0:
                # write holding register to address number 3, value 1
                # write(3, 1) if write is not None else print("Cannot send signal to address 3, value 1")
                register_state[3] = 1  
                break
        
            w1, h1 = x2 - x1, y2 - y1
            ROI = frame[y1:y2, x1:x2]
            hsv_roi = cv2.cvtColor(ROI, cv2.COLOR_BGR2HSV)

            # Apply color masks
            masked_red = cv2.inRange(hsv_roi, lower_red, upper_red)
            masked_blue = cv2.inRange(hsv_roi, lower_blue, upper_blue)
            masked_green = cv2.inRange(hsv_roi, lower_green, upper_green)

            # Find contours and annotate
            for mask, color_name, color_bgr, address in [
                (masked_red, "red", (0, 0, 255), 0),
                (masked_green, "green", (0, 255, 0), 1),
                (masked_blue, "blue", (255, 0, 0), 2),
            ]:
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    if cv2.contourArea(contour) > 0.25 * w1 * h1:
                        x, y, w, h = cv2.boundingRect(contour)
                        cv2.rectangle(frame, (x + x1, y + y1), (x + x1 + w, y + y1 + h), (76, 153, 0), 3)
                        cv2.putText(frame, color_name, (x + x1, y + y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_bgr, 2)
                        # write(address, 1) if write is not None else print(f"Cannot send signal to {address}")
                        register_state[address] = 0
                        # write(address, 1)
                        break
        if time() - last_update_time >= update_interval:
            for i in range(4):
                write(i, register_state[i]) if write is not None else print(f"Cannot write to address {register_state[i]}, value {i}")
            last_update_time = time()

        end_time = time()

        # red_value = read(34)
        # green_value = read(35)
        # blue_value = read(36)
        # NG_value = read(37)

        # process if any value is enabled to 1, take the photo, save it in the working dir, name it with detection type, and 

        if (end_time - start_time) > 0:
            fps = 1 / (end_time - start_time)

        frame = cv2.resize(frame, (int(resized_width), int(resized_height)))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        current_date = datetime.date.today()
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        cv2.putText(frame, f"{current_date} {current_time}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, f'FPS: {int(fps)}', (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    
    # Repeat after 10 ms
    root.after(10, lambda: update_frame_hsv(capture, video_label, root, int(resized_width), int(resized_height), last_update_time, update_interval,write))

def update_frame(capture:cv2.VideoCapture, video_label:label_to_put_video, 
                 root:tk.Tk, resized_width, resized_height, last_update_time, update_interval, write=None,enable_detection = False):
    ret, frame = capture.read()
    fps = 0
    start_time = time()
    # write(0, 0)
    # write(1, 0)
    # write(2, 0)
    # write(3, 0)
    if ret:
        frame = cv2.flip(frame, 1)
            # instead of loading .pt model, we'll load the .engine file
            # from model.ObjectDetection import ObjectDetection
        # frame, fps = detection.__call__(frame)

        # frame, xyxys, class_ids = tensorRT.detection(frame)
        register_state = [0, 0, 0, 0]
        frame, xyxys, class_ids = detection.webcam(frame)
        for bbox, class_id in zip(xyxys, class_ids):
            x1, y1, x2, y2 = bbox
            if class_id == 0:
                # write holding register to address number 3, value 1
                # write(3, 1) if write is not None else print("Cannot send signal to address 3, value 1")
                register_state[3] = 1

            elif class_id == 4: # red
                register_state[0] = 1
            elif class_id == 3: # green
                register_state[1] = 1
            elif class_id == 2: # blue
                register_state[2] = 1
            else: 
                continue
        print(register_state)
        if time() - last_update_time >= update_interval:
            for i in range(4):
                write(i, register_state[i]) if write is not None else print(f"Cannot write to address {register_state[i]}, value {i}")
            last_update_time = time()

        end_time = time()

        if (end_time - start_time) > 0:
            fps = 1 / (end_time - start_time)

        frame = cv2.resize(frame, (int(resized_width), int(resized_height)))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        current_date = datetime.date.today()
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        cv2.putText(frame, f"{current_date} {current_time}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, f'FPS: {int(fps)}', (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    
    # Repeat after 10 ms
    root.after(10, lambda: update_frame(capture, video_label, root, int(resized_width), int(resized_height), last_update_time, update_interval, write))

def update_normal_frame(capture:cv2.VideoCapture, video_label:label_to_put_video, 
                 root:tk.Tk, resized_width, resized_height, last_update_time, update_interval, write=None, enable_detection = False):
    ret, frame = capture.read()
    fps = 0
    start_time = time()
    if ret:
        frame = cv2.flip(frame, 1)

        end_time = time()

        if (end_time - start_time) > 0:
            fps = 1 / (end_time - start_time)

        frame = cv2.resize(frame, (int(resized_width), int(resized_height)))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        current_date = datetime.date.today()
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        cv2.putText(frame, f"{current_date} {current_time}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, f'FPS: {int(fps)}', (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    
    # Repeat after 10 ms
    root.after(10, lambda: update_normal_frame(capture, video_label, root, int(resized_width), int(resized_height), last_update_time, update_interval, write))