import customtkinter as ctk
import tkinter as tk
from PIL import Image
from threading import Thread
class SecondFrame():
    def __init__(self,screen_width: ctk.CTk.winfo_screenwidth, 
                 video_frame_width, screen_height:ctk.CTk.winfo_screenheight, 
                 video_frame_height, fixed_button_size:bool, fg_color = None,*args, **kwargs):
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
        # self.frame_to_show_detected_object()
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
                                relheight = 3/10)
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
        self.oval_start = self.lights_canvas_start.create_oval(0, 0, 
                                             3/16 * self.button_frame_width, 
                                             7/8 * self.button_frame_height, 
                                             fill="gray", outline = "black")
        self.oval_stop = self.lights_canvas_stop.create_oval(0, 0, 
                                             3/16 * self.button_frame_width, 
                                             7/8 * self.button_frame_height,
                                             fill="gray", outline="black")
        # self.lights_start = ctk.CTkLabel(self.lights_frame, text="Start", text_color="black", bg_color=self.fg_color,
        #                                         font=ctk.CTkFont(size=10, weight="bold"))
        # self.lights_start.place(relx = 1/4, rely = 1, anchor = tk.CENTER)
        self.lights_canvas_start.create_text(3/32 * self.button_frame_width ,
                                             self.button_frame_height,
                                                text = "Start",
                                                fill = "black",
                                                font = ctk.CTkFont(size=12, weight="bold")
                                                )
        self.lights_canvas_stop.create_text((3/32 * self.button_frame_width),
                                            self.button_frame_height,
                                                text = "Stop",
                                                fill = "black",
                                                font = ctk.CTkFont(size=12, weight="bold")
                                                )
        self.lights_frame.update()

    def lights_indicate_product_quality(self):
        self.product_quality_frame = ctk.CTkFrame(self.second_frame, fg_color=self.fg_color,
                                                  corner_radius=10, 
                                                  border_color="black",
                                                  border_width=2)
        self.product_quality_frame.place(relx = 0, 
                                        rely = self.button_frame_height / self.video_frame_height + 3/10,
                                        relwidth = self.button_frame_width / self.second_frame_width,
                                        relheight = 1/2)
        self.product_quality_frame_height = 1/2 * self.video_frame_height
        self.entry_text = ctk.CTkLabel(self.product_quality_frame, 
                                       text = "NHẬP", 
                                       text_color = "green", 
                                       font = ("Arial", 18))
        self.entry_text.place(relx = 1/4,
                              rely = 0,
                              relwidth = 1/4,
                              relheight = 1/5)
        self.counter_text = ctk.CTkLabel(self.product_quality_frame, 
                                       text = "ĐẾM", 
                                       text_color = "green", 
                                       font = ("Arial", 18))
        self.counter_text.place(relx = 2/4, 
                                rely = 0, 
                                relwidth = 1/4,
                                relheight = 1/5)
        self.reset_text = ctk.CTkLabel(self.product_quality_frame, 
                                       text = "RESET", 
                                       text_color = "green", 
                                       font = ("Arial", 18))
        self.reset_text.place(relx = 3/4,
                              rely = 0,
                              relwidth = 1/4,
                              relheight = 1/5)
        self.blue_text = ctk.CTkLabel(self.product_quality_frame, 
                                       text = "Xanh dương", 
                                       text_color = "green", 
                                       font = ("Arial", 18))
        self.red_text = ctk.CTkLabel(self.product_quality_frame, 
                                       text = "Hàng đỏ", 
                                       text_color = "green", 
                                       font = ("Arial", 18))
        self.green_text = ctk.CTkLabel(self.product_quality_frame, 
                                       text = "Xanh lá", 
                                       text_color = "green", 
                                       font = ("Arial", 18))
        self.NG_text = ctk.CTkLabel(self.product_quality_frame, 
                                       text = "Hàng lỗi", 
                                       text_color = "green", 
                                       font = ("Arial", 18))
        self.red_text.place(relx = 0, rely = 1/5, relwidth = 1/4, relheight = 1/5)
        self.green_text.place(relx = 0, rely = 2/5, relwidth = 1/4, relheight = 1/5)
        self.blue_text.place(relx = 0, rely = 3/5, relwidth = 1/4, relheight = 1/5)
        self.NG_text.place(relx = 0, rely = 4/5, relwidth = 1/4, relheight = 1/5)


        self.integer_var = tk.StringVar()
        self.red_entry = tk.Entry(self.product_quality_frame, textvariable=self.integer_var)
        self.red_entry.place(relx=1/4,
                               rely = 1/5, relwidth = 1/4, relheight = 1/5)

        self.red_show = tk.Text(self.product_quality_frame, width = int(1/5 * self.button_frame_width), height = int(1/5 * self.product_quality_frame_height))
        self.red_show.place(relx = 2/4,
                              rely = 1/5,
                              relwidth = 1/4, relheight = 1/5)
        self.red_show.tag_configure("center", justify='center', foreground="red", font=("Helvetica", 12, "bold"))
        self.red_show.insert(tk.END, "0")
        self.red_show.tag_add("center", "1.0", "end")
        self.red_show.configure(state="disabled")

        self.red_reset = ctk.CTkButton(self.product_quality_frame, text="RESET", fg_color="gray", command=self.reset1)
        self.red_reset.place(relx = 3/4,
                               rely = 1/5,
                               relwidth = 1/4, 
                               relheight = 1/5)
        
        self.integer_var2 = tk.StringVar()
        self.green_entry = tk.Entry(self.product_quality_frame, textvariable=self.integer_var2)
        self.green_entry.place(relx=1/4,
                               rely = 2/5, relwidth = 1/4, relheight = 1/5)

        self.green_show = tk.Text(self.product_quality_frame, width = int(1/4 * self.button_frame_width), 
                                  height = int(1/5 * self.product_quality_frame_height))
        self.green_show.place(relx = 2/4,
                              rely = 2/5,
                              relwidth = 1/4, relheight = 1/5)
        self.green_show.tag_configure("center", justify='center', foreground="red", font=("Helvetica", 12, "bold"))
        self.green_show.insert(tk.END, "0")
        self.green_show.tag_add("center", "1.0", "end")
        self.green_show.configure(state="disabled")

        self.reset_green = ctk.CTkButton(self.product_quality_frame, text="RESET", fg_color="gray", command=self.reset2)
        self.reset_green.place(relx = 3/4,
                               rely = 2/5,
                               relwidth = 1/4, 
                               relheight = 1/5)
        
        self.integer_var3 = tk.StringVar()
        self.blue_entry = tk.Entry(self.product_quality_frame, textvariable=self.integer_var3)
        self.blue_entry.place(relx=1/4,
                               rely = 3/5, relwidth = 1/4, relheight = 1/5)

        self.blue_show = tk.Text(self.product_quality_frame, width = int(1/4 * self.button_frame_width), 
                                  height = int(1/5 * self.product_quality_frame_height))
        self.blue_show.place(relx = 2/4,
                              rely = 3/5,
                              relwidth = 1/4, relheight = 1/5)
        self.blue_show.tag_configure("center", justify='center', foreground="red", font=("Helvetica", 12, "bold"))
        self.blue_show.insert(tk.END, "0")
        self.blue_show.tag_add("center", "1.0", "end")
        self.blue_show.configure(state="disabled")

        self.blue_reset = ctk.CTkButton(self.product_quality_frame, text="RESET", fg_color="gray", command=self.reset3)
        self.blue_reset.place(relx = 3/4,
                               rely = 3/5,
                               relwidth = 1/4, 
                               relheight = 1/5)
        
        self.integer_var4 = tk.StringVar()
        self.NG_entry = tk.Entry(self.product_quality_frame, textvariable=self.integer_var4)
        self.NG_entry.place(relx = 1/4, 
                            rely = 4/5, relwidth = 1/4, relheight = 1/5)
        self.NG_show = tk.Text(self.product_quality_frame, width = int(1/4 * self.button_frame_width), 
                                  height = int(1/5 * self.product_quality_frame_height))
        self.NG_show.place(relx = 2/4,
                              rely = 4/5,
                              relwidth = 1/4, relheight = 1/5)
        self.NG_show.tag_configure("center", justify='center', foreground="red", font=("Helvetica", 12, "bold"))
        self.NG_show.insert(tk.END, "0")
        self.NG_show.tag_add("center", "1.0", "end")
        self.NG_show.configure(state="disabled")
        self.NG_reset = ctk.CTkButton(self.product_quality_frame, text="RESET", fg_color="gray", command=self.reset4)
        self.NG_reset.place(relx = 3/4,
                               rely = 4/5,
                               relwidth = 1/4, 
                               relheight = 1/5)

        # self.after(1000, self.update_red_show) 
        # self.after(1000, self.check_storage_limit_red)

    def frame_to_show_detected_object(self):
        self.detected_object_frame = ctk.CTkFrame(self.second_frame, fg_color=self.fg_color, 
                                                  border_width = 2,
                                                  border_color = "black", corner_radius = 10)
        self.detected_object_frame.place(relx= (8/12 * self.second_frame_width) / self.second_frame_width,
                        rely = 5/9,
                        relwidth = (4/12 * self.second_frame_width) / self.second_frame_width,
                        relheight = 4/9
                        )
        self.detected_object_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), uniform="a")
        self.detection_type = ctk.CTkLabel(self.detected_object_frame, 
                                       text = "No object detected", 
                                       text_color = "green", 
                                       font = ("Arial", 21),
                                       wraplength=4/12 * self.second_frame_width, 
                                       justify = "left")
        self.detection_type.grid(column = 0, row = 2, padx = 10, sticky = "nsew")
        self.saved_dir = ctk.CTkLabel(self.detected_object_frame, 
                                       text = "Saved image directory: None", 
                                       text_color = "green", 
                                       font = ("Arial", 21),
                                       wraplength=4/12 * self.second_frame_width - 20, 
                                       justify = "left")
        self.saved_dir.grid(column = 0, row = 3, rowspan = 3, sticky = "nsew", padx = 10)
        self.test = ctk.CTkLabel(self.detected_object_frame, 
                                       text = "Test", 
                                       text_color = "green", 
                                       font = ("Arial", 21),
                                       wraplength=4/12 * self.second_frame_width, 
                                       justify = "left")
        self.test.grid(column = 0, row = 6,padx = 10, sticky = "nsew")
        
    def reset1(self):
        pass

    def reset2(self):
        pass
        
    def reset3(self):
        pass
    
    def reset4(self):
        pass

    def clicked_start(self):
        pass
    
    def clicked_stop(self):
        pass