import customtkinter as ctk
import tkinter as tk

class FourthFrame():
    def __init__ (self, screen_width: ctk.CTk.winfo_screenwidth, 
                 video_frame_width, screen_height:ctk.CTk.winfo_screenheight, 
                 video_frame_height, fg_color = None):
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
        self.change_appearance()
        self.fourth_frame.update()

    def auto_manual(self):
        self.auto_manual_frame = ctk.CTkFrame(master = self.fourth_frame, fg_color = self.fg_color, 
                                                # border_color = "black",
                                                # border_width = 2,
                                                # corner_radius = 10
                                                )
        self.auto_manual_frame_height = self.screen_height - self.video_frame_height 
        self.auto_manual_frame.place(relx = 0,
                                    rely = 0, 
                                    relwidth = self.auto_manual_frame_height/self.fourth_frame_width,
                                    relheight = self.auto_manual_frame_height / self.fourth_frame_height)


        self.switch = ctk.CTkSwitch(self.auto_manual_frame, text = "MANUAL", command=self.switch_event)
        self.switch.place(relx = 1/2, 
                          rely = self.switch.winfo_reqheight()/self.auto_manual_frame_height, anchor = "center")
        
        self.manual_auto_light = ctk.CTkFrame(self.auto_manual_frame, fg_color = "black")
        self.manual_auto_light.place(relx = 0,
                                     rely = self.switch.winfo_reqheight() * 3/self.auto_manual_frame_height,
                                     relwidth = 1,
                                     relheight  = (self.auto_manual_frame_height - self.switch.winfo_reqwidth())/ self.auto_manual_frame_height)
        print(self.manual_auto_light.winfo_reqwidth(), self.manual_auto_light.winfo_reqheight())
        self.manual_canvas_light = ctk.CTkCanvas(self.manual_auto_light, bg= self.fg_color,
                                                 highlightthickness = 0)
        self.manual_canvas_light.place(relx = 1/20, 
                                       rely = 0,
                                       relwidth = 2/5, 
                                       relheight = 3/5)
        print(self.manual_canvas_light.winfo_reqwidth(), self.manual_canvas_light.winfo_reqheight())
        self.manual_canvas_light.create_oval(0, 0,
                                                2/5 * self.auto_manual_frame_height,
                                                3/5 * self.manual,
                                                fill="gray", 
                                                outline="black")

        self.auto_canvas_light = ctk.CTkCanvas(self.manual_auto_light, bg = self.fg_color,
                                                highlightthickness = 0)
        self.auto_canvas_light.place(relx = 1/20 + 1/2,
                                     rely = 0,
                                     relwidth = 2/5,
                                     relheight = 3/5)
        self.auto_manual_frame.update()

    def change_appearance(self):
        self.frame_for_option_menu = ctk.CTkFrame(self.fourth_frame, fg_color = self.fg_color)
        self.appearance_mode_option_menu = ctk.CTkOptionMenu(master = self.frame_for_option_menu, values = ["Peace puff", "Sour green cherry"], 
                                                             command=self.func_to_change_color())
        self.frame_for_option_menu.place(relx = (self.fourth_frame_width - self.appearance_mode_option_menu.winfo_reqwidth()) / self.fourth_frame_width, 
                                         rely = 0, 
                                         relwidth = self.appearance_mode_option_menu.winfo_reqwidth() / self.fourth_frame_width, 
                                         relheight = 1)
        self.appearance_mode_option_menu.place(relx = 1/2, rely = 1/4, anchor = "center")
        return self.appearance_mode_option_menu.get()
    def func_to_change_color(self):
        pass
    def switch_event(self):
        if self.switch.get() == 1:
            print("Switching to manual mode")
        else:
            print("Switching back to auto mode")