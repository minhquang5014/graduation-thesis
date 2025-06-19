import torch
import numpy as np
import cv2
from time import time
from ultralytics import YOLO
from supervision.draw.color import ColorPalette, Color
from supervision import Detections, BoxAnnotator
import tkinter as tk
from tkinter import Button
from PIL import ImageTk, Image
import datetime
import os
import sys
# I don't know why every single time when I wanna import module from another folder, I would have to add the path of the parent folder to the system path. 
# It is just so annoying, is there any other ways to do it quickly??
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from PLC.plc_connection import PLCConnection
    print("Import successfully")
except ModuleNotFoundError:
    print("Import error")
colors=[Color(r=255, g=64, b=64), Color(r=255, g=161, b=160)]
class Webcam:
    def __init__(self, capture_index, model, window, window_title, detection=False):
        self.window = window
        self.window_title = window_title
        self.capture_index = capture_index
        self.model = model
        self.register_state = [0, 0, 0, 0]

        if detection == True:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
            print(f"Device used: {self.device}")
            self.model = YOLO(model)
            self.model.fuse()
            self.model.to(self.device)
            self.CLASS_NAMES_DICT = self.model.model.names 
            self.box_annotator = BoxAnnotator(color=ColorPalette(colors=colors), thickness=3)

        self.vid = cv2.VideoCapture(self.capture_index)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.canvas = tk.Canvas(window, width=self.width, height=self.height)
        self.canvas.pack()

        self.btn_record = Button(window, text="record", width=15, command=self.record)
        self.btn_record.pack(side=tk.LEFT)

        self.btn_snapphoto = Button(window, text="take photo", width=15, command = self.take_photo)
        self.btn_snapphoto.pack(side=tk.LEFT)
    
        self.show_box = False
        self.text = tk.Text(window, width = int(self.width/40), height = int(self.height / 200))
        self.text.tag_configure("center", justify='center', foreground="red", font=("helvetica", 12, "bold"))
        self.text.insert(tk.END, "no face detected")
        self.text.tag_add("center", "1.0", "end")
        self.text.configure(state=tk.DISABLED)
        self.text.pack(side=tk.LEFT)

        self.button_show = Button(window, text="Show_bounding_box", width = 20, command = self.toggle_box)
        self.button_show.pack(side=tk.LEFT)

        self.is_recording = False
        self.out = None
        self.plc_connection_status = False
        self.directories = "images"
        if not os.path.exists(self.directories):
            os.makedirs(self.directories)
        self.update()
        self.plc_connection_status = self.connect_plc()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def connect_plc(self):
        self.call_out_PLC_object = PLCConnection()  # no need to specify the ip address and port, let's just put the default value there
        self.plc_connection_status = self.call_out_PLC_object.connectPLC()   
        return self.plc_connection_status
    def toggle_box(self):
        self.show_box = not self.show_box

    def face_detected(self):
        self.text.configure(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, "face_detected")
        self.text.tag_add("center", "1.0", "end")
        self.text.configure(state=tk.DISABLED)
    def no_face_detected(self):
        self.text.configure(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, "no face detected")
        self.text.tag_add("center", "1.0", "end")
        self.text.configure(state=tk.DISABLED)

    def predict(self, frame):
        return self.model(frame)
    
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

    def take_photo(self):
        ret, frame = self.vid.read()
        if ret:
            filename = os.path.join(self.directories,f"photo_{datetime.datetime.now().strftime('%d%m_%Hh%Mm%Ss')}.jpg")
            cv2.imwrite(filename, frame)
            print(f"photo saved as {filename}")

    def record(self):
        if self.is_recording:
            self.is_recording = False
            if self.out:
                self.out.release()
                self.out = None
            self.btn_record.config(text="Start Recording")
            print("Recording stopped")
        else:
            self.is_recording = True
            file_name = os.path.join(self.directories, f"video_{datetime.datetime.now().strftime('%d%M%Y_%Hh%Mm%Ss')}.avi")
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            frame_width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.out = cv2.VideoWriter(file_name, fourcc, 20.0, (frame_width, frame_height))
            self.btn_record.config(text="Stop recording")
            print(f"Recording started. Saving to {file_name}")
        
    def update(self):
        last_update_time = time()
        update_interval = 0.4
        ret, frame = self.vid.read()
        frame = cv2.flip(frame, 1)
        fps = 0
        if ret:
            start_time = time()

            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.predict(frame)
            frame, boxes_out = self.plot_boxes(results, frame)
            self.register_state = [0, 0, 0, 0]
            for ((x1, y1, x2, y2), class_id) in boxes_out:
                if class_id == 0:
                    self.register_state[3] = 1
                elif class_id == 4:
                    self.register_state[0] = 1
                elif class_id == 3:
                    self.register_state[1] = 1
                elif class_id == 2:
                    self.register_state[2] = 1
                else:
                    continue
            if time() - last_update_time >= update_interval:
                for i in range(4):
                    self.call_out_PLC_object.write(i, self.register_state[i]) if self.plc_connection_status != False else print(f"Cannot send signal to PLC address {i}")
                last_update_time = time()
            end_time = time()
            if end_time - start_time != 0:
                fps = 1/np.round(end_time - start_time, 2)
            # print(fps)
            cv2.putText(frame, f'FPS: {int(fps)}', (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            if self.is_recording and self.out is not None:
                self.out.write(frame)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)   

    def on_closing(self):
        if self.is_recording:
            self.is_recording = False
            if self.out is not None:
                self.out.release()
                self.out = None
        self.vid.release()
        self.window.destroy()
        
if __name__ == '__main__':
    root = tk.Tk()
    webcam_detectuion = Webcam(capture_index="video/3.avi",model = "model/best.pt", window=root, window_title="Detection interface", detection=True)


