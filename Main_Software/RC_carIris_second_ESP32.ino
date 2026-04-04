#include <WiFi.h>
#include <WiFiUdp.h>
#include <ESP32Servo.h>

Servo ultraSonic;

const char* ssid = "ZentinelY2K";
const char* password = "M8!rTz#4qLpX92vB2i#x";

WiFiUDP udp;
const int trig = 19;
const int echo = 34;
unsigned int localPort = 4211;   // B listens here
unsigned int remotePort = 4210;  // A listens here
const int green = 25;
const int yellow = 17;
const int red = 16;
//21,22 for G
IPAddress ESP32_A_IP(10, 253, 27, 157); //10.253.27.157

void setup() {
  Serial.begin(115200);
  

  ultraSonic.attach(23);
  ultraSonic.write(80);
  pinMode(trig,OUTPUT);
  pinMode(echo,INPUT);
  //LEDs
  pinMode(red,OUTPUT);
  pinMode(yellow,OUTPUT);
  pinMode(green,OUTPUT);
  //wifi and wireless setup
  WiFi.begin(ssid, password);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  udp.begin(localPort);

  Serial.println("\nESP32 B ready");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

}

float objectDetected(){
  digitalWrite(trig,LOW);
  delayMicroseconds(4);
  digitalWrite(trig,HIGH); // send blast
  delayMicroseconds(20);
  digitalWrite(trig,LOW); //recieve blast and stop
  //process bounced off sound
  long duration = pulseIn(echo,HIGH); //pulseIn to recieve it
  float distance = (duration*0.034)/2; 
  return distance;
}

void loop() {
  float distance = objectDetected();
  //Serial.println(distance);
  if (distance <= 25 && distance > 0.00){
       udp.beginPacket(ESP32_A_IP,remotePort);
       udp.print("Red");
       udp.endPacket();
       digitalWrite(red,HIGH);
       digitalWrite(green,LOW);
       digitalWrite(yellow,LOW);
       //safety protocol
       ultraSonic.write(0);
       delay(1200);
       const float distanceRight = objectDetected();
       Serial.println(distanceRight);
       delay(100);
       ultraSonic.write(180);
       delay(1200);
       const float distanceLeft = objectDetected();
       Serial.println(distanceLeft);
       delay(100);
       Serial.println(distanceRight);
       Serial.println(distanceLeft);
       ultraSonic.write(80);
       delay(1200);
       if(distanceRight <= 25 && distanceLeft <= 18 && distanceRight > 0.00 && distanceLeft > 0.00){
        udp.beginPacket(ESP32_A_IP,remotePort);
        Serial.println("Sent");
        udp.print("SP_B");
        udp.endPacket();
        delay(20);
      }
       else if(distanceLeft > distanceRight && distanceLeft > 0.00 && distanceRight > 0.00){
          udp.beginPacket(ESP32_A_IP,remotePort);
          udp.print("SP_RL");
          udp.endPacket();
          delay(20);
       }
       else if (distanceRight >= distanceLeft && distanceLeft > 0.00 && distanceRight > 0.00){
          udp.beginPacket(ESP32_A_IP,remotePort);
          udp.print("SP_RR");
          udp.endPacket();
          delay(20);
      }
    
    delay(3000);
      
  }
  else if (distance <= 70 && distance > 25 && distance > 0.00 ){
       udp.beginPacket(ESP32_A_IP,remotePort);
       udp.print("Yellow");
       udp.endPacket();
       digitalWrite(yellow,HIGH);
       digitalWrite(green,LOW);
       digitalWrite(red,LOW);
  } 
  else if (distance > 70 && distance > 0.00){
    udp.beginPacket(ESP32_A_IP,remotePort);
    udp.print("Green");
    udp.endPacket();
    digitalWrite(green,HIGH);
    digitalWrite(red,LOW);
    digitalWrite(yellow,LOW);
  }

    


      
    
    /*udp.beginPacket(ESP32_A_IP, remotePort);
    udp.print("Reply from B");
    udp.endPacket();*/
  
  
}


