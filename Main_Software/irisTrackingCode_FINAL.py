import cv2
import mediapipe as mp
import socket #for communication with Arduino IDE
import time as tm


ESP32_IP = "10.138.11.157" #my ip

Port = 4210

#UDP socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#USE THIS FUNCTION FOR COMMAND SENDING
last_cmd = None
last_send_time = 0
interval = 0.1

def send_cmd(command):
        global last_cmd,last_send_time,interval
        start = tm.time()
        if (start - last_send_time) > interval:
            send_logic_eyes = sock.sendto(command.encode(),(ESP32_IP,Port)) 
            last_cmd = command
            last_send_time = start
            return()
        
mp_face_mesh = mp.solutions.face_mesh #get the actual AI
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,  # This enables the iris landmarks
    min_detection_confidence=0.6, # The more high it is the less jitter
    min_tracking_confidence=0.6
)



def getDistance(valueX2,valueX1):
        distance = valueX2 - valueX1
        return distance
        
"""Left_Eye_Iris= [468, 469, 470, 471, 472]
Right_Eye_Iris= [473, 474, 475, 476, 477]
#Left Eye identify:
#468 = middle of iris, 469 = rightmost corner >, 470 = uppermost ^, 471 = leftmost <, 472 = downmost .
#right label:
#474 = rightmost
leftLmcenter = 0
rightMostLm = 0 
leftMostLm = 0
RightLmcenter = 0
Run1nonZeroLogic = False
Run2nonZeroLogic = False
left_and_rightMost_cornerDistance = 0
center_right_and_center_left = 0
nonZero_left_and_rightMost_cornerDistance = 0
nonZero_center_right_and_center_leftDistance = 0
ratio = 0"""

video = cv2.VideoCapture(0)

