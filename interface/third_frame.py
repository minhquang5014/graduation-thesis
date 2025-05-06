import customtkinter as ctk
import tkinter as tk

class ThirdFrame():
    def __init__ (self, screen_width: ctk.CTk.winfo_screenwidth, 
                 video_frame_width, screen_height:ctk.CTk.winfo_screenheight, 
                 video_frame_height, fg_color = "#ffd7b5"):
        self.fg_Color = fg_color
        self.third_frame = ctk.CTkFrame(master = None, fg_color = fg_color)
        