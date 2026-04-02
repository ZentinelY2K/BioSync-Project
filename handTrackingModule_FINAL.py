import cv2
import mediapipe as mp
import socket #for communication with Arduino IDE
import time as tm #for delay
import math as mt
import json as js #import json to send dictionaries over to Arduino


ESP32_IP = "10.253.27.157" #my ip

Port = 4210

#UDP socke
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


class handDetector():   
    def __init__(self, mode=False, maxHands = 2, model_complexity = 1, detectionConf = 0.5, trackConf = 0.5): #same parameters discussed
    #the follorwing are self declared variables for each method that the user can manipulate
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity = model_complexity
        self.detectionConf = detectionConf
        self.trackConf = trackConf

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.model_complexity,self.detectionConf,self.trackConf) #static,maxnumHands,minDetectionConf,etc
        self.mpDraw = mp.solutions.drawing_utils #this draws the 21 landmarks

    def findHands(self,flipCam,draw = True):
        #read flipCams and get boolean
        flipCamRGB = cv2.cvtColor(flipCam,cv2.COLOR_BGR2RGB) #class hands only uses RGB (red,green,blue) images 
        self.results = self.hands.process(flipCamRGB) #processes the flipCam and throws it back
        #print(results.multi_hand_landmarks) #detects if anything is there
        if self.results.multi_hand_landmarks: #results is the processed RGB
           for handLms in self.results.multi_hand_landmarks:
              if draw:
                self.mpDraw.draw_landmarks(flipCam,handLms,self.mpHands.HAND_CONNECTIONS) #mpDraw can accept lots of parameters, in this case
            #handLms is a single hand, in this case, it is hand 0 in our flipCam, then mpHands.HAND_CONNECTIONS uses the mpHands module to draw connections across limbs
        return flipCam
    
    #loop-like logic
    def findPosition(self,flipCam, handIndex = 0, draw = True):
        landmarkList = [] #first index = id second = x third = y
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handIndex]
            for id,lm in enumerate(myHand.landmark): #here id is the ettiquete itself and lm is the landmark we're getting
               #from 'handsLms.landmark', enumerate is used to sort them in order, for loop to go through each one
                #each id returns x,y,z 
                #sheer,raw values before turned into pixels are the image ratio (it might see like -6.40244)
                #if we multiply by the width and height we get the pixel value
                #for each hand landmark get the information from it              
                height,width,channels = flipCam.shape #get height,width, and channels from the flipCam shape
                center_x,center_y = int(lm.x*width), int(lm.y*height) #here we will multiply the landmark by the width and height but separate the variables
                 #print id,x, and y pixel values
                landmarkList.append([id,center_x,center_y])
                #if draw:
                  # #id certain landmark is certain landmark then:
                    #cv2.circle(flipCam,(center_x,center_y),15,color,cv2.FILLED) 
                    # #this draws a circle for that landmark, which matches
                    #its pixel value, then, comes '25' which is the size and BGR color, then we fill it
        return(landmarkList)

last_cmd = None
last_send_time = 0
interval = 0.1

