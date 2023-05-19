import cv2
import mediapipe as mp
import numpy as np
from tkinter import *
from time import *

eyePoses = {}
endCalibration = False


def startPress():
    eyePoses['center'] = (x,y)
    calStart = Label(win, text='Press the appearing buttons in order (your eye should lie in the eyebox)', font="Helvetica")
    calStart.place(relx = 0.5, rely = 0.5, anchor = 'center')
    button1()

def button1():
    sleep(0.3)
    cal1 = Button(win, text='1', command=button2)
    cal1.place(relx = 0.01, rely = 0.02)

def button2():
    eyePoses['top-left'] = (x,y)
    sleep(0.3)
    cal2 = Button(win, text='2', command=button3)
    cal2.place(relx = 0.5, rely = 0.02)

def button3():
    eyePoses['top-mid'] = (x,y)
    sleep(0.3)
    cal3 = Button(win, text='3', command=button4)
    cal3.place(relx = 0.95, rely = 0.02)

def button4():
    eyePoses['top-right'] = (x,y)
    sleep(0.3)
    cal4 = Button(win, text='4', command=button5)
    cal4.place(relx = 0.01, rely = 0.5)

def button5():
    eyePoses['mid-left'] = (x,y)
    sleep(0.3)
    cal5 = Button(win, text='5', command=button6)
    cal5.place(relx = 0.95, rely = 0.5)

def button6():
    eyePoses['mid-right'] = (x,y)
    sleep(0.3)
    cal6 = Button(win, text='6', command=button7)
    cal6.place(relx = 0.01, rely = 0.9)

def button7():
    eyePoses['bot-left'] = (x,y)
    sleep(0.3)
    cal7 = Button(win, text='7', command=button8)
    cal7.place(relx = 0.5, rely = 0.9)

def button8():
    eyePoses['bot-mid'] = (x,y)
    sleep(0.3)
    cal8 = Button(win, text='8', command=button9)
    cal8.place(relx = 0.95, rely = 0.9)

def button9():
    global endCalibration 

    eyePoses['bot-right'] = (x,y)
    print('Calibration success!')
    print(eyePoses)
    win.destroy()
    endCalibration = True
        


        
#Create an instance of tkinter frame
win= Tk()

#Define the geometry of window
win.geometry("1980x1080")     
start = Button(win, text="Start Calibration", command=startPress)
start.place(relx = 0.5, rely = 0.5, anchor = 'center')


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

        cv2.imshow('EyeBox', resized)



    if cv2.waitKey(33) == ord('s') or endCalibration == True:
        cv2.destroyAllWindows()
        break

    win.update()

