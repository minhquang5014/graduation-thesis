import tkinter as tk
import cv2
from PIL import Image, ImageTk
from time import time
import datetime
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

def update_frame(capture:cv2.VideoCapture, video_label:label_to_put_video, 
                 root:tk.Tk, resized_width, resized_height, enable_detection = False):
    ret, frame = capture.read()
    if ret:
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (int(resized_width), int(resized_height)))
        if enable_detection == True:
            from model.ObjectDetection import ObjectDetection
            frame = ObjectDetection(frame = frame, model="model/best2.pt").__call__()
            
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        current_date = datetime.date.today()
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        cv2.putText(frame, f"{current_date} {current_time}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    
    # Repeat after 10 ms
    root.after(10, lambda: update_frame(capture, video_label, root, int(resized_width), int(resized_height)))

def update_frame_and_attempt_reconnection(capture_container:list[cv2.VideoCapture], video_label:label_to_put_video, root:tk.Tk, resized_width, resized_height):
    def loop():
        capture = capture_container[0]

        if not capture or not capture.isOpened():
            video_label.configure(text="Camera not available", image="")
            try:
                # Try reconnecting
                new_cap = cv2.VideoCapture(0)
                if new_cap.isOpened():
                    capture_container[0] = new_cap
                    print("Camera reconnected.")
                else:
                    new_cap.release()
            except Exception as e:
                print("Reconnect failed:", e)

            root.after(1000, loop)  # Check again after 1s
            return

        ret, frame = capture.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (int(resized_width), int(resized_height)))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            current_date = datetime.date.today()
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            cv2.putText(frame, f"{current_date} {current_time}", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk, text="")
        else:
            print("Camera disconnected during stream.")
            capture.release()
            capture_container[0] = None

        root.after(30, loop)

    loop()
