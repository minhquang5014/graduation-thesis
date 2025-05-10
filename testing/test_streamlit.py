import streamlit as st
import cv2
from PIL import Image
import time

st.title("Quick Webcam Stream")

# OpenCV video capture
cap = cv2.VideoCapture(0)

frame_placeholder = st.empty()

# Loop through frames
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to RGB
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Show the frame in Streamlit
    frame_placeholder.image(frame, channels="RGB")

    # Optional sleep to control frame rate
    time.sleep(0.03)

cap.release()
