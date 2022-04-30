import cv2
import mediapipe as mp
import time
import autopy
import numpy as np

# todo
# close the terminal/exit() when a fist is made
# clicking based on the point gesture

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
wScreen, hScreen = autopy.screen.size()
print(wScreen, hScreen)
frameR = 200
pTime = 10
sleepLimit = 60


cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,max_num_hands=1) as hands:
  while cap.isOpened():
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    success, image = cap.read()
    time.sleep(1/sleepLimit)# hack to set the frame rate
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    # image = cv2.resize(image,(0, 0), fx=0.5, fy=0.5)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imageHeight, imageWidth, _ = image.shape
    
    results = hands.process(image)
    # To limit the boundaries in order to improve the mouse pointer consistency
    cv2.rectangle(image, (frameR,frameR),(1280-frameR,720-frameR),(255,255,0),2)
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        if hand_landmarks.landmark[8] is None:
            continue
        # first
        normalizedLandmark = hand_landmarks.landmark[8]# first Tip of the pointer value
        pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)
        # second tip of pointer value
        normalizedLandmark2 = hand_landmarks.landmark[12]
        pixelCoordinatesLandmark2 = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark2.x, normalizedLandmark2.y, imageWidth, imageHeight)
        
        
        
        # # debug the pointer tip coordinates
        # print("pixel coordinate tip: ",pixelCoordinatesLandmark,"pixel coordinate second: ", pixelCoordinatesLandmark2,end="\r")
        
        # converting the tip coordinates to mouse position
        try:
            mouseX = np.interp(pixelCoordinatesLandmark[0], (frameR,1280-frameR),(0,wScreen))
            mouseY = np.interp(pixelCoordinatesLandmark[1],(frameR,720-frameR),(0,hScreen))
            # print(mouseX,mouseY,end="\r")
            # moving the mouse
            autopy.mouse.move(wScreen - mouseX, mouseY)
            print("mouse tracking is working correctly         ",end="\r")
            # cv2.circle(image,(pixelCoordinatesLandmark[0],pixelCoordinatesLandmark[1]),15,(255,0,255),cv2.FILLED)
            # print(pixelCoordinatesLandmark)
        except TypeError:
            print("point is out of the screen             ",end="\r")
        except ValueError:
            print("point is out of bounds                  ",end="\r")

        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
 
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Flip the image horizontally for a selfie-view display.
    image = cv2.resize(image,(0, 0),fx=0.5, fy=0.5)
    image = cv2.flip(image, 1)
    cv2.putText(image, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,0), 3)
    # cv2.imshow('MediaPipe Hands', image)

    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()