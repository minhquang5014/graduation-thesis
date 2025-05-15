from interface import create_window, second_frame, third_frame, fourth_frame
from interface import put_label_camera
import cv2
import customtkinter as ctk
import functools
color_dir = {
    "Peace puff": "#ffd7b5",
    "Sour green cherry": "#c8ffb5"
}

class MainWindow(create_window.FullscreenWindow):
    def __init__(self, fg_color = "#ffd7b5", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fg_color = fg_color
        self.video_label, self.label_width, self.label_height = put_label_camera.label_to_put_video(
                self.frame,
                screen_width=self.screen_width,
                screen_height=self.screen_height,
                fixed_video_label=True
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
        def custom_start():
            print("START button clicked (overridden)")
            # You can put custom logic here...
        self.second.start_button.configure(command=custom_start)

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
        self.capture = cv2.VideoCapture(0)
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

        # press Esp to exit
        self.root.bind('<Escape>', self.exit_fullscreen)
        self.root.mainloop()

    def exit_fullscreen(self, event):
        self.capture.release()
        cv2.destroyAllWindows()
        self.root.destroy()

if __name__ == "__main__":
    MainWindow()
    