while True:
  
    broken_by_failedCapture, capture = video.read()

    
    

    # Invert y-axis
    flipCam = cv2.flip(capture, 1)
    
    #convert to RGB
    rgb_capture = cv2.cvtColor(flipCam, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_capture)
    
    
    if results.multi_face_landmarks:
        mesh_coords = results.multi_face_landmarks[0]

    #dictionary to capture landmarks
    #landmark_for_reading = {}
    #for id in range(468, 478):
   
            
        #478 for it to be inclusive
            
            


    #landmark = mesh_coords.landmark[id]

    landmark468 = mesh_coords.landmark[468]#center
    landmark133 = mesh_coords.landmark[133]#rightmost
    landmark33 = mesh_coords.landmark[33]#leftmost
    landmark52 = mesh_coords.landmark[52]#uppermost
    landmark152 = mesh_coords.landmark[152]#downmost
    landmark473 = mesh_coords.landmark[473]#center right
    landmark386 = mesh_coords.landmark[386]#downwmostForCrushagainstCenter Right
    landmark145 = mesh_coords.landmark[145]#downwmostForCrushagainstCenter Left
    landmark0 = mesh_coords.landmark[0] #middle of lip Top
    landmark17 = mesh_coords.landmark[17] #bottom of lip
    landmark61 = mesh_coords.landmark[61] #left corner lip
    landmark291 = mesh_coords.landmark[291] #right corner lip
    landmark205 = mesh_coords.landmark[205] #left corner center cheek
    landmark425 = mesh_coords.landmark[425] #right corner center cheek

            
    # Pixel values
    height, width, channel = flipCam.shape

    center_x_468, center_y_468 = int(landmark468.x * width), int(landmark468.y * height)
    
    center_x_133, center_y_133 = int(landmark133.x * width), int(landmark133.y * height)

    center_x_33, center_y_33 = int(landmark33.x * width), int(landmark33.y * height)

    center_x_52, center_y_52= int(landmark52.x * width), int(landmark52.y * height)

    center_x_152, center_y_152 = int(landmark152.x * width), int(landmark152.y * height)

    center_x_473, center_y_473 = int(landmark473.x * width), int(landmark473.y * height)
    
    center_x_386, center_y_386 = int(landmark386.x * width), int(landmark386.y * height)

    center_x_145, center_y_145 = int(landmark145.x * width), int(landmark145.y * height)

    center_x_0, center_y_0 = int(landmark0.x * width), int(landmark0.y * height)

    center_x_17, center_y_17 = int(landmark17.x * width), int(landmark17.y * height)

    center_x_61, center_y_61 = int(landmark61.x * width), int(landmark61.y * height)
    
    center_x_291, center_y_291 = int(landmark291.x * width), int(landmark291.y * height)
    
    center_x_205, center_y_205 = int(landmark205.x * width), int(landmark205.y * height)

    center_x_425, center_y_425 = int(landmark425.x * width), int(landmark425.y * height)

    #For every iteration these values will reset after reacing the circle statement, meaning
    #the index will remian the same since they don't 'stack', they just overwrite themselves
    #landmark_for_reading[id] = (center_x,center_y) #id is the key and then its value are the coordinates

    cv2.circle(flipCam,(center_x_133, center_y_133),2,(0,255,255),cv2.FILLED)

    cv2.circle(flipCam,(center_x_468, center_y_468),2,(0,255,0),cv2.FILLED)
       
    cv2.circle(flipCam,(center_x_33, center_y_33),2,(0,255,255),cv2.FILLED)

    cv2.circle(flipCam,(center_x_52, center_y_52),2,(255,0,0),cv2.FILLED)
    
    cv2.circle(flipCam,(center_x_152, center_y_152),2,(255,0,0),cv2.FILLED)

    cv2.circle(flipCam,(center_x_473, center_y_473),2,(0,0,255),cv2.FILLED)
    
    cv2.circle(flipCam,(center_x_386, center_y_386),2,(0,0,255),cv2.FILLED)

    cv2.circle(flipCam,(center_x_145, center_y_145),2,(0,255,0),cv2.FILLED)

    cv2.circle(flipCam,(center_x_0, center_y_0),2,(0,255,0),cv2.FILLED)

    cv2.circle(flipCam,(center_x_17, center_y_17),2,(0,255,0),cv2.FILLED)

    cv2.circle(flipCam,(center_x_61, center_y_61),2,(0,255,0),cv2.FILLED)

    cv2.circle(flipCam,(center_x_291, center_y_291),2,(0,255,0),cv2.FILLED)

    cv2.circle(flipCam,(center_x_205, center_y_205),2,(0,255,0),cv2.FILLED)

    cv2.circle(flipCam,(center_x_425, center_y_425),2,(0,255,0),cv2.FILLED)


    def divideZero(value1,value2):
        division = 0
        if value2 == 0:
              return None
        else:
            division = round(value1/value2,2)
            return division
        
    def eyeLogic():
       global looking_up,looking_down,looking_left,looking_right,Neutral,looking_right_Hawk,looking_left_Hawk,looking_up_hawk
       Distance_center_to_up = getDistance(center_y_468,center_y_52)
       Distance_center_to_down = getDistance(center_y_152,center_y_468)
       ratioforYs = divideZero(Distance_center_to_down,Distance_center_to_up)

       DistanceClose_Crash_Center_to_Down = getDistance(center_y_386,center_y_473)
    
       DistanceClose_Crash_Center_to_Down_LEFT = getDistance(center_y_145,center_y_468)

       Distance_center_to_left = getDistance(center_x_468,center_x_33)
       Distance_center_to_right = getDistance(center_x_133,center_x_468)
       #ratio = divideZero(Distance_center_to_left,Distance_center_to_right)
       ratio_FRONT = divideZero(Distance_center_to_left,Distance_center_to_down)
       ratio_Laterals = divideZero(Distance_center_to_left,Distance_center_to_up)


       #if DistanceClose_Crash_Center_to_Down <=1: #GoBackwards

       if ratioforYs is None or ratio_Laterals is None or ratio_FRONT is None:
           return 
       elif ratioforYs >= 7.30 and looking_left != True:
           looking_up = True
       elif ratioforYs <= 5.15: #Go Backwards
           looking_down = True
     #run if and only if others are false
       
       elif ratio_Laterals <= 0.58 and looking_down != True and looking_up != True and Neutral != True:
           looking_left = True
          

       elif ratio_Laterals >= 1 and looking_down != True and looking_up != True:
          looking_right = True

       elif ratio_FRONT >= .1 and ratio_FRONT <= .13 and looking_left != True:
          Neutral = True
        
       return()
         

    
    looking_up,looking_down,looking_left,looking_right,looking_left_Hawk,looking_right_Hawk,looking_up_hawk = False,False,False,False,False,False,False
    smirking_left,smirking_right,Neutral = False,False,False
    def logic_smirking():
        global smirking_left,smirking_right
        #distances and ratios then if statements
        distance_bottom_top_lip = getDistance(center_y_17,center_y_0)
        distance_left_right_cornerOflips = getDistance(center_y_61,center_y_291)
        
        distance_left_corner_lip_to_LeftCheek = getDistance(center_y_205,center_y_61)
        distance_right_corner_lip_to_RightCheek = getDistance(center_y_425,center_y_291)
  
        ratio_leftCornerLip_to_leftCheek = divideZero(distance_left_corner_lip_to_LeftCheek,distance_left_right_cornerOflips)
        ratio_rightCornerLip_to_RightCheek = divideZero(distance_right_corner_lip_to_RightCheek,distance_left_right_cornerOflips)

   
        if ratio_leftCornerLip_to_leftCheek is None or ratio_rightCornerLip_to_RightCheek is None:
            return None 
        elif ratio_leftCornerLip_to_leftCheek <= 5.20 and ratio_leftCornerLip_to_leftCheek >= 0:
            smirking_left = True
        elif ratio_leftCornerLip_to_leftCheek <= 0 and ratio_rightCornerLip_to_RightCheek >= -6.20:
            smirking_right = True
            
        
        return()        
    
    def state_machine():
        global smirking_left,smirking_right,Neutral, looking_up,looking_down,looking_left,looking_right,looking_left_Hawk,looking_right_Hawk,looking_up_hawk

        if smirking_left == True:
            cv2.putText(flipCam,"Smirking LEFT",(0,35),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,255),3) 
            send_cmd("RL")
            print("Smirking Left")
        elif smirking_right == True:
            cv2.putText(flipCam,"Smirking RIGHT",(0,35),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,255),3) 
            send_cmd("RR")
            print("Smirking Right")
        elif Neutral == True:
            cv2.putText(flipCam,"Neutral",(0,35),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,255),3) 
            send_cmd("X")
            print("Looking Neutral")
        elif looking_up == True:
            cv2.putText(flipCam,"Looking Up",(0,35),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,255),3) 
            send_cmd("F")
            print("Looking Up")
        elif looking_down == True:
            cv2.putText(flipCam,"Looking Down",(0,35),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,255),3) 
            send_cmd("B")
            print("Looking Down")
        elif looking_left == True:
            cv2.putText(flipCam,"Looking Left",(0,35),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,255),3) 
            send_cmd("SL")
            print("Looking Left")
        elif looking_right == True:
            cv2.putText(flipCam,"Looking Right",(0,35),cv2.FONT_HERSHEY_COMPLEX,1.5,(255,0,255),3) 
            print("Looking Right")
            send_cmd("SR")

        return()
    
  
    
    eyeLogic()
    logic_smirking()
    state_machine()


    
    

            


    cv2.imshow('WebCam', flipCam)
    if cv2.waitKey(1) & 0xFF == ord('x'):
        send_cmd("X")
        break


flipCam.release() #clean up
cv2.destroyAllWindows() #clean upt