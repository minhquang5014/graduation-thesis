import cv2
import numpy as np

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

    def video_loop(self):
        while True:
            ret, frame = self.capture.read()
            if not ret:
                print("Failed to capture image")
                break

            frame = cv2.flip(frame, 1)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            masks = [
                (cv2.inRange(hsv, self.lower_black, self.upper_black),"Black Object", (0, 0, 0)),
                (cv2.inRange(hsv, self.lower_white, self.upper_white), "White Object", (0, 0, 200))
            ]

            for mask, label, color in masks:
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    if cv2.contourArea(contour) > 3000:
                        x, y, w, h = cv2.boundingRect(contour)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)  # Draw rectangle
                        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                        break

            # Find contours for black
            # contours_black, _ = cv2.findContours(mask_black, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # for contour in contours_black:
            #     area = cv2.contourArea(contour)
            #     if area > 1500:
            #         x, y, w, h = cv2.boundingRect(contour)
            #         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)
            #         cv2.putText(frame, "Black Object", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

            # Find contours for white
            # contours_white, _ = cv2.findContours(mask_white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # for contour in contours_white:
            #     area = cv2.contourArea(contour)
            #     if area > 1500:
            #         x, y, w, h = cv2.boundingRect(contour)
            #         cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
            #         cv2.putText(frame, "White Object", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            # Show result
            cv2.imshow("Color Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.capture.release()
        cv2.destroyAllWindows()

# Run the camera
if __name__ == "__main__":
    OpenCVCapture()
