from interface import create_window, second_frame
from interface import put_label_camera
import cv2
import customtkinter as ctk
class MainWindow(create_window.CreateWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.capture = cv2.VideoCapture(0)
            self.video_label, self.label_width, self.label_height = put_label_camera.label_to_put_video(
                self.frame,
                screen_width=self.screen_width,
                screen_height=self.screen_height
                )
            put_label_camera.update_frame(self.capture, self.video_label, self.root)
        except Exception as e:
            print(e)
        second_frame.SecondFrame(
            screen_width=self.screen_width, 
            video_frame_width=self.label_width, 
            screen_height=self.screen_height, 
            video_frame_height=self.label_height
        )
        self.root.bind('<Escape>', self.exit_fullscreen)
        self.root.mainloop()
    def exit_fullscreen(self, event):
        self.capture.release()
        cv2.destroyAllWindows()
        self.root.destroy()

if __name__ == "__main__":
    MainWindow()