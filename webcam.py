import cv2
import numpy as np
from white_and_black import detect_white_and_black
class OpenCVCapture:
    def __init__(self, camera_index=0, width=640, height=480):
        self.camera_index = camera_index
        self.width = width
        self.height = height

        # Define HSV ranges for black and white
        self.lower_black = np.array([0, 0, 0])
        self.upper_black = np.array([180, 255, 50])  # dark values

        self.lower_white = np.array([0, 0, 200])
        self.upper_white = np.array([180, 30, 255])  # bright values

        self.capture = cv2.VideoCapture(self.camera_index)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        self.video_loop()

    def video_loop(self, enable_detection=True):
        while True:
            ret, frame = self.capture.read()
            if not ret:
                print("Failed to capture image")
                break
            frame=cv2.flip(frame, 1)

            if (enable_detection==True):
                frame = detect_white_and_black(frame)
                
            # Show result
            cv2.imshow("Color Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.capture.release()
        cv2.destroyAllWindows()

# Run the camera
if __name__ == "__main__":
    OpenCVCapture()
