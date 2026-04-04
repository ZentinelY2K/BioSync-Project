import speech_recognition as sp
import time
import socket #for communication with Arduino IDE
import time as tm #for delay
import math as mt


ESP32_IP = "10.253.27.157" #my ip

Port = 4210

#UDP socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

send_logic_hands = ''

def send_cmd_hands(command):
        global  send_logic_hands
        send_logic_hands = sock.sendto(command.encode(),(ESP32_IP,Port)) 
        return()




recognizer_obj = sp.Recognizer()
mic = sp.Microphone()


with mic as source:
    print("Calibrating for background noise...")
    recognizer_obj.adjust_for_ambient_noise(source, duration=1)

print("System is online. I'm listening in the background...")


def callback(recognizer, audio):
    try:
      
        text = recognizer.recognize_google(audio).lower()
        print(f"Recognized: {text}")
        
        if "x" in text:
            send_cmd_hands('X')
        elif "f" in text:
            send_cmd_hands('F')
        elif "b" in text:
            send_cmd_hands('B')
        elif "s" and "l" in text:
            send_cmd_hands('SL')
        elif "s" and "r" in text:
            send_cmd_hands('SR')
        elif "r" and "l" in text:
            send_cmd_hands('RL')
        elif "r" and "r" in text:
            send_cmd_hands('RR')
        
    except sp.UnknownValueError:
       
        pass 
    except sp.RequestError as e:
        print(f"Network error: {e}")

stop_listening = recognizer_obj.listen_in_background(mic, callback, phrase_time_limit=3)


try:
    while True:
        time.sleep(0.1)  
except KeyboardInterrupt:
    stop_listening(wait_for_stop=False)