from interface import create_window, second_frame, third_frame, fourth_frame
from interface import put_label_camera
import cv2
import functools
from PLC.plc_connection import PLCConnection
from threading import Thread
import tkinter as tk
import customtkinter as ctk
import numpy as np

color_dir = {
    "Peace puff": "#ffd7b5",
    "Sour green cherry": "#c8ffb5"
}

DEFAULT_NUMBER_OBJ = 10

class MainWindow(create_window.BiggerWindow):
    def __init__(self, fg_color = "#ffd7b5", capture_index = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_value = 1
        self.fg_color = fg_color
        self.capture_index = capture_index

        self.lower_red = np.array([0, 100, 100])
        self.upper_red = np.array([12, 255, 255])
        self.lower_green = np.array([30, 100, 100])
        self.upper_green = np.array([92, 255, 255])
        self.lower_blue = np.array([95, 120, 120])
        self.upper_blue = np.array([130, 255, 255])

        self.connect_plc = PLCConnection(host = '192.168.0.1')
        self.connect_status = self.connect_plc.connectPLC()
        self.connect_plc.write(16, 1)

        # first frame to put the label video
        self.video_label, self.label_width, self.label_height = put_label_camera.label_to_put_video(
                self.root,
                screen_width=self.screen_width,
                screen_height=self.screen_height,
                fixed_video_label=False
                )
        
        # call the Frame object
        self.second = second_frame.SecondFrame(
            screen_width=self.screen_width, 
            video_frame_width=self.label_width, 
            screen_height=self.screen_height, 
            video_frame_height=self.label_height, 
            fixed_button_size = False,
            fg_color = self.fg_color
        )
        self.second.red_entry.bind('<Return>', self.on_enter_red)
        self.second.green_entry.bind('<Return>', self.on_enter_green)
        self.second.blue_entry.bind('<Return>', self.on_enter_blue)
        self.second.NG_entry.bind('<Return>', self.on_enter_NG)

        self.trace_id = self.second.integer_var.trace_add('write', self.validate_integer_red)
        self.trace_id2 = self.second.integer_var2.trace_add('write', self.validate_integer_green)
        self.trace_id3 = self.second.integer_var3.trace_add('write', self.validate_integer_blue)
        self.trace_id4 = self.second.integer_var4.trace_add('write', self.validate_integer_NG)

        self.second.start_button.configure(command=self.custom_start)
        self.second.stop_button.configure(command=self.custom_stop)

        # override the reset button commands on the second frame
        self.second.red_reset.configure(command=self.reset1)
        self.second.reset_green.configure(command=self.reset2)
        self.second.blue_reset.configure(command=self.reset3)
        self.second.NG_reset.configure(command=self.reset4)


        self.root.after(1000, self.check_storage_limit_red)
        self.root.after(1000, self.check_storage_limit_green)
        self.root.after(1000, self.check_storage_limit_blue)
        self.root.after(1000, self.check_storage_limit_NG)

        self.root.after(400, self.read_start_stop_lights)

        self.third = third_frame.ThirdFrame(
            screen_width=self.screen_width, 
            video_frame_width=self.label_width, 
            screen_height=self.screen_height, 
            video_frame_height=self.label_height,
            fg_color = self.fg_color
        )
        self.root.after(400, self.read_initial_light1)
        self.root.after(400, self.read_initial_light2)
        self.root.after(400, self.read_initial_light3)
        self.root.after(400, self.read_initial_light4)

        self.fourth = fourth_frame.FourthFrame(
            screen_width=self.screen_width, 
            video_frame_width=self.label_width, 
            screen_height=self.screen_height, 
            video_frame_height=self.label_height, 
            fg_color = self.fg_color
        )
        if self.connect_status is False:
            self.fourth.insert_textbox(message="Failed to connect to PLC, please check connection")
        else:
            self.fourth.insert_textbox(message="Connected PLC successfully")
        self.auto_manual_switch = self.fourth.switch
        self.auto_manual_switch.configure(command = self.custom_auto_manual_switch)

        self.capture = cv2.VideoCapture(capture_index)
        ret, frame = self.capture.read()
        if not self.capture.isOpened() or not ret or frame is None:
            self.fourth.insert_textbox(message="Unable to access camera. Please check your camera")
        else:
            put_label_camera.update_frame(
                self.capture,
                self.video_label,
                self.root,
                resized_width=self.label_width,
                resized_height=self.label_height,
                write=self.connect_plc.write,
                enable_detection=True
            )

        Thread(target = self.connect_plc.connectPLC, daemon=True).start()
        # Thread(target = self.custom_start, daemon=True).start()
        # Thread(target = self.custom_stop, daemon=True).start()
        # Thread(target = self.custom_auto_manual_switch, daemon=True).start()

        # press Esp to exit
        self.root.bind('<Escape>', self.exit_fullscreen)
        self.root.mainloop()

    def read_initial_light1(self):  # read state of the conveyor belt
        result_light1 = self.connect_plc.read(9)
        if result_light1 == 0:
            self.third.canvas1_obj.itemconfig(self.third.canvas_light1, fill="gray")
        else:
            self.third.canvas1_obj.itemconfig(self.third.canvas_light1, fill="green")
        self.root.after(200, self.read_initial_light1)
    def read_initial_light2(self):
        result_light2 = self.connect_plc.read(10)
        if result_light2 == 0:
            self.third.canvas2_obj.itemconfig(self.third.canvas_light2, fill = "gray")
        else:
            self.third.canvas2_obj.itemconfig(self.third.canvas_light2, fill="green")
    def read_initial_light3(self):
        result_light3 = self.connect_plc.read(11)
        if result_light3 == 0:
            self.third.canvas3_obj.itemconfig(self.third.canvas_light3, fill = "gray")
        else:
            self.third.canvas3_obj.itemconfig(self.third.canvas_light3, fill="green")
    def read_initial_light4(self):
        result_light4 = self.connect_plc.read(12)
        if result_light4 == 0:
            self.third.canvas4_obj.itemconfig(self.third.canvas_light4, fill = "gray")
        else:
            self.third.canvas4_obj.itemconfig(self.third.canvas_light4, fill="green")

    def custom_start(self):
        self.fourth.insert_textbox(message="Pressing start. The program is now running, sending int to h_reg 3")
        self.connect_plc.write(4, 1)
        self.connect_plc.write(5, 0)
        self.root.after(400, self.reset_start_stop_button)
        
    def custom_stop(self):
        self.fourth.insert_textbox(message="Pressing stop. Stops the program now, sending int to h_reg 4")
        self.connect_plc.write(5, 1)
        self.connect_plc.write(4, 0)
        self.root.after(400, self.reset_start_stop_button)

    def reset_start_stop_button(self):
        self.connect_plc.write(4, 0)
        self.connect_plc.write(5, 0)
        self.read_start_stop_lights()
    def read_start_stop_lights(self):
        initial_start_state = self.connect_plc.read(6)
        initial_stop_state = self.connect_plc.read(7)
        self.update_lights(initial_start_state, initial_stop_state)

    def update_lights(self, state1, state2):
        if state1 == 1:
            self.second.lights_canvas_start.itemconfig(self.second.oval_start, fill = "green")
        else:
            self.second.lights_canvas_start.itemconfig(self.second.oval_start, fill = "gray")
        if state2 == 1:
            self.second.lights_canvas_stop.itemconfig(self.second.oval_stop, fill = "red")
        else:
            self.second.lights_canvas_stop.itemconfig(self.second.oval_stop, fill = "gray")

    def custom_auto_manual_switch(self):
        if self.auto_manual_switch.get() == 1:
            self.connect_plc.write(8, 1)
            self.fourth.insert_textbox(message="Switching to manual mode now")
        else:
            self.connect_plc.write(8, 0)
            self.fourth.insert_textbox(message="Switching back to auto mode")
    
    
    # check if the input value is a integer
    def on_enter_red(self, *arg):
        value1 = self.second.integer_var.get()
        if not value1.isdigit():
            self.second.integer_var.set(''.join(filter(str.isdigit, value1)))
    def validate_integer_red(self, *args):   
        value = self.second.integer_var.get()
        if value.isdigit() and int(value) > DEFAULT_NUMBER_OBJ:   
            self.fourth.insert_textbox(f"You have entered {value} so {value} red objects will be in process")
            self.connect_plc.write(17, int(value))
        elif value.isdigit() and int(value) <= DEFAULT_NUMBER_OBJ:
            self.fourth.insert_textbox(f"By default, {DEFAULT_NUMBER_OBJ} objects will be in the process of classification")
            self.connect_plc.write(17, DEFAULT_NUMBER_OBJ)
        else:
            self.fourth.insert_textbox("Invalid Input, only integers are allowed")
    def reset1(self):
        self.connect_plc.write(21, 1)
        self.root.after(400, lambda: self.connect_plc.write(21, 0))
        self.connect_plc.write(17, DEFAULT_NUMBER_OBJ)
        self.second.red_show.configure(state=tk.NORMAL)
        self.second.red_show.delete("1.0", tk.END)
        self.second.red_show.insert(tk.END, "0")
        self.second.red_show.tag_add("center", "1.0", "end")
        self.second.red_show.configure(state=tk.DISABLED)
        self.second.integer_var.trace_remove("write", self.trace_id)
        self.second.integer_var.set("")
        self.trace_id = self.second.integer_var.trace_add("write", self.validate_integer_red)
        self.fourth.insert_textbox(f"Reset red object counter, will start counting again. By default, {DEFAULT_NUMBER_OBJ} objects will be in process")
    def check_storage_limit_red(self):
        try:
            # get the input value
            limit = int(self.second.integer_var.get())
        except ValueError:
            limit = DEFAULT_NUMBER_OBJ
        storage_red = self.connect_plc.read(30)
        if storage_red == 1:
            self.fourth.insert_textbox("The storage for red is full")
        else:
            if limit > DEFAULT_NUMBER_OBJ:
                self.fourth.insert_textbox(f"You have entered {limit} for red storage, so {limit} objects will be in process of classification")
        self.root.after(1000, self.check_storage_limit_red)


    def on_enter_green(self, *arg):
        value2 = self.second.integer_var2.get()
        if not value2.isdigit():
            self.second.integer_var2.set(''.join(filter(str.isdigit, value2)))
    def validate_integer_green(self, *args):
        value = self.second.integer_var2.get()
        if value.isdigit() and int(value) > DEFAULT_NUMBER_OBJ:   
            self.fourth.insert_textbox(f"You have entered {value} so {value} green objects will be in process")
            self.connect_plc.write(18, int(value))
        elif value.isdigit() and int(value) <= DEFAULT_NUMBER_OBJ:
            self.fourth.insert_textbox(f"By default, {DEFAULT_NUMBER_OBJ} objects will be in the process of classification")
            self.connect_plc.write(18, DEFAULT_NUMBER_OBJ)
        else:
            self.fourth.insert_textbox("Invalid Input, only integers are allowed")
    def reset2(self):
        self.connect_plc.write(22, 1)
        self.root.after(400, lambda: self.connect_plc.write(22, 0))
        self.connect_plc.write(18, DEFAULT_NUMBER_OBJ)
        self.second.green_show.configure(state=tk.NORMAL)
        self.second.green_show.delete("1.0", tk.END)
        self.second.green_show.insert(tk.END, "0")
        self.second.green_show.tag_add("center", "1.0", "end")
        self.second.green_show.configure(state=tk.DISABLED)
        
        self.second.integer_var2.trace_remove("write", self.trace_id2)
        self.second.integer_var2.set("")
        self.trace_id2 = self.second.integer_var2.trace_add("write", self.validate_integer_green)
        self.fourth.insert_textbox(f"Reset green object counter, will start counting again. By default, {DEFAULT_NUMBER_OBJ} objects will be in process")
    def check_storage_limit_green(self):
        try:
            # get the input value
            limit = int(self.second.integer_var2.get())
        except ValueError:
            limit = DEFAULT_NUMBER_OBJ
        storage_green = self.connect_plc.read(31)
        if storage_green == 1:
            self.fourth.insert_textbox("The storage for green is full")
        else:
            if limit > DEFAULT_NUMBER_OBJ:
                self.fourth.insert_textbox(f"You have entered {limit} for green storage, so {limit} objects will be in process of classification")
        self.root.after(1000, self.check_storage_limit_green)


    def on_enter_blue(self, *arg):
        value3 = self.second.integer_var3.get()
        if not value3.isdigit():
            self.second.integer_var3.set(''.join(filter(str.isdigit, value3)))
    def validate_integer_blue(self, *args):
        value = self.second.integer_var3.get()
        if value.isdigit() and int(value) > DEFAULT_NUMBER_OBJ:   
            self.fourth.insert_textbox(f"You have entered {value} so {value} blue objects will be in process")
            self.connect_plc.write(19, int(value))
        elif value.isdigit() and int(value) <= DEFAULT_NUMBER_OBJ:
            self.fourth.insert_textbox(f"By default, {DEFAULT_NUMBER_OBJ} objects will be in the process of classification")
            self.connect_plc.write(19, DEFAULT_NUMBER_OBJ)
        else:
            self.fourth.insert_textbox("Invalid Input, only integers are allowed")
    def reset3(self):
        self.connect_plc.write(23, 1)
        self.root.after(400, lambda: self.connect_plc.write(23, 0))
        self.connect_plc.write(19, DEFAULT_NUMBER_OBJ)
        self.second.blue_show.configure(state=tk.NORMAL)
        self.second.blue_show.delete("1.0", tk.END)
        self.second.blue_show.insert(tk.END, "0")
        self.second.blue_show.tag_add("center", "1.0", "end")
        self.second.blue_show.configure(state=tk.DISABLED)
        
        self.second.integer_var3.trace_remove("write", self.trace_id3)
        self.second.integer_var3.set("")
        self.trace_id3 = self.second.integer_var3.trace_add("write", self.validate_integer_blue)
        self.fourth.insert_textbox(f"Reset blue object counter, will start counting again. By default, {DEFAULT_NUMBER_OBJ} objects will be in process")
    def check_storage_limit_blue(self):
        try:
            # get the input value
            limit = int(self.second.integer_var3.get())
        except ValueError:
            limit = DEFAULT_NUMBER_OBJ
        storage_blue = self.connect_plc.read(32)
        if storage_blue == 1:
            self.fourth.insert_textbox("The storage for blue is full")
        else:
            if limit > DEFAULT_NUMBER_OBJ:
                self.fourth.insert_textbox(f"You have entered {limit} for blue storage, so {limit} objects will be in process of classification")
        self.root.after(1000, self.check_storage_limit_blue)


    def on_enter_NG(self):
        value4 = self.second.integer_var4.get()
        if not value4.isdigit():
            self.second.integer_var4.set(''.join(filter(str.isdigit, value4)))
    def validate_integer_NG(self, *args):
        value = self.second.integer_var4.get()
        if value.isdigit() and int(value) > DEFAULT_NUMBER_OBJ:   
            self.fourth.insert_textbox(f"You have entered {value} so {value} NG objects will be in process")
            self.connect_plc.write(20, int(value))
        elif value.isdigit() and int(value) <= DEFAULT_NUMBER_OBJ:
            self.fourth.insert_textbox(f"By default, {DEFAULT_NUMBER_OBJ} objects will be in the process of classification")
            self.connect_plc.write(20, DEFAULT_NUMBER_OBJ)
        else:
            self.fourth.insert_textbox("Invalid Input, only integers are allowed")
    def reset4(self):
        self.connect_plc.write(24, 1)
        self.root.after(400, lambda: self.connect_plc.write(24, 0))
        self.connect_plc.write(20, DEFAULT_NUMBER_OBJ)
        self.second.NG_show.configure(state=tk.NORMAL)
        self.second.NG_show.delete("1.0", tk.END)
        self.second.NG_show.insert(tk.END, "0")
        self.second.NG_show.tag_add("center", "1.0", "end")
        self.second.NG_show.configure(state=tk.DISABLED)
        self.second.integer_var4.trace_remove("write", self.trace_id4)
        self.second.integer_var4.set("")
        self.trace_id4 = self.second.integer_var4.trace_add("write", self.validate_integer_NG)
        self.fourth.insert_textbox(f"Reset NG object counter, will start counting again. By default, {DEFAULT_NUMBER_OBJ} objects will be in process")
    def check_storage_limit_NG(self):
        try:
            # get the input value
            limit = int(self.second.integer_var4.get())
        except ValueError:
            limit = DEFAULT_NUMBER_OBJ
        storage_NG = self.connect_plc.read(33)
        if storage_NG == 1:
            self.fourth.insert_textbox("The storage for NG is full")
        else:
            if limit > DEFAULT_NUMBER_OBJ:
                self.fourth.insert_textbox(f"You have entered {limit} for NG storage, so {limit} objects will be in process of classification")
        self.root.after(1000, self.check_storage_limit_NG)


    def exit_fullscreen(self, event):
        self.connect_plc.write(16, 0)
        self.capture.release()
        cv2.destroyAllWindows()
        self.root.destroy()

if __name__ == "__main__":
    # MainWindow(capture_index = "video/video_07332025_11h33m31s.avi")
    MainWindow(capture_index = 0)
    