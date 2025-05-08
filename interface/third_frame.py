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
      self.third_frame_height = self.screen_height - self.video_frame_height
      self.lights_frame = ctk.CTkFrame(self.third_frame, 
                                       fg_color=self.fg_color, 
                                       border_color="black",
                                       border_width=2, corner_radius = 10)
      
      self.lights_frame_width = self.video_frame_width - (8/64 * self.video_frame_width * 2)
      self.lights_frame_height = self.third_frame_height - (4/64 * self.third_frame_height * 2)
      self.lights_frame.place(relx = 8/64, 
                              rely = 4/64,
                              relwidth = self.lights_frame_width / self.video_frame_width,
                              relheight = self.lights_frame_height / self.third_frame_height
      )

      self.label = ctk.CTkLabel(self.lights_frame, text = "PLC Output", 
                                       text_color = "orange", 
                                       font = ("Arial", 18), 
                                       fg_color = "black", corner_radius = 10,
                                          bg_color = "black",
                                       )
      self.label.place(relx=0, rely= 0, relwidth = 1, relheight = 1/6)
      self.canvas_list = []

      # create 4 canvas for output lighting system
      for i in range(4):
         self.canvas = ctk.CTkCanvas(self.lights_frame,
                                 bg = self.fg_color, 
                                 highlightthickness = 0, 
                                 )
         self.canvas_list.append(self.canvas)
      
      self.lights_canvas_height = self.lights_frame_height * 5/6
      self.lights_canvas_y = self.lights_frame_height * 1/6

      relative_width = 10/48 * self.lights_frame_width
      relative_height = 9/15 * self.lights_canvas_height
      
      self.canvas_list[0].place(relx = 10/480,
                                rely = 1/6 + (self.lights_canvas_height * 2/15) / self.lights_frame_height,
                                 relwidth = 10/48,
                                 relheight = relative_height / self.lights_frame_height)
      self.canvas_list[1].place(relx = 1/4 + 10/480,
                                rely = 1/6 + (self.lights_canvas_height * 2/15) / self.lights_frame_height,
                                relwidth = 10/48,
                                relheight = relative_height / self.lights_frame_height)
      self.canvas_list[2].place(relx = 1/2 + 10/480,
                                rely = 1/6 + (self.lights_canvas_height * 2/15) / self.lights_frame_height,
                                relwidth = 10/48,
                                relheight = relative_height / self.lights_frame_height)
      self.canvas_list[3].place(relx = 3/4 + 10/480,
                                rely = 1/6 + (self.lights_canvas_height * 2/15) / self.lights_frame_height,
                                relwidth = 10/48,
                                relheight = relative_height / self.lights_frame_height)
      for self.canvas in self.canvas_list:
         self.canvas.create_oval(0, 0, 
                                 10/48 * self.lights_frame_width,
                                 relative_height,
                                 fill = "gray", outline = "black")
      
      self.text1 = ctk.CTkLabel(self.lights_frame, text="Van xoay", text_color="black", bg_color=self.fg_color,
                                            font=ctk.CTkFont(size=15, weight="bold"))
      self.text2 = ctk.CTkLabel(self.lights_frame, text="Van đẩy", text_color="black", bg_color=self.fg_color,
                                            font=ctk.CTkFont(size=15, weight="bold"))
      self.text3 = ctk.CTkLabel(self.lights_frame, text="Van gắp", text_color="black", bg_color=self.fg_color,
                                             font=ctk.CTkFont(size=15, weight="bold"))    
      self.text4 = ctk.CTkLabel(self.lights_frame, text="Băng tải", text_color="black", bg_color=self.fg_color,
                                             font=ctk.CTkFont(size=15, weight="bold"))
      
      self.text1.place(relx = (10/480 * self.lights_frame_width + relative_width/2) / self.lights_frame_width,
                       rely = (relative_height + 4/15 * self.lights_canvas_height + self.lights_canvas_y) / self.lights_frame_height,
                       anchor = "center")
      self.text2.place(relx = ((1/4 + 10/480) * self.lights_frame_width + relative_width/2) / self.lights_frame_width,
                       rely = (relative_height + 4/15 * self.lights_canvas_height + self.lights_canvas_y) / self.lights_frame_height,
                       anchor = "center")
      self.text3.place(relx = ((1/2 + 10/480) * self.lights_frame_width + relative_width/2) / self.lights_frame_width,
                         rely = (relative_height + 4/15 * self.lights_canvas_height + self.lights_canvas_y) / self.lights_frame_height,
                         anchor = "center")
      self.text4.place(relx = ((3/4 + 10/480) * self.lights_frame_width + relative_width/2) / self.lights_frame_width,
                         rely = (relative_height + 4/15 * self.lights_canvas_height + self.lights_canvas_y) / self.lights_frame_height,
                         anchor = "center")


