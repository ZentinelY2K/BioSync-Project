import cv2
import mediapipe as mp
import time as tm
x = cv2.VideoCapture(0)
video = cv2.flip(1,x)#open webcam
mpHands = mp.solutions.hands
hands = mpHands.Hands() #static,maxnumHands,minDetectionConf,etc
mpDraw = mp.solutions.drawing_utils #this draws the 21 landmarks
previous_time = 0
current_time = 0
while True:
    trueYN, frame = video.read() #read frames and get boolean
    frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) #class hands only uses RGB (red,green,blue) images 
    results = hands.process(frameRGB) #processes the frame and throws it back
    #print(results.multi_hand_landmarks) #detects if anything is there
    if results.multi_hand_landmarks: #results is the processed RGB
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark): #here id is the ettiquete itself and lm is the landmark we're getting
                #from 'handsLms.landmark', enumerate is used to sort them in order, for loop to go through each one
                #each id returns x,y,z 
                #sheer,raw values before turned into pixels are the image ratio (it might see like -6.40244)
                #if we multiply by the width and height we get the pixel value
                #for each hand landmark get the information from it
                height,width,channels = frame.shape #get height,width, and channels from the frame shape
                center_x,center_y = int(lm.x*width), int(lm.y*height) #here we will multiply the landmark by the width and height but separate the variables
                print(id,center_x,center_y) #print id,x, and y pixel values
                if id == 8 and center_x >=350: #id certain landmark is certain landmark then:
                    cv2.circle(frame,(center_x,center_y),15,(255,0,0),cv2.FILLED) #this draws a circle for that landmark, which matches
                    #its pixel value, then, comes '25' which is the size and BGR color, then we fill it
            mpDraw.draw_landmarks(frame,handLms,mpHands.HAND_CONNECTIONS) #mpDraw can accept lots of parameters, in this case
            #handLms is a single hand, in this case, it is hand 0 in our frame, then mpHands.HAND_CONNECTIONS uses the mpHands module to draw connections across limbs



    current_time  = tm.time()
    fps = 1/(current_time-previous_time)    
    previous_time = current_time
    
    cv2.putText(frame,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),3) 
    #cv2.putText(frame,"Axel!",(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),3) My name
    #here the first argument to the parameters is 'frame' (a.k.a our actual video) then we cast the fps (int) to a string
    #since we are displaying text, then we give it (10,70) which is out x,y and then cv2.font is the font and then 3 is the
    #thickness, then (BGR) is blue, red, green (in this case the combination is purple) then 3 is the scale at the end


    cv2.imshow("Webcam",frame) #name webcam window 'n show frame
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break
cv2.release()
cv2.destroyAllWindows()
    
