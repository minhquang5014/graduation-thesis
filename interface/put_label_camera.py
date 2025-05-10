import tkinter as tk
import cv2
from PIL import Image, ImageTk

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
def update_frame(capture:cv2.VideoCapture, video_label:label_to_put_video, root:tk.Tk, resized_width, resized_height):
    ret, frame = capture.read()
    if ret:
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (int(resized_width), int(resized_height)))
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    
    # Repeat after 10 ms
    root.after(10, lambda: update_frame(capture, video_label, root, int(resized_width), int(resized_height)))