import cv2
from flask import Flask, Response

app = Flask(__name__)   # initialize the flask application, __name__ is passed to help flask determine the root path

def video_stream():
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        success, frame = camera.read()
        if not success:
            print("Error: Failed to capture frame.")
            break
        frame = cv2.flip(frame, 1)
        ret, buffer = cv2.imencode('.jpg', frame)    # encode the frame as jpeg images, buffer contains the encoded images
        if not ret:
            print("Error: Failed to encode frame.")
            break

        frame = buffer.tobytes()   # converts the encoded images to bytes
        yield (b'--frame\r\n'      # yields the images bytes in the format that is compatible to http responses, used for streaming videos
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()

# define a route in flask. When users navigate to the click, it will send to the video feed
# creates a http response that streams the video
# set up the mimetype used for server-push streams, where each frame is sent separately
@app.route('/')
def video_feed():   
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame') 

if __name__ == '__main__':
    app.run(debug=True)