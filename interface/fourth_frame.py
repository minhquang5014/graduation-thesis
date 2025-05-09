import customtkinter as ctk
import tkinter as tk

class FourthFrame():
    def __init__ (self, screen_width: ctk.CTk.winfo_screenwidth, 
                 video_frame_width, screen_height:ctk.CTk.winfo_screenheight, 
                 video_frame_height, fg_color = "#ffd7b5"):
        self.fg_Color = fg_color
        self.fourth_frame = ctk.CTkFrame(master = None, fg_color = fg_color)
        
        self.screen_width = screen_width
        self.video_frame_width = video_frame_width
        self.screen_height = screen_height
        self.video_frame_height = video_frame_height

        self.fourth_frame_width = self.screen_width - self.video_frame_width
        self.fourth_frame_height = self.screen_height - self.video_frame_height

        self.fourth_frame.place(relx = video_frame_width/screen_width,
                               rely = video_frame_height/screen_height,
                               relwidth = self.fourth_frame_width/screen_width,
                               relheight = self.fourth_frame_height/screen_height
                               )
        self.fourth_frame.update()
