import customtkinter as ctk
import tkinter as tk

class FourthFrame():
    def __init__ (self, screen_width: ctk.CTk.winfo_screenwidth, 
                 video_frame_width, screen_height:ctk.CTk.winfo_screenheight, 
                 video_frame_height, fg_color = "#ffd7b5"):
        self.fg_color = fg_color
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
        self.auto_manual()
        self.fourth_frame.update()
    def auto_manual(self):
        self.auto_manual_frame = ctk.CTkFrame(master = self.fourth_frame, fg_color = self.fg_color, 
                                                border_color = "black",
                                                border_width = 2,
                                                corner_radius = 10)
        self.auto_manual_frame_height = self.screen_height - self.video_frame_height 
        self.auto_manual_frame.place(relx = 0,
        rely = 0, 
        relwidth = self.auto_manual_frame_height/self.fourth_frame_width,
        relheight = self.auto_manual_frame_height / self.fourth_frame_height)
        self.auto_manual_frame.grid_rowconfigure((0, 1, 2), weight=1, uniform="a")
        self.auto_manual_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="a")

        self.switch = ctk.CTkSwitch(self.auto_manual_frame, text = "MANUAL", command=self.switch_event)
        self.switch.grid(row=0, column=1)
        
        self.manual_auto_light = ctk.CTkFrame(self.auto_manual_frame, fg_color = "black")
        self.manual_auto_light.place(relx = 0,
                                     rely = self.switch.winfo_reqheight() * 3/self.auto_manual_frame_height,
                                     relwidth = 1,
                                     relheight  = (self.auto_manual_frame_height - (self.switch.winfo_reqwidth()))/ self.auto_manual_frame_height)
        print(self.switch.winfo_reqheight(), self.switch.winfo_reqwidth())
        

        self.auto_manual_frame.update()
    def switch_event(self):
        if self.switch.get() == 1:
            print("Switching to manual mode")
        else:
            print("Switching back to auto mode")