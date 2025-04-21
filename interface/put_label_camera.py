import tkinter as tk
import cv2
from PIL import Image, ImageTk

def label_to_put_video(frame, screen_width, screen_height, width=640, height=480):
    video_label = tk.Label(frame, bg="black")
    video_label.place(x=0, y=0, relwidth=width/screen_width, relheight=height/screen_height)
    return video_label
def update_frame(capture:cv2.VideoCapture, video_label:label_to_put_video, root:tk.Tk):
    ret, frame = capture.read()
    if ret:
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    
    # Repeat after 10 ms
    root.after(10, lambda: update_frame(capture, video_label, root))