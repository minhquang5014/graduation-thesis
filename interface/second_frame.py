import customtkinter as ctk
import tkinter as tk
from PIL import Image
from threading import Thread
class SecondFrame():
    def __init__(self,screen_width: ctk.CTk.winfo_screenwidth, 
                 video_frame_width, screen_height:ctk.CTk.winfo_screenheight, 
                 video_frame_height, fixed_button_size:bool, fg_color = "#ffd7b5",*args, **kwargs):
        self.screen_width = screen_width 
        self.video_frame_width = video_frame_width
        self.screen_height = screen_height
        self.video_frame_height = video_frame_height
        self.fg_color = fg_color
        self.fixed_button_size = fixed_button_size
        self.second_frame = ctk.CTkFrame(master=None, fg_color=self.fg_color)
        self.second_frame_width = screen_width - video_frame_width
        self.second_frame.place(relx=video_frame_width/screen_width,
                            rely=0,
                            relwidth=self.second_frame_width/screen_width,
                            relheight=video_frame_height/screen_height
                            )
        self.putting_buttons()
        self.putting_group_name()
        self.start_stop_lights()
        self.lights_indicate_product_quality()
        # self.putting_logo()
        self.second_frame.update()

    def putting_buttons(self):
        self.button_frame = ctk.CTkFrame(self.second_frame, fg_color=self.fg_color)
        self.button_frame_width = 8/12 * self.second_frame_width
        self.button_frame_height = 1/5 * self.video_frame_height
        self.button_frame.place(relx=0,
                            rely=0,
                            relwidth= self.button_frame_width / self.second_frame_width,
                            relheight= 1/5 
                            )
        if self.fixed_button_size:
            self.width = 240
            self.height = 60
        else:
            self.width = self.button_frame_width / 4
            self.height = self.button_frame_height / 3
        self.start_button = ctk.CTkButton(self.button_frame, 
                                          text="START",
                                          width = self.width,
                                          height = self.height,
                                          fg_color = "green",
                                            corner_radius = 50, 
                                            hover_color="gray", 
                                            command=self.clicked_start
                                            )
        # self.start_button.grid(row=0, column=0, padx=5, pady=5, anchor = tk.CENTER)
        self.start_button.place(relx = 7/24, rely = 0.5, anchor = tk.CENTER)
        self.stop_button = ctk.CTkButton(self.button_frame, 
                                          text="STOP",
                                          width = self.width,
                                          height = self.height,
                                          fg_color = "red",
                                            corner_radius = 50, 
                                            hover_color="gray", 
                                            command=self.clicked_stop
                                            )
        self.stop_button.place(relx = 17/24, rely = 0.5, anchor = tk.CENTER)
    def putting_group_name(self):
        self.name_label = tk.Label(self.second_frame, bg="black")
        
        self.name_label.place(relx= (8/12 * self.second_frame_width) / self.second_frame_width,
                        rely = 0,
                        relwidth = (4/12 * self.second_frame_width) / self.second_frame_width,
                        relheight = 5/9
                        )
        for i in range (6):
            self.name_label.rowconfigure(i, weight =1)
            self.name_label.columnconfigure(0, weight=1)
        self.name1 = ctk.CTkLabel(self.name_label, text= "Nhóm 3", text_color="yellow", 
                                            font=ctk.CTkFont(size=20, weight="bold"))
        self.name1.grid(row=0, column = 0)
        self.name2 = ctk.CTkLabel(self.name_label, text="Trần Minh Quang", text_color="white", 
                                            font=ctk.CTkFont(size=15, weight="bold"))
        self.name2.grid(row=1, column=0)
        self.name3 = ctk.CTkLabel(self.name_label, text="Nguyễn Tiến Đạt", text_color="white",
                                            font=ctk.CTkFont(size=15, weight="bold"))
        self.name3.grid(row=2, column=0)
        self.name4 = ctk.CTkLabel(self.name_label, text="Vũ Việt Bắc", text_color="white", bg_color="black",
                                            font=ctk.CTkFont(size=15, weight="bold"))
        self.name4.grid(row=3, column=0)
        self.name5 = ctk.CTkLabel(self.name_label, text="Vũ Văn Long", text_color="white", bg_color="black",
                                            font=ctk.CTkFont(size=15, weight="bold"))
        self.name5.grid(row=4, column=0)
        self.name6 = ctk.CTkLabel(self.name_label, text="ThS.Nguyễn Quang Thư", text_color="white",
                                            font=ctk.CTkFont(size=15, weight="bold"))
        self.name6.grid(row=5, column=0)
        self.name_label.update()

    def putting_logo(self):
        self.width_for_image = int(self.video_frame_height / 2.25)
        self.bg_image = ctk.CTkImage(Image.open("logo_my_uni.jpg"),
                                               size=(self.width_for_image, self.width_for_image))
        self.bg_image_label = ctk.CTkLabel(self.second_frame, image=self.bg_image)
        self.bg_image_label.place(
            relx = (8/12 * self.second_frame_width) / self.second_frame_width,
            rely = 5/9,
            relwidth = (4/12 * self.second_frame_width) / self.second_frame_width,
            relheight = (4/9 * self.video_frame_height) / self.video_frame_height
        )
    def start_stop_lights(self):
        self.lights_frame = ctk.CTkFrame(self.second_frame, fg_color=self.fg_color, 
                                        #  border_color="black",
                                        # border_width=2, corner_radius = 10
                                        )
        self.lights_frame.place(relx = 1/8 * self.button_frame_width / self.second_frame_width,
                                rely = self.button_frame_height / self.video_frame_height,
                                relwidth = 3/4 * self.button_frame_width / self.second_frame_width,
                                relheight = 1/5)
        # print(3/4 * self.button_frame_width, 1/5 * self.video_frame_height)

        self.lights_canvas_start = ctk.CTkCanvas(self.lights_frame, bg = self.fg_color, 
                                           highlightthickness = 0, )
        self.lights_canvas_start.place(relx = 1/8, rely = 0,
                                       relwidth = 1/4,
                                       relheight = 7/8
                                       )
        self.lights_canvas_stop = ctk.CTkCanvas(self.lights_frame, bg=self.fg_color, 
                                                highlightthickness = 0, )
        self.lights_canvas_stop.place(relx = 1/2 + 1/8, 
                                      rely = 0,
                                      relwidth = 1/4,
                                      relheight = 7/8
                                      )
        self.lights_canvas_start.create_oval(0, 0, 
                                             3/16 * self.button_frame_width, 
                                             7/8 * self.button_frame_height, 
                                             fill="green", outline = "black")
        self.lights_canvas_stop.create_oval(0, 0, 
                                             3/16 * self.button_frame_width, 
                                             7/8 * self.button_frame_height,
                                             fill="red", outline="black")
        # self.lights_start = ctk.CTkLabel(self.lights_frame, text="Start", text_color="black", bg_color=self.fg_color,
        #                                         font=ctk.CTkFont(size=10, weight="bold"))
        # self.lights_start.place(relx = 1/4, rely = 1, anchor = tk.CENTER)
        self.lights_canvas_start.create_text(3/32 * self.button_frame_width ,
                                                7/8 * self.button_frame_height / 2,
                                                text = "Start",
                                                fill = "black",
                                                font = ctk.CTkFont(size=10, weight="bold")
                                                )
        self.lights_canvas_stop.create_text((3/32 * self.button_frame_width),
                                            7/8 * self.button_frame_height / 2,
                                                text = "Stop",
                                                fill = "black",
                                                font = ctk.CTkFont(size=10, weight="bold")
                                                )
        self.lights_frame.update()
    def lights_indicate_product_quality(self):
        self.lights_indicate_product_quality_frame = ctk.CTkFrame(self.second_frame, fg_color="black")
        self.lights_indicate_product_quality_frame.place(relx = 0, 
                                                         rely = 2 * self.button_frame_height / self.video_frame_height,
                                                         relwidth = self.button_frame_width / self.second_frame_width,
                                                         relheight = 1/5)

    def clicked_start(self):
        print("start clicked")
    def clicked_stop(self):
        print("stop clicked")