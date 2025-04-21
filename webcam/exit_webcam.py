import cv2

def exit_webcam(capture):
    capture.release()
    cv2.destroyAllWindows()