thumb_up,thumb_down,palm_stop,peace_right,peace_left,rock_left,rock_right,shotgun_right,shotgun_left = False,False,False,False,False,False,False,False,False
def main():
        
    global last_cmd,last_send_time,interval
    previous_time = 0
    current_time = 0
    video = cv2.VideoCapture(0) #open webcam
   
    
    detector = handDetector()
    
    while True:
        trueYN, frame = video.read()
        flipCam = cv2.flip(frame, 1)
        flipCam = detector.findHands(flipCam,draw=True) #set to true for vectors
        landmarkList = detector.findPosition(flipCam,draw= False) #set to true for your own drawings
        #Please note that:
        #from left to right: x increases
        #from up  to down: y increases
        #so the leftmost value of x is 0 and the rightmost is  >= 600
        #for y, it would give you 0 from the top and slowly build its way to >= 600 to the bottom
        #it is a 640x40 image

        #create dictionaries for modular project making
        #for i in landmarkList:
            #print(i)
        palm = {"BottomPalm":0}
            
        knuckles = {"thumb_knuckles":1,"index_knuckles":5,"middle_knuckles":9,"ring_knuckles":13,"pinky_knuckles":17}

        fingers = {"Thumb":{
                "Bottom": 2,"Middle":3,"Tip":4
            },
            "Index":{
                "Bottom": 6,"Middle":7,"Tip":8
            },
            "Middle":{
                "Bottom": 10,"Middle":11,"Tip":12
            },
            "Ring":{
                "Bottom": 14,"Middle":15,"Tip":16
            },
            "Pinky":{
                "Bottom": 18,"Middle":19,"Tip":20
            }
            }
        def palmTracing(color,size,Palm = False):
            """
            Maps '0' respectively, if not using set it to False
            """
            if Palm == True:
               center_x_palm = landmarkList[palm["BottomPalm"]][1]
               center_y_palm = landmarkList[palm["BottomPalm"]][2]
               cv2.circle(flipCam,(center_x_palm,center_y_palm),size,color,cv2.FILLED) 
            return()
        def knuckleTracing(color,size,KnuckleThumb = False,KnuckleIndex = False,KnuckleMiddle = False,KnuckleRinger = False,KnucklePinky = False):
            """
            knuckle tracing maps 1,5,9,13, and 17 respetively. If just manipulatiung a single landmark or finger set it to false
            """
            if KnuckleThumb == True:
               center_x_KnuckleThumb = landmarkList[knuckles["thumb_knuckles"]][1]
               center_y_KnuckleThumb = landmarkList[knuckles["thumb_knuckles"]][2]
               cv2.circle(flipCam,(center_x_KnuckleThumb,center_y_KnuckleThumb),size,color,cv2.FILLED)

            if KnuckleIndex == True:
                center_x_KnuckleIndex = landmarkList[knuckles["index_knuckles"]][1]
                center_y_KnuckleIndex = landmarkList[knuckles["index_knuckles"]][2]
                cv2.circle(flipCam,(center_x_KnuckleIndex,center_y_KnuckleIndex),size,color,cv2.FILLED) 

            if KnuckleMiddle == True:
                center_x_KnuckleMiddle = landmarkList[knuckles["middle_knuckles"]][1]
                center_y_KnuckleMiddle = landmarkList[knuckles["middle_knuckles"]][2]
                cv2.circle(flipCam,(center_x_KnuckleMiddle,center_y_KnuckleMiddle),size,color,cv2.FILLED) 
                
            if KnuckleRinger == True:    
                center_x_KnuckleRinger = landmarkList[knuckles["ring_knuckles"]][1]
                center_y_KnuckleRinger = landmarkList[knuckles["ring_knuckles"]][2]
                cv2.circle(flipCam,(center_x_KnuckleRinger,center_y_KnuckleRinger),size,color,cv2.FILLED)

            if KnucklePinky == True:
               center_x_KnucklePinky = landmarkList[knuckles["pinky_knuckles"]][1]
               center_y_KnucklePinky = landmarkList[knuckles["pinky_knuckles"]][2]
               cv2.circle(flipCam,(center_x_KnucklePinky,center_y_KnucklePinky),size,color,cv2.FILLED)
            return()
        
        def fingerTracing(color,size,thumbFinger = False, indexFinger = False, middleFinger = False, ringerFinger = False, pinkyFinger = False):
            """
            This maps the rest of the indexes (2,3,4,6,7,8,10,11,12,14,15,16,18,19,20) respectively, comment out if not using 
            landmark, set to False if not usign specific finger
            """

            if thumbFinger == True:
               center_x_Fthumb = landmarkList[fingers["Thumb"]["Bottom"]][1]
               center_y_Fthumb = landmarkList[fingers["Thumb"]["Bottom"]][2]

               center_x_FthumbMiddle = landmarkList[fingers["Thumb"]["Middle"]][1]
               center_y_FthumbMiddle = landmarkList[fingers["Thumb"]["Middle"]][2]

               center_x_FthumbTip = landmarkList[fingers["Thumb"]["Tip"]][1]
               center_y_FthumbTip = landmarkList[fingers["Thumb"]["Tip"]][2]

               cv2.circle(flipCam,(center_x_Fthumb,center_y_Fthumb),size,color,cv2.FILLED)
               cv2.circle(flipCam,(center_x_FthumbMiddle,center_y_FthumbMiddle),size,color,cv2.FILLED)
               cv2.circle(flipCam,(center_x_FthumbTip,center_y_FthumbTip),size,color,cv2.FILLED)

            if indexFinger == True:
               center_x_FIndex = landmarkList[fingers["Index"]["Bottom"]][1]
               center_y_FIndex = landmarkList[fingers["Index"]["Bottom"]][2]

               center_x_FIndexMiddle = landmarkList[fingers["Index"]["Middle"]][1]
               center_y_FIndexMiddle = landmarkList[fingers["Index"]["Middle"]][2]

               center_x_FIndexTip = landmarkList[fingers["Index"]["Tip"]][1]
               center_y_FIndexTip = landmarkList[fingers["Index"]["Tip"]][2]

               cv2.circle(flipCam,(center_x_FIndex,center_y_FIndex),size,color,cv2.FILLED)
               cv2.circle(flipCam,(center_x_FIndexMiddle,center_y_FIndexMiddle),size,color,cv2.FILLED)
               cv2.circle(flipCam,(center_x_FIndexTip,center_y_FIndexTip),size,color,cv2.FILLED)

            if middleFinger == True:
               center_x_FMiddle = landmarkList[fingers["Middle"]["Bottom"]][1]
               center_y_FMiddle = landmarkList[fingers["Middle"]["Bottom"]][2]

               center_x_FMiddleMiddle = landmarkList[fingers["Middle"]["Middle"]][1]
               center_y_FMiddleMiddle = landmarkList[fingers["Middle"]["Middle"]][2]

               center_x_FMiddleTip = landmarkList[fingers["Middle"]["Tip"]][1]
               center_y_FMiddleTip = landmarkList[fingers["Middle"]["Tip"]][2]

               cv2.circle(flipCam,(center_x_FMiddle,center_y_FMiddle),size,color,cv2.FILLED)
               cv2.circle(flipCam,(center_x_FMiddleMiddle,center_y_FMiddleMiddle),size,color,cv2.FILLED)
               cv2.circle(flipCam,(center_x_FMiddleTip,center_y_FMiddleTip),size,color,cv2.FILLED)

            if ringerFinger == True:
               center_x_Fring = landmarkList[fingers["Ring"]["Bottom"]][1]
               center_y_Fring = landmarkList[fingers["Ring"]["Bottom"]][2]

               center_x_FringMiddle = landmarkList[fingers["Ring"]["Middle"]][1]
               center_y_FringMiddle = landmarkList[fingers["Ring"]["Middle"]][2]

               center_x_FringTip = landmarkList[fingers["Ring"]["Tip"]][1]
               center_y_FringTip = landmarkList[fingers["Ring"]["Tip"]][2]

               cv2.circle(flipCam,(center_x_Fring,center_y_Fring),size,color,cv2.FILLED)
               cv2.circle(flipCam,(center_x_FringMiddle,center_y_FringMiddle),size,color,cv2.FILLED)
               cv2.circle(flipCam,(center_x_FringTip,center_y_FringTip),size,color,cv2.FILLED)

            if pinkyFinger == True:
               center_x_Fpinky = landmarkList[fingers["Pinky"]["Bottom"]][1]
               center_y_Fpinky = landmarkList[fingers["Pinky"]["Bottom"]][2]

               center_x_FpinkyMiddle = landmarkList[fingers["Pinky"]["Middle"]][1]
               center_y_FpinkyMiddle = landmarkList[fingers["Pinky"]["Middle"]][2]

               center_x_FpinkyTip = landmarkList[fingers["Pinky"]["Tip"]][1]
               center_y_FpinkyTip = landmarkList[fingers["Pinky"]["Tip"]][2]

               cv2.circle(flipCam,(center_x_Fpinky,center_y_Fpinky),size,color,cv2.FILLED)
               cv2.circle(flipCam,(center_x_FpinkyMiddle,center_y_FpinkyMiddle),size,color,cv2.FILLED)
               cv2.circle(flipCam,(center_x_FpinkyTip,center_y_FpinkyTip),size,color,cv2.FILLED)

        
        def get_distance_pixels(valueY2,valueY1):
            distance_pixels = valueY2 - valueY1
            return distance_pixels
        
        def non_zero_div(numerator,denominator):
            if denominator == 0 or numerator == 0:
                return None
            elif numerator != None and denominator != None:
                ratio_non_zero = round(numerator/denominator,2)
                return(ratio_non_zero)                                                                          
       
        def send_cmd_hands(command):
            global last_cmd,last_send_time,interval
            start = tm.time()
            if (start - last_send_time) > interval:
                send_logic_hands = sock.sendto(command.encode(),(ESP32_IP,Port)) 
                last_cmd = command
                last_send_time = start
            return()
        
        #Dictionaries for gesture scalation PWM
        #thumb_up_PWM = {
           # "ratio": None

       # }
        
        

  
        def thumb_up():
            global thumb_up
            """
            We will get the distance between the tip of the thumb (index 4) and the knuckle of the index (5)
            """
            
            center_y_FthumbTip = landmarkList[fingers["Thumb"]["Tip"]][2]

            center_y_KnuckleIndex = landmarkList[knuckles["index_knuckles"]][2]

            center_y_palm = landmarkList[palm["BottomPalm"]][2]

            center_y_KnuckleMiddle = landmarkList[knuckles["middle_knuckles"]][2]

            distance_ThumbTip_to_IndexKnuckle = get_distance_pixels(center_y_KnuckleIndex,center_y_FthumbTip)

            distance_palm_to_middleKnuckle = get_distance_pixels(center_y_palm, center_y_KnuckleMiddle)

            ratio = non_zero_div(distance_ThumbTip_to_IndexKnuckle,distance_palm_to_middleKnuckle)
           # PWM_values_thumb_up = round(ratio*120,2)
            
            if ratio is None or distance_ThumbTip_to_IndexKnuckle is None or distance_palm_to_middleKnuckle is None:
                return None
            elif ratio >= 1.10 and distance_ThumbTip_to_IndexKnuckle >= 20 and distance_palm_to_middleKnuckle >= 20 :
            #else:
               thumb_up = True
        
            else:
                thumb_up = False

            return()
        
        
        def Peace_sign_rightMost(): 
            global peace_right 
            center_y_KnuckleIndex = landmarkList[knuckles["index_knuckles"]][2]
            center_y_palm = landmarkList[palm["BottomPalm"]][2]

            tip_of_index_y = landmarkList[fingers["Index"]["Tip"]][2]
            tip_of_middle_y = landmarkList[fingers["Middle"]["Tip"]][2]
            tip_of_index_x = landmarkList[fingers["Index"]["Tip"]][1]
            tip_of_middle_x = landmarkList[fingers["Middle"]["Tip"]][1]


            tip_of_pinky_y = landmarkList[fingers['Pinky']['Tip']][2]
            tip_of_thumb_y = landmarkList[fingers['Thumb']['Tip']][2]
            
            distance_palm_to_middleKnuckle = get_distance_pixels(center_y_palm, center_y_KnuckleIndex)

            Distance_pinky_thumb= get_distance_pixels(tip_of_thumb_y,tip_of_pinky_y)

            ratio_for_exclution = non_zero_div(Distance_pinky_thumb,distance_palm_to_middleKnuckle)

            distanceIndexandMiddle = get_distance_pixels(tip_of_middle_y,tip_of_index_y)

            ratio = non_zero_div(distanceIndexandMiddle,distance_palm_to_middleKnuckle)
            
            palm_x = landmarkList[palm["BottomPalm"]][1]

            if ratio is None or ratio_for_exclution is None or palm_x is None:
                return None
            elif ratio <= -0.10 and ratio_for_exclution < 0.05 and palm_x > 350:
                fingerTracing(color = (0,0,255),size = 12,indexFinger = True,middleFinger = True)
                peace_right = True
            else:
                peace_right = False

               
            return()
     
        def Peace_sign_leftMost():
            global peace_left 
            center_y_KnuckleIndex = landmarkList[knuckles["index_knuckles"]][2]
            center_y_palm = landmarkList[palm["BottomPalm"]][2]

            tip_of_index_y = landmarkList[fingers["Index"]["Tip"]][2]
            tip_of_middle_y = landmarkList[fingers["Middle"]["Tip"]][2]
            tip_of_index_x = landmarkList[fingers["Index"]["Tip"]][1]
            tip_of_middle_x = landmarkList[fingers["Middle"]["Tip"]][1]


            tip_of_pinky_y = landmarkList[fingers['Pinky']['Tip']][2]
            tip_of_thumb_y = landmarkList[fingers['Thumb']['Tip']][2]
            
            distance_palm_to_middleKnuckle = get_distance_pixels(center_y_palm, center_y_KnuckleIndex)

            Distance_pinky_thumb= get_distance_pixels(tip_of_thumb_y,tip_of_pinky_y)

            ratio_for_exclution = non_zero_div(Distance_pinky_thumb,distance_palm_to_middleKnuckle)

            distanceIndexandMiddle = get_distance_pixels(tip_of_middle_y,tip_of_index_y)

            ratio = non_zero_div(distanceIndexandMiddle,distance_palm_to_middleKnuckle)
            
            palm_x = landmarkList[palm["BottomPalm"]][1]

            if ratio is None or ratio_for_exclution is None or palm_x is None:
                return None
       
            elif ratio <= -0.10 and ratio_for_exclution < 0.05 and palm_x <= 350:
                peace_left = True
            else:
                peace_left = False


            return()
        
      
               




        def thumb_down():
            global thumb_down
            center_y_FthumbTip = landmarkList[fingers["Thumb"]["Tip"]][2]

            center_y_KnuckleIndex = landmarkList[knuckles["index_knuckles"]][2]

            center_y_palm = landmarkList[palm["BottomPalm"]][2]

            center_y_KnuckleMiddle = landmarkList[knuckles["middle_knuckles"]][2]

            distance_ThumbTip_to_IndexKnuckle = get_distance_pixels(center_y_KnuckleIndex,center_y_FthumbTip)

            distance_palm_to_middleKnuckle = center_y_palm

            ratio = non_zero_div(distance_ThumbTip_to_IndexKnuckle,distance_palm_to_middleKnuckle)
            if ratio is None:
                return None
            elif ratio <= -0.4:
                thumb_down = True
            else:
                thumb_down = False
        
            return()
        
        
        
        def openPalm():
            global palm_stop
            tip_of_thumb_y = landmarkList[fingers["Thumb"]["Tip"]][2]
            tip_of_index_y = landmarkList[fingers["Index"]["Tip"]][2]
            tip_of_middle_y = landmarkList[fingers["Middle"]["Tip"]][2]
            tip_of_ring_y = landmarkList[fingers["Ring"]["Tip"]][2]
            tip_of_pinky_y = landmarkList[fingers["Pinky"]["Tip"]][2]

            palm_landmark_y = landmarkList[palm["BottomPalm"]][2]

            middle_of_ring = landmarkList[fingers['Ring']['Middle']][2]

            distance_thumb_index = get_distance_pixels(tip_of_index_y,tip_of_thumb_y)
            distance_middle_ring = get_distance_pixels(tip_of_middle_y,tip_of_ring_y)
            distance_ring_pinky = get_distance_pixels(tip_of_ring_y,tip_of_pinky_y)

            ratio_thumb_index = non_zero_div(distance_thumb_index,palm_landmark_y)
            ratio_ring_pinky = non_zero_div(distance_ring_pinky,palm_landmark_y)

            ratio_pinky_thumb = non_zero_div(tip_of_thumb_y,middle_of_ring)

          
            if ratio_thumb_index is None or ratio_ring_pinky is None or ratio_pinky_thumb is None:
                return None

            elif ratio_thumb_index  <= - 0.13 and ratio_ring_pinky <= - 0.08 and ratio_pinky_thumb >= 1.15:
                palm_stop = True
            else:
                palm_stop = False

            return()
        def shotGun_leftMost():
            global shotgun_left
            tip_of_thumb_y = landmarkList[fingers["Thumb"]["Tip"]][2]
            tip_of_index_y = landmarkList[fingers["Index"]["Tip"]][2]
            bottom_index_y = landmarkList[fingers["Index"]["Bottom"]][2]
            tip_of_ring_y = landmarkList[fingers["Ring"]["Tip"]][2]
            tip_of_pinky_y = landmarkList[fingers["Pinky"]["Tip"]][2]
            index_knuckle_y = landmarkList[knuckles['index_knuckles']][2]

            middle_of_ring = landmarkList[fingers['Ring']['Middle']][2]

            tip_of_Middle = landmarkList[fingers['Middle']['Tip']][2]
            #1a 1b ISEF 1 
            Middle_middle = landmarkList[fingers['Middle']['Middle']][2]
            

            palm_landmark_y = landmarkList[palm["BottomPalm"]][2]
        
            distance_thumb_index = get_distance_pixels(tip_of_index_y,tip_of_thumb_y)
            #distance_ring_pinky = get_distance_pixels(tip_of_ring_y,tip_of_pinky_y)
            
            distance_indexKnuckle_tip_thumb = get_distance_pixels(index_knuckle_y,tip_of_thumb_y)

            distance_indexBottom_index_tip = get_distance_pixels(tip_of_index_y,bottom_index_y)

           # ratio_thumb_tip_ring = non_zero_div(tip_of_thumb_y, middle_of_ring)

            ratio_shotgun_palm = non_zero_div(distance_thumb_index,palm_landmark_y)

            ratio_shotGunPalm_indexKnuckle = non_zero_div(distance_indexKnuckle_tip_thumb,palm_landmark_y)
            
            ratio_index_tip_middle_tip = non_zero_div(tip_of_Middle,tip_of_index_y)
            palm_x = landmarkList[palm["BottomPalm"]][1]

            ratio_thumb_tip_to_middle=non_zero_div(tip_of_thumb_y,Middle_middle)

       
            if ratio_shotgun_palm is None or distance_indexBottom_index_tip is None or ratio_shotGunPalm_indexKnuckle is None or ratio_index_tip_middle_tip is None or ratio_thumb_tip_to_middle is None or palm_x is None:
                return None
            

            elif ratio_shotgun_palm <= -0.30 and ratio_shotGunPalm_indexKnuckle <=  -0.15 and palm_x <= 350 and ratio_index_tip_middle_tip >= 1.50 and ratio_thumb_tip_to_middle >= 1.02:
                shotgun_left = True
            else:
                shotgun_left = False
           
        
            return()
        
        def shotGun_RightMost():
            global shotgun_right
            tip_of_thumb_y = landmarkList[fingers["Thumb"]["Tip"]][2]
            tip_of_index_y = landmarkList[fingers["Index"]["Tip"]][2]
            bottom_index_y = landmarkList[fingers["Index"]["Bottom"]][2]
            tip_of_ring_y = landmarkList[fingers["Ring"]["Tip"]][2]
            tip_of_pinky_y = landmarkList[fingers["Pinky"]["Tip"]][2]
            index_knuckle_y = landmarkList[knuckles['index_knuckles']][2]

            middle_of_ring = landmarkList[fingers['Ring']['Middle']][2]

            tip_of_Middle = landmarkList[fingers['Middle']['Tip']][2]
            #1a 1b ISEF 1 
            Middle_middle = landmarkList[fingers['Middle']['Middle']][2]
            

            palm_landmark_y = landmarkList[palm["BottomPalm"]][2]
        
            distance_thumb_index = get_distance_pixels(tip_of_index_y,tip_of_thumb_y)
            #distance_ring_pinky = get_distance_pixels(tip_of_ring_y,tip_of_pinky_y)
            
            distance_indexKnuckle_tip_thumb = get_distance_pixels(index_knuckle_y,tip_of_thumb_y)

            distance_indexBottom_index_tip = get_distance_pixels(tip_of_index_y,bottom_index_y)

           # ratio_thumb_tip_ring = non_zero_div(tip_of_thumb_y, middle_of_ring)

            ratio_shotgun_palm = non_zero_div(distance_thumb_index,palm_landmark_y)

            ratio_shotGunPalm_indexKnuckle = non_zero_div(distance_indexKnuckle_tip_thumb,palm_landmark_y)
            
            ratio_index_tip_middle_tip = non_zero_div(tip_of_Middle,tip_of_index_y)

            palm_x = landmarkList[palm["BottomPalm"]][1]
            
            ratio_thumb_tip_to_middle=non_zero_div(tip_of_thumb_y,Middle_middle)


  
            if ratio_shotgun_palm is None or distance_indexBottom_index_tip is None or ratio_shotGunPalm_indexKnuckle is None or ratio_index_tip_middle_tip is None or ratio_thumb_tip_to_middle is None or palm_x is None:
                return None
            

            elif ratio_shotgun_palm <= -0.30 and ratio_shotGunPalm_indexKnuckle <=  -0.15 and palm_x > 350 and ratio_index_tip_middle_tip >= 1.50 and ratio_thumb_tip_to_middle >= 1.02:
                shotgun_right = True
            else:
                shotgun_right = False
        
            return()
        
        def rock_and_roll_leftMost():
            global rock_left 
            """LET THERE BE ROOOOOCK!!!!!"""
            index_middle = landmarkList[fingers['Middle']['Middle']][2]
            thumb_tip = landmarkList[fingers['Thumb']['Tip']][2]
            ringer_middle = landmarkList[fingers['Ring']['Middle']][2]
            pinky_middle = landmarkList[fingers['Pinky']['Tip']][2]
            palm_x = landmarkList[palm["BottomPalm"]][1]

     
            
            distance_thumb_index = get_distance_pixels(index_middle,thumb_tip)
            ratio_ringer_pinky = non_zero_div(ringer_middle,pinky_middle)

            ratio_thumb_index = non_zero_div(distance_thumb_index,ratio_ringer_pinky)


            if ratio_thumb_index is None or ratio_thumb_index is None or ratio_ringer_pinky is None or palm_x is None:
                return None
            elif ratio_thumb_index <= 35 and ratio_thumb_index >= 2 and ratio_ringer_pinky >=1.10 and palm_x <= 350:
               rock_left = True
            else:
                rock_left = False
            return ()
        
        def rock_and_roll_rightMost():
            global rock_right
            """LET THERE BE ROOOOOCK!!!!!"""
            index_middle = landmarkList[fingers['Middle']['Middle']][2]
            thumb_tip = landmarkList[fingers['Thumb']['Tip']][2]
            ringer_middle = landmarkList[fingers['Ring']['Middle']][2]
            pinky_tip = landmarkList[fingers['Pinky']['Tip']][2]
            palm_x = landmarkList[palm["BottomPalm"]][1]

            
            distance_thumb_index = get_distance_pixels(index_middle,thumb_tip)
            ratio_ringer_pinky = non_zero_div(ringer_middle,pinky_tip)

            ratio_thumb_index = non_zero_div(distance_thumb_index,ratio_ringer_pinky)

          

            if ratio_thumb_index is None or ratio_thumb_index is None or ratio_ringer_pinky is None or palm_x is None:
                return None
            elif ratio_thumb_index <= 40 and ratio_thumb_index >= 2 and ratio_ringer_pinky >=1.10 and palm_x > 350:
               rock_right = True
            else:
                rock_right = False
               
            return ()
        def state_machine():
            global thumb_up,thumb_down,palm_stop,peace_right,peace_left,rock_left,rock_right,shotgun_right,shotgun_left
            if thumb_up == True:
                cv2.putText(flipCam,"Thumb Up",(0,35),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,255),3) 
                fingerTracing(color = (255,0,0),size = 12,thumbFinger=True)
                send_cmd_hands("F")
            elif thumb_down == True:
                cv2.putText(flipCam,"Thumb Down",(0,35),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,255),3) 
                fingerTracing(color = (0,0,255),size=12,thumbFinger=True)
                send_cmd_hands("B")
            elif palm_stop == True:
                cv2.putText(flipCam,"Palm",(0,35),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,255),3) 
                fingerTracing((0,255,255),size = 12,thumbFinger = True, indexFinger = True, middleFinger = True, ringerFinger = True, pinkyFinger = True)
                send_cmd_hands("X")
            elif peace_right == True:
                cv2.putText(flipCam,"PeaceRight",(0,35),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,255),3) 
                fingerTracing(color = (0,0,255),size = 12,indexFinger = True,middleFinger = True)
                send_cmd_hands("45_DEG")
            elif peace_left == True:
                cv2.putText(flipCam,"PeaceLeft",(0,35),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,255),3) 
                fingerTracing(color = (255,0,0),size = 12,indexFinger = True,middleFinger = True)
                send_cmd_hands("135_DEG") 
            elif rock_left == True:
                cv2.putText(flipCam,"RockLeft",(0,35),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,255),3) 
                fingerTracing((255,0,0),size=12,thumbFinger = True,pinkyFinger=True) 
                send_cmd_hands("RL")
            elif rock_right == True:
                cv2.putText(flipCam,"RockRight",(0,35),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,255),3) 
                fingerTracing((0,0,255),size=12,thumbFinger = True,pinkyFinger=True)
                send_cmd_hands("RR")
            elif shotgun_left == True:
                cv2.putText(flipCam,"ShotGun LEFT",(0,35),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,255),3) 
                fingerTracing((255,0,0),size=12,indexFinger = True,thumbFinger = True)
                send_cmd_hands("SL")
            elif shotgun_right == True:
                cv2.putText(flipCam,"ShotGun RIGHT",(0,35),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,255),3) 
                fingerTracing((0,0,255),size=12,indexFinger = True,thumbFinger = True)
                send_cmd_hands("SR")
            else:
              cv2.putText(flipCam,"Neutral",(0,35),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,255),3) 
            return()
        
        




        if len(landmarkList) != 0:

            state_machine()
            #forward & back
            thumb_up() #go forward
            thumb_down() #go backwards

            openPalm() #stopCameraRotation 

            #rotate camera (ESP32S3 mounted on servo)
            Peace_sign_rightMost() #rotate camera/servo to the right
            Peace_sign_leftMost() #rotate camera/servo to the left 
        
            #strafing
            shotGun_RightMost() #Strafe Right
            shotGun_leftMost() #Strafe Left
            
            #Rotation
            rock_and_roll_leftMost() #rotate Left
            rock_and_roll_rightMost() #rotate Right

            

            """
            Here goes all logic
            """
            
            #challenge: if a peace sign is made, stop
            
            #palmTracing(Palm = True) #palm
            #knuckleTracing(KnuckleThumb = False,KnuckleIndex = False,KnuckleMiddle = False,KnuckleRinger = False,KnucklePinky = False) #knuckles
            #fingerTracing(thumbFinger = False, indexFinger = False, middleFinger = False, ringerFinger = False, pinkyFinger = False) #fingers

        
        #cv2.putText(flipCam,str("For better results look for a stable lighting (nor too bright nor too dark)\n please"`),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)  
        #cv2.putText(flipCam,"Axel!",(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255),3) My name
        #here the first argument to the parameters is 'flipCam' (a.k.a our actual video) then we cast the fps (int) to a string
        #since we are displaying text, then we give it (10,70) which is out x,y and then cv2.font is the font and then 3 is the
         #thickness, then (BGR) is blue, red, green (in this case the combination is purple) then 3 is the scale at the end


        cv2.imshow("Webcam",flipCam) #name webcam window 'n show flipCam
        if cv2.waitKey(1) & 0xFF == ord('x'):
            send_cmd_hands("X")
            break
    flipCam.release()
    cv2.destroyAllWindows()
    


if __name__ == "__main__": #if we run this script do this
    main() 

