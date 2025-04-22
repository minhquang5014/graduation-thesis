import customtkinter as ctk
import tkinter as tk
import cv2
from PIL import Image, ImageTk

class CreateWindow:
    def __init__(self, *args, **kwargs):
        self.root = ctk.CTk()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        self.root.title("Color Detection")
        self.root.configure(bg="black")

        self.frame = ctk.CTkFrame(master=self.root, fg_color="#ffd7b5")
        self.frame.pack(fill="both", expand=True)

        self.root.update()
        self.root.attributes('-fullscreen', True)

    def exit_fullscreen(self, event):
        self.root.destroy()

# CreateWindow()

# class ExtentedWindow(CreateWindow):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.capture = cv2.VideoCapture(0)
#         self.video_label = label_to_put_video(self.frame, self.screen_width, self.screen_height)
#         update_frame(self.capture, self.video_label, self.root)
#         self.root.bind('<Escape>', self.exit_fullscreen)
#         self.root.mainloop()
#     def exit_fullscreen(self, event):
#         self.capture.release()
#         cv2.destroyAllWindows()
#         self.root.destroy()

# ExtentedWindow()