import cv2
import mediapipe as mp
import pyautogui

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks = True)
screen_w, screen_h = pyautogui.size()
roi = False

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
        print(x, y)
        cv2.circle(frame, (x, y), 6, (0, 255, 0))
        if not roi:
            roi = True
            xCrop = int(x - width/2)
            yCrop = int(y - height/2)
        # print(xCrop, yCrop)
        # Crop the frame
        cropped_frame = frame[yCrop:yCrop+height, xCrop:xCrop+width]
        resized = cv2.resize(cropped_frame, (640, 360))

        cv2.imshow('Cropped Frame', resized)
        if pyautogui.onScreen(x, y):
            pyautogui.moveTo(x, y)
        # for landmark in landmarks[0].landmark[474:478]:
            # x 
            # x = int(landmark.x * w )
            # y = int(landmark.y * h)
            # cv2.circle(frame, (x, y), 3, (0, 255, 0))
            # screen_x = x * 5
            # screen_y = y * 5
            # print(x, y)
            # print('break')
            # pyautogui.moveTo(screen_x, screen_y)

    cv2.imshow('face', frame)
    
    if cv2.waitKey(33) == ord('s'):
        cv2.destroyAllWindows()
        break
