"""import cv2
import mediapipe as mp
import time as tm
import handTrackingModule as HtModule

previous_time = 0
current_time = 0
video = cv2.VideoCapture(0) #open webcam
detector = HtModule.handDetector()

while True:
    trueYN, frame = video.read()
    frame = detector.findHands(frame)
    landmarkList = detector.findPosition(frame)
    #Please note that:
    #from left to right: x increases
    #from up  to down: y increases
    #so the leftmost value of x is 0 and the rightmost is  >= 600
    #for y, it would give you 0 from the top and slowly build its way to >= 600 to the bottom
    #it is a 640x40 image
    if len(landmarkList) != 0:
        if landmarkList[8]:
            print(landmarkList[8])
            
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


video.release()
cv2.destroyAllWindows()"""
 def divideZero(value1,value2):
        division = 0
        if value2 == 0:
              return None
        else:
            division = round(value1/value2,2)
            return division
    def logic_smirking():
        #distances and ratios then if statements
        distance_bottom_top_lip = getDistance(center_y_17,center_y_0)
        distance_left_right_cornerOflips = getDistance(center_y_61,center_y_291)
        
        distance_left_corner_lip_to_LeftCheek = getDistance(center_y_205,center_y_61)
        distance_right_corner_lip_to_RightCheek = getDistance(center_y_425,center_y_291)
  
        ratio_leftCornerLip_to_leftCheek = divideZero(distance_left_corner_lip_to_LeftCheek,distance_left_right_cornerOflips)
        ratio_rightCornerLip_to_RightCheek = divideZero(distance_right_corner_lip_to_RightCheek,distance_left_right_cornerOflips)

   
        if ratio_leftCornerLip_to_leftCheek is None or ratio_rightCornerLip_to_RightCheek is None:
            return None 
        elif ratio_leftCornerLip_to_leftCheek <= 5.00 and ratio_leftCornerLip_to_leftCheek >= 0:
            print("Smirking Left")
        elif ratio_leftCornerLip_to_leftCheek <= 0 and ratio_rightCornerLip_to_RightCheek >= -6.00:
            print("Smirking Right")
        else:
            print("Neutral")
        return()        








    Distance_center_to_up = getDistance(center_y_468,center_y_52)
    Distance_center_to_down = getDistance(center_y_152,center_y_468)
    ratioforYs = round(Distance_center_to_down/Distance_center_to_up,2)

    DistanceClose_Crash_Center_to_Down = getDistance(center_y_386,center_y_473)
    
    DistanceClose_Crash_Center_to_Down_LEFT = getDistance(center_y_145,center_y_468)

    Distance_center_to_left = getDistance(center_x_468,center_x_33)
    Distance_center_to_right = getDistance(center_x_133,center_x_468)
    ratio = round(Distance_center_to_left/Distance_center_to_right,2)

    
    #if DistanceClose_Crash_Center_to_Down <=1: #GoBackwards
        #print("Going Backwards")

    if ratioforYs >= 6.35: #Go Forward
        print("Looking Up")
        send_cmd("F")
    elif ratioforYs <= 5.00 and ratioforYs >= 4.20: #Go Backwards
        print("Looking Down")
        send_cmd("B"

     #run if and only if others are false

    elif ratio <= 0.60: #Strafe Left
        print("Looking Left")  
        send_cmd("SL")
    elif ratio > 1.25:
        print("looking right") #Strafe Right
        send_cmd("SR")
    #elif ratio > 0.65 and ratio < 1:
        #print("looking front") #Go Forward
        #send_cmd("U")
    else:
        send_cmd("X")
           