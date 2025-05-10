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
      
      self.lights_frame_width = self.video_frame_width - (8/64 * self.video_frame_width * 2)
      self.lights_frame_height = self.video_frame_height - (2/64 * (self.screen_height - self.video_frame_height) * 2)

      self.lights_frame.place(relx = 8/64, 
                              rely = 2/64,
                              relwidth = self.lights_frame_width / self.video_frame_width,
                              relheight = self.lights_frame_height / self.video_frame_height,
                              )

      self.label = ctk.CTkLabel(self.lights_frame, text = "PLC Output", 
                                       text_color = "orange", 
                                       font = ("Arial", 18), 
                                       fg_color = "black", corner_radius = 10,
                                          bg_color = "black",
                                       )
      self.label.place(relx=0, rely= 0, relwidth = 1, relheight = 1/6)
      self.canvas_list = []
      bg_for_canvas = self.fg_color

      # create 6 canvas for output lighting system
      for i in range(6):
         self.light = ctk.CTkCanvas(self.lights_frame,
                                       bg = bg_for_canvas, 
                                       highlightthickness = 0,
                                       )
         self.canvas_list.append(self.light)

      self.lights_canvas_height = self.lights_frame_height * 5/6 
      self.lights_canvas_y = self.lights_frame_height * (1/6 + 1/64)

      self.canvas_list[0].place(relx = 1/15, 
                        rely = self.lights_canvas_y / self.lights_frame_height,
                        relwidth= 1/5,
                        relheight= 1/3)
      
      self.canvas_list[1].place(relx = 6/15,
                                rely = 1/6 + 1/64,
                                relwidth= 1/5,
                                relheight= 1/3)
      self.canvas_list[2].place(relx= 11/15,
                                rely = 1/6 + 1/64,
                                relwidth= 1/5,
                                relheight= 1/3)
      self.canvas_list[3].place(relx = 1/15,
                                rely = 3/6 + 1/12,
                                 relwidth= 1/5,
                                 relheight= 1/3)
      self.canvas_list[4].place(relx = 6/15,
                                rely = 3/6 + 1/12,
                                 relwidth= 1/5,
                                 relheight= 1/3)
      self.canvas_list[5].place(relx = 11/15,
                                rely = 3/6 + 1/12,
                                 relwidth= 1/5,
                                 relheight= 1/3)
      
      for self.light in self.canvas_list:
         self.light.create_oval(0, 0, 1/5 * self.lights_frame_width, 1/5 * self.lights_canvas_height,
                                 fill = "gray", 
                                 outline = "black")
      





