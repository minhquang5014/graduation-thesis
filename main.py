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
        self.fg_color = fg_color
        self.capture_index = capture_index
        self.connect_plc = PLCConnection(host = '192.168.0.1')
        self.connect_status = self.connect_plc.connectPLC()
        print(self.connect_status)
        self.video_label, self.label_width, self.label_height = put_label_camera.label_to_put_video(
                self.frame,
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
        self.second.start_button.configure(command=self.custom_start)
        self.second.stop_button.configure(command=self.custom_stop)

        self.third = third_frame.ThirdFrame(
            screen_width=self.screen_width, 
            video_frame_width=self.label_width, 
            screen_height=self.screen_height, 
            video_frame_height=self.label_height,
            fg_color = self.fg_color
        )
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
                resized_height=self.label_height
            )
        
        Thread(target = self.connect_plc.connectPLC, daemon=True).start()
        # Thread(target = self.custom_start, daemon=True).start()
        # Thread(target = self.custom_stop, daemon=True).start()
        # Thread(target = self.custom_auto_manual_switch, daemon=True).start()

        # press Esp to exit
        self.root.bind('<Escape>', self.exit_fullscreen)
        self.root.mainloop()

    def custom_start(self):
        self.fourth.insert_textbox(message="Pressing start. The program is now running")
        self.connect_plc.write(3, 1)

    def custom_stop(self):
        self.fourth.insert_textbox(message="Pressing stop. Stops the program now")
        self.connect_plc.write(4, 1)

    def custom_auto_manual_switch(self):
        if self.auto_manual_switch.get() == 1:
            self.connect_plc.write(7, 1)
            self.fourth.insert_textbox(message="Switching to manual mode now")
        else:
            self.connect_plc.write(7, 0)
            self.fourth.insert_textbox(message="Switching back to auto mode")
            
    def exit_fullscreen(self, event):
        self.capture.release()
        cv2.destroyAllWindows()
        self.root.destroy()

if __name__ == "__main__":
    MainWindow()
    