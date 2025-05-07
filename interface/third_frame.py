import customtkinter as ctk
import tkinter as tk

class ThirdFrame():
    def __init__ (self, screen_width: ctk.CTk.winfo_screenwidth, 
                 video_frame_width, screen_height:ctk.CTk.winfo_screenheight, 
                 video_frame_height, fg_color = "#ffd7b5"):
        self.fg_color = fg_color
        self.third_frame = ctk.CTkFrame(master = None, fg_color = fg_color)
        
        self.screen_width = screen_width
        self.video_frame_width = video_frame_width
        self.screen_height = screen_height
        self.video_frame_height = video_frame_height
        
        self.third_frame.place(relx = 0,
                               rely = video_frame_height/screen_height,
                               relwidth = video_frame_width/screen_width,
                               relheight = (screen_height - video_frame_height)/screen_height
                               )
        self.lights_system_to_detect_failure()
        self.third_frame.update()

    def lights_system_to_detect_failure(self):
        self.lights_frame = ctk.CTkFrame(self.third_frame, 
                                         fg_color=self.fg_color, 
                                         border_color="black",
                                         border_width=2, corner_radius = 10)
        
        self.lights_frame_width = 1/4 * self.video_frame_width
        self.lights_frame_height = 2/3 * (self.screen_height - self.video_frame_height)

        self.lights_frame.place(relx = 0.25, 
                                rely = 1/8,
                                relwidth = 0.5,
                                relheight = 6/8,
                                )
        
        
        self.label = ctk.CTkLabel(self.lights_frame, text = "Lights system to detect failure", 
                                         text_color = "orange", 
                                         font = ("Arial", 20), 
                                         fg_color = "black", corner_radius = 10,
                                            bg_color = "black",
                                         )
        self.label.place(relx=0, rely= 0 , relwidth = 1, relheight = 1/4)
        
        self.light1 = ctk.CTkCanvas(self.lights_frame,
                                   bg = self.fg_color, 
                                   highlightthickness = 0,
                                #    border_width = 2,
                                #    border_radius = 50,
                                   )
        self.light1.place(relx = 0.1, rely = 0.3, relwidth = 0.2, relheight = 0.2)
        self.light1.create_oval(0, 0, 1, 1, fill = "red", outline = "black")

