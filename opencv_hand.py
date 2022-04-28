import cv2
import time
import autopy
import numpy as np
import mediapipe as mp

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 10
detector = mp.solutions.hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,max_num_hands=1)
while True:
    success, img = cap.read()
    # detector.findHands()
    # lmList, bbox = detector.findPosition(img)
    # results = detector.process(img)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    if not success:
        continue
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)