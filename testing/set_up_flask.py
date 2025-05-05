from flask import Flask, Response, render_template
from webcam.webcam import OpenCVCapture

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML layout

@app.route('/video_feed')
def video_feed():
    webcam = OpenCVCapture(camera_index=0, width=640, height=480)
    return Response(webcam.video_loop(enable_detection=True, enable_flask=True), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()