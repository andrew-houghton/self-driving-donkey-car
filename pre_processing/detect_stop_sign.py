import cv2
import os
import numpy as np
from matplotlib import pyplot as plt
import time

video_capture = cv2.VideoCapture(0)

def detect_stop_sign(image):
    stop_sign_cascade = cv2.CascadeClassifier('draft_model.xml')  #I need another 4 hours to train a 10-stage classifier
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    signs = stop_sign_cascade.detectMultiScale(gray, 1.1, 5)
    if signs != None :
        return True

    return False

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read() #replace this funtion with the one which can retrieve frame from picamera
    # Draw a rectangle around the faces
    frame = detect_stop_sign(frame)
    # Display the resulting frame
    imgplot = plt.imshow(frame, cmap='gray')
    # use for debugging
    # plt.ion()
    # plt.draw()
    # plt.show()
    time.sleep(0.01)
