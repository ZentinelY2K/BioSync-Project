import cv2  #import openCV
import mediapipe as mp # import MediaPipe

#Get camera opened
brokenByEsc = False
brokenByFalse = False
frame = cv2.VideoCapture(0) # use '0' as default webcam
engineAI = mp.solutions.hands.Hands() #AI engine for hands
skeleton = mp.solutions.drawing_utils()
while True:
    boolean_readV, read_frame = frame.read() #returns two values that's why two variables
    turn_into_RGB = cv2.cvtColor(frame,cv2.COLOR_BRG2RGB)
    hand_obj_final = turn_into_RGB.process(frame)
    results = hand_obj_final
    if results == True:
        print("Hand detected")
    else:
        print("No hand detected")

    cv2.imshow("Test Window",read_frame)

    if cv2.waitKey(1) & 0xFF == ord('x'):
        brokenByEsc = True
        break
frame.release()
cv2.destroyAllWindows()
if brokenByEsc:
    print("Stopped by key 'x' ")
if brokenByFalse:
    print("Video Capture Failed")