import cv2
import mediapipe as mp
import pyautogui
from eyeCalibration import *

screen_w, screen_h = pyautogui.size()
x = calibration()

eyeWidth = x[2] - x[0]
eyeHeight = x[3] - x[1]

w_ratio = eyeWidth / 1980
h_ratio = eyeHeight / 1080



cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks = True)





while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)

    landmarks = output.multi_face_landmarks
    h, w, _ = frame.shape
    width = 160
    height = 90
    
    if landmarks:
        points = landmarks[0].landmark[474:478]
        x = [landmark.x * w for landmark in points]
        y = [landmark.y * h for landmark in points]
        centroid = (sum(x) / len(points), sum(y) / len(points))
        x = int(centroid[0]) 
        y = int(centroid[1]) 
        cv2.circle(frame, (x, y), 6, (0, 255, 0))

        calibratedX = int(x * w_ratio * 1280)
        calibratedY = int(y * h_ratio * 720)
        print(x,y)
        print(calibratedX, calibratedY)
        if pyautogui.onScreen(calibratedX, calibratedY):
            pyautogui.moveTo(calibratedX, calibratedY)

    cv2.imshow('face', frame)
    
    if cv2.waitKey(33) == ord('s'):
        cv2.destroyAllWindows()
        break