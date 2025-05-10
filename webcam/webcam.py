import cv2
import numpy as np
from webcam.white_and_black import detect_white_and_black
from utilities.encode_frame import encode_frame
from webcam.exit_webcam import exit_webcam
class OpenCVCapture:
    def __init__(self, camera_index=0, width=640, height=480):
        self.camera_index = camera_index
        self.width = width
        self.height = height

        self.capture = cv2.VideoCapture(self.camera_index)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def video_loop(self, enable_detection=True, enable_flask=False):
        if enable_flask:
            return self.flask_stream(enable_detection)
        else:
            try:
                while True:
                    ret, frame = self.capture.read()
                    if not ret:
                        print("Failed to grab frame")
                        break
                    frame = cv2.flip(frame, 1)

                    if enable_detection:
                        frame = detect_white_and_black(frame)

                    cv2.imshow("Color Detection", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            except Exception as e:
                print(f"Error: {e}")
            finally:
                exit_webcam(self.capture)

    def flask_stream(self, enable_detection=True):
        while True:
            ret, frame = self.capture.read()
            if not ret:
                print("Failed to grab frame")
                break
            frame = cv2.flip(frame, 1)

            if enable_detection:
                frame = detect_white_and_black(frame)
            frame = encode_frame(frame)
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        exit_webcam(self.capture)
