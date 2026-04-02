# Title
BioSync - Translating Biological Inputs into Robotic outputs | A solution to expensive Biometric software for human-machine interfaces

# Abstract 
BioSync is a project that started in October 29 2025, this, being my first time interacting with Electronics, mostly Arduino-related software and hardware, the goal being to develop a program capable of turning Biological inputs (such as hand gestures, gaze with iris, and facial expression) to robotic outputs (an RC car). This project has come a long way, and officially came to an end on March 29 2026. These 5 months of restless work and iteration has laid the fundations for my knowledge in Robotics, and greatly improved my programming and critical-thinking skills, a project that im proud of.

# Awards🥇
BioSync was developed during my freshman year, where I presented it at my school fair, winning first place in the category of Robotics & Intelligent Machines, where I soon got moved to participate on the Sun Country Regional Fair (El Paso) where I competed against all public,private,and charter school districts in El Paso in my category, also winning first place in Robotics & Intelligent Machines, this, led me to participate at the Texas Science & Engineering Fair (TX-SEF).

# Documentation
Unfortunetely, Biosync was developed far before I took the grasp of Github, and, therefore, lacks complete code history, although, there are different sources to take a closer look at my project, some of these sources are a Powerpoint presentation, the source code (which contains comments and Doc strings), and this ReadMe.

# Framworks Used and Materials
To achieve hand detection, iris tracking, and facial expression classification, I decided to use Python as my base programming language, along with two libraries: Mediapipe & OpenCV For the RC car I used the Arduino IDE to program both ESP32's, and a basic chassis with wheels for movement

# How does it work? - A Brief Overview

# Gesture/Gaze/Facial Classification and Detection
BioSync, as previously mentioned, uses OpenCV and Mediapipe, OpenCV acts as the 'camera' where it takes multiple pictures per second, called frames, MediaPipe in this case tracks the different landmarks, whether it is your hand(hand.mesh_cords) or face(face.mesh_cords), the landmarks give specific positions (x and y) which we can use to classify different gestures, for this, we use distances & ratios, for example:
Let's say you want to detect when someone is looking left, you can compare the distance between the left corner of your eyeball and the iris, if the distance decreases below a threshold, that means the person is looking left, although, this presents a problem, if you move far from the camera or closer, those readings become unstable, therefore I implemented ratios, which means we compare two distances (such as the distance from the right corner of your eyeball to the iris) by dividing the distance we want to track by the one we're comparing to, since, as one increases, the other one does too, as one decreases so does the other, giving us stable readings we can use to hardcode different gestures and classify them. 

# Robotic Output
The RC car uses a dual-controller system, with two ESP32's, one is responsible for recieving Python commands and taking

