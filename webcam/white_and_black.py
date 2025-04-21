import numpy as np
import cv2

lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 50])  # dark values
lower_white = np.array([0, 0, 200])
upper_white = np.array([180, 30, 255])  # bright values

def detect_white_and_black(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    masks = [
        (cv2.inRange(hsv, lower_black, upper_black),"Black Object", (0, 0, 0)),
        (cv2.inRange(hsv, lower_white, upper_white), "White Object", (255, 255, 255))
    ]

    for mask, label, color in masks:
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) > 3000:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)  # Draw rectangle
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return frame