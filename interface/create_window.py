import customtkinter as ctk
import tkinter as tk
import cv2
from PIL import Image, ImageTk

class CreateWindow:
    def __init__(self, *args, **kwargs):
        self.root = ctk.CTk()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.attributes('-fullscreen', True)
        self.root.title("Color Detection")
        self.root.configure(bg="black")

        self.frame = ctk.CTkFrame(master=self.root, fg_color="#ffd7b5")
        self.frame.pack(fill="both", expand=True)
        # self.label_to_put_video()
        # Bind ESC to exit
        self.root.bind('<Escape>', self.exit_fullscreen)

        # Start the webcam feed
        self.capture = cv2.VideoCapture(0)
        self.update_frame()

        self.root.mainloop()
    def label_to_put_video(self, width=640, height=480):
        self.video_label = tk.Label(self.frame, bg="black")
        self.video_label.place(x=0, y=0, relwidth=width/self.screen_width, relheight=height/self.screen_height)
    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        
        # Repeat after 10 ms
        self.root.after(10, self.update_frame)

    def exit_fullscreen(self, event):
        self.capture.release()
        self.root.destroy()

CreateWindow()
