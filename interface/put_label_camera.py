import tkinter as tk
import cv2
from PIL import Image, ImageTk
from time import time
import datetime
import numpy as np
import os

class FirstLabel:
    def __init__(self,video_capture, image_output_dir:str, video_output_dir:str, insert_textbox = None, model_path = None, yaml_path = None, model_type=None):
        self.register_state = [0, 0, 0, 0]
        self.insert_textbox = insert_textbox or (lambda msg: print(f"[Pending UI]: {msg}"))
        self.recording = False
        self.out = None
        self.model_path = model_path
        self.image_outout_dir = image_output_dir
        self.video_output_dir = video_output_dir
        self.yaml_path = yaml_path
        self.video_capture = video_capture
        self.current_frame = None
        self.model_type = model_type
        if self.model_type == "pt":
            self.model_path = "model/training_with_6classes.pt" if self.model_path is None else self.model_path  # specify your custom model path or it will use the default model in the working dir to run inference
            self.model = self.load_pytorch_model()
            self.insert_textbox(f"Loading pytorch model {self.model_path} for object detection")
        elif self.model_type == "rt":
            self.model_path = "model/custom_train_yolov10s_4.engine" if self.model_path is None else self.model_path
            self.yaml_path = "model/data.yaml" if self.yaml_path is None else self.yaml_path
            self.model = self.load_tensorrt_model()
            self.insert_textbox(f"Loading tensorRT model {self.model_path} for object detection")
    def load_tensorrt_model(self):
        from model.running_tensorRT import TensorRTDetection
        self.tensorRT = TensorRTDetection(video_capture = self.video_capture, model_path = self.model_path, yaml_path=self.yaml_path)
        return self.tensorRT  # call out the TensorRT object
    def load_pytorch_model(self):
        from model.ObjectDetection import ObjectDetection
        self.detection = ObjectDetection(self.model_path)
        return self.detection  # call out the object
    def label_to_put_video(self, frame, screen_width, screen_height, fixed_video_label=False, label_width=None, label_height=None):
        if fixed_video_label:
            label_width = 640
            label_height = 480
        else:
            label_width = screen_width / 1.953
            label_height = screen_height / 1.354
        video_label = tk.Label(frame, bg="black")
        video_label.place(x=0, y=0, relwidth=label_width/screen_width, relheight=label_height/screen_height)
        return video_label, label_width, label_height
    def update_frame(self, capture:cv2.VideoCapture, video_label:label_to_put_video, 
                    root:tk.Tk, resized_width, resized_height, last_update_time, update_interval, write=None):
        ret, frame = capture.read()
        if ret:
            fps = 0
            start_time = time()
            frame = cv2.flip(frame, 1)
                # instead of loading .pt model, we'll load the .engine file
                # from model.ObjectDetection import ObjectDetection
            # frame, fps = detection.__call__(frame)

            # frame, xyxys, class_ids = tensorRT.detection(frame)
            self.register_state = [0, 0, 0, 0]
            if self.model_type != None:  # can this disable the model detection if we don't need it??
                frame, xyxys, class_ids = self.model.webcam(frame)
                for bbox, class_id in zip(xyxys, class_ids):
                    x1, y1, x2, y2 = bbox
                    if class_id == 0:
                        # write holding register to address number 3, value 1
                        # write(3, 1) if write is not None else print("Cannot send signal to address 3, value 1")
                        self.register_state[3] = 1
                    elif class_id == 4: # red
                        self.register_state[0] = 1
                    elif class_id == 3: # green
                        self.register_state[1] = 1
                    elif class_id == 2: # blue
                        self.register_state[2] = 1
                    else: 
                        continue
                print(self.register_state)
                if time() - last_update_time >= update_interval:
                    for i in range(4):
                        write(i, self.register_state[i]) if write is not None else print(f"Cannot write to address {self.register_state[i]}, value {i}")
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

            if self.recording and self.out:
                self.out.write(cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR))  # convert back to BGR to save in the color dir

            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
            self.current_frame = cv2.cvtColor(frame.copy(), cv2.COLOR_RGBA2BGR)
        # Repeat after 10 ms
        root.after(10, lambda: self.update_frame(capture, video_label, root, int(resized_width), int(resized_height), last_update_time, update_interval, write))
        return int(resized_width), int(resized_height)
    def taking_photo(self):
        # maybe this function can be defined on the main.py file
        if self.current_frame is not None:
            self.capture_image(self.current_frame)
        else:
            self.insert_textbox("No frame to capture. Please recheck camera connection")
    def capture_image(self, frame, image_name = f"photo_{datetime.datetime.now().strftime('%d%m_%Hh%Mm%Ss')}.jpg"):
        if not os.path.exists(self.image_outout_dir):
            os.makedirs(self.image_outout_dir)
        filename = os.path.join(self.image_outout_dir,image_name)
        cv2.imwrite(filename, frame)
        self.insert_textbox(f"photo saved as {filename}")
    def record_video(self, vid, record_button):
        if self.recording:
            self.recording = False
            if self.out:
                self.out.release()
                self.out = None
            record_button.configure(text="Start Recording")
            self.insert_textbox("Recording stopped")
        else:
            self.recording = True
            if not os.path.exists(self.video_output_dir):
                os.makedirs(self.video_output_dir)
                self.insert_textbox(f"Creating an output folder to store video recording outputs {self.video_output_dir}")
            file_name = os.path.join(
                self.video_output_dir,
                f"video_{datetime.datetime.now().strftime('%d%m%Y_%Hh%Mm%Ss')}.avi"
            )
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            frame_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.out = cv2.VideoWriter(file_name, fourcc, 20.0, (frame_width, frame_height))
            record_button.configure(text="Stop Recording")
            self.insert_textbox(f"Recording started. Saving to {file_name}")
    def set_insert_textbox(self, insert_textbox):
        self.insert_textbox = insert_textbox
        




    # these functions below didn't really work, please don't call it now
    # unnecessary function, just for the purpose of testing
    def update_normal_frame(self, capture:cv2.VideoCapture, video_label:label_to_put_video, 
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
        root.after(10, lambda: self.update_normal_frame(capture, video_label, root, int(resized_width), int(resized_height), last_update_time, update_interval, write))
    def update_frame_hsv(self, capture:cv2.VideoCapture, video_label:label_to_put_video, 
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
            frame, xyxys, class_ids = self.detection.__call__(frame)
            for bbox, class_id in zip(xyxys, class_ids):
                x1, y1, x2, y2 = bbox
                if class_id == 0:
                    # write holding register to address number 3, value 1
                    # write(3, 1) if write is not None else print("Cannot send signal to address 3, value 1")
                    self.register_state[3] = 1  
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
                            self.register_state[address] = 0
                            # write(address, 1)
                            break
            if time() - last_update_time >= update_interval:
                for i in range(4):
                    write(i, self.register_state[i]) if write is not None else print(f"Cannot write to address {self.register_state[i]}, value {i}")
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
        root.after(10, lambda: self.update_frame_hsv(capture, video_label, root, int(resized_width), int(resized_height), last_update_time, update_interval,write))