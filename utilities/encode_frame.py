import cv2

def encode_frame(frame):
    """
    Encodes a frame to JPEG format and returns the byte data.
    """
    ret, buffer = cv2.imencode('.jpg', frame)
    if not ret:
        return None
    return buffer.tobytes()