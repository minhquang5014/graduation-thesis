from interface import create_window, second_frame, third_frame, fourth_frame
from interface import put_label_camera
import cv2
import customtkinter as ctk
import functools
from PLC.plc_connection import PLCConnection
from threading import Thread

color_dir = {
    "Peace puff": "#ffd7b5",
    "Sour green cherry": "#c8ffb5"
}

class MainWindow(create_window.BiggerWindow):
    def __init__(self, fg_color = "#ffd7b5", capture_index = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_value = 1
        self.fg_color = fg_color
        self.capture_index = capture_index
        self.connect_plc = PLCConnection(host = '192.168.0.1')
        self.connect_status = self.connect_plc.connectPLC()
        self.connect_plc.write(16, 1)
        
        print(self.connect_status)

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

        self.second.start_button.configure(command=self.custom_start)
        self.second.stop_button.configure(command=self.custom_stop)
        
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
    


    def on_enter_red(self, *arg):
        value1 = self.second.integer_var.get()
        if not value1.isdigit():
            self.second.integer_var.set(''.join(filter(str.isdigit, value1)))
    def on_enter_green(self, *arg):
        value2 = self.second.integer_var2.get()
        if not value2.isdigit():
            self.second.integer_var2.set(''.join(filter(str.isdigit, value2)))
    def on_enter_blue(self, *arg):
        value3 = self.second.integer_var3.get()
        if not value3.isdigit():
            self.second.integer_var3.set(''.join(filter(str.isdigit, value3)))
    def on_enter_NG(self):
        value4 = self.second.integer_var4.get()
        if not value4.isdigit():
            self.second.integer_var4.set(''.join(filter(str.isdigit, value4)))
    def exit_fullscreen(self, event):
        self.connect_plc.write(16, 0)
        self.capture.release()
        cv2.destroyAllWindows()
        self.root.destroy()

if __name__ == "__main__":
    # MainWindow(capture_index = "video/video_07332025_11h33m31s.avi")
    MainWindow(capture_index = 0)
    