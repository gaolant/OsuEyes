import cv2
import mediapipe as mp
import numpy as np
from tkinter import *

def buttonPress(bpos):
    pass

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks = True)
roi = False

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)

    landmarks = output.multi_face_landmarks
    h, w, _ = frame.shape
    width = 80
    height = 45
    
    if landmarks:
        points = landmarks[0].landmark[474:478]
        x = [landmark.x * w for landmark in points]
        y = [landmark.y * h for landmark in points]
        centroid = (sum(x) / len(points), sum(y) / len(points))
        x = int(centroid[0]) 
        y = int(centroid[1]) 
        if not roi:
            roi = True
            xCrop = int(x - width/2)
            yCrop = int(y - height/2)
        cropped_frame = frame[yCrop:yCrop+height, xCrop:xCrop+width]
        resized = cv2.resize(cropped_frame, (320, 180))

        cv2.imshow('Cropped Frame', resized)

    # Create a new window with dimensions 1920x1080
    window = np.zeros((1080, 1920, 3))

    c_t_l = (10, 10)

    # cv2.circle(window, c_t_l, 5, (255, 255, 255), -1)
    # cv2.createButton('button', buttonPress, None)
    # # Display the window
    # cv2.imshow('Calibration', window)

    #Create an instance of tkinter frame
    win= Tk()

    #Define the geometry of window
    win.geometry("1980x1080")     
    
    #Create a canvas object
    c = Canvas(win,width=400, height=400)
    c.pack()

    #Draw an Oval in the canvas
    c.create_oval(60,60,210,210)

    win.mainloop()

    if cv2.waitKey(33) == ord('s'):
        cv2.destroyAllWindows()
        break




