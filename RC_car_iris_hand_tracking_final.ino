#include <WiFi.h>
#include <WiFiUdp.h>
String ssid = "ZentinelY2K";
String password = "M8!rTz#4qLpX92vB2i#x";
WiFiUDP udp;
unsigned int localPort = 4210; //same as python in order to listen
unsigned int remotePort = 4211;  // SECOND_esp32 bridge listens here
IPAddress ESP32_B_IP(10, 253, 27, 146); //10.253.27.146
//LeftMotors L2998N
const int ENA_LEFT = 17;
const int IN1_LEFT = 18;
const int IN2_LEFT = 19;

const int IN3_LEFT = 21;
const int IN4_LEFT = 22;
const int ENB_LEFT = 23;

//RightMotors L298N
const int ENA_RIGHT = 26;
const int IN1_RIGHT = 25;
const int IN2_RIGHT = 16;

const int IN3_RIGHT = 32;
const int IN4_RIGHT = 14;
const int ENB_RIGHT = 27; //CHANGE THIS SAME AS ENA_RIGHT WHEN YOU GET HOME AFTER SCHOOL 


bool can_move = true;
bool go_180 = false;
bool go_75= false;
bool go_max = false;

void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200);
  
  WiFi.begin(ssid, password);

  Serial.println("Connecting: ");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  udp.begin(localPort); 
  Serial.println(WiFi.localIP());

  pinMode(ENA_LEFT,OUTPUT);
  pinMode(IN1_LEFT,OUTPUT);
  pinMode(IN2_LEFT,OUTPUT);

  pinMode(IN3_LEFT,OUTPUT);
  pinMode(IN4_LEFT,OUTPUT);
  pinMode(ENB_LEFT,OUTPUT);
  
  pinMode(ENA_RIGHT,OUTPUT);
  pinMode(IN1_RIGHT,OUTPUT);
  pinMode(IN2_RIGHT,OUTPUT);
  
  pinMode(IN3_RIGHT,OUTPUT);
  pinMode(IN4_RIGHT,OUTPUT);
  pinMode(ENB_RIGHT,OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  int command_recieve = udp.parsePacket(); //check if letter has arrived
  if(command_recieve){
    char packetBuffer[255]; //read 255 bytes max
    int len = udp.read(packetBuffer,255);
    if(len > 0){
      packetBuffer[len] = 0; //strings end with \0 so we cut it for safe transition
    }
    String COMMAND_LETTER = String(packetBuffer);
    Serial.println(COMMAND_LETTER);
    String last_cmd = COMMAND_LETTER;
    Serial.println(COMMAND_LETTER);
    if(COMMAND_LETTER == "Red"){
      stopCar();
      can_move = false;
      go_180  = false;
      go_75 = false;
      go_max = false;
    }
    else if (COMMAND_LETTER == "SP_RL"){
      rotateLeft();
      delay(900);
      stopCar();
    }
    else if(COMMAND_LETTER == "SP_RR"){
      rotateRight();
      delay(900);
      stopCar();

    }
    else if(COMMAND_LETTER == "SP_B"){
        moveBackwards(128);
        delay(1000);
        stopCar();
    }
    else if (COMMAND_LETTER == "Yellow"){
      can_move = true;
      go_180 = false;
      go_75 = true;
      go_max = false;
    }
    else if (COMMAND_LETTER == "Green"){
      can_move = true;
      go_180 = false;
      go_75 = false;
      go_max = true;
    }
    else if (go_max == true && COMMAND_LETTER == "F"  && can_move == true){
      moveForward(255);
    }
    else if (go_75 == true && COMMAND_LETTER == "F" && can_move == true){
      moveForward(128);
    }
    else if (COMMAND_LETTER == "F" && can_move == true){
      moveForward(255);
    }
    else if (COMMAND_LETTER == "X" && can_move == true){
      stopCar();
    }
    else if (COMMAND_LETTER == "B" && can_move == true){
      moveBackwards(255);
    }
    else if (COMMAND_LETTER == "RL" && can_move == true){
      rotateLeft();
    }
    else if (COMMAND_LETTER == "RR" && can_move == true){
      rotateRight();
    }
    else if (COMMAND_LETTER == "SL" && can_move == true){
      strafeLeft();
    }
    else if (COMMAND_LETTER == "SR" && can_move == true){
      strafeRight();
    }
    else if (COMMAND_LETTER == "B" && can_move == true){
      moveBackwards(255);
    }

    
  }
 

}

void moveForward(double speedForward){
  digitalWrite(IN1_LEFT,HIGH);
  digitalWrite(IN2_LEFT,LOW);

  digitalWrite(IN3_LEFT,HIGH);
  digitalWrite(IN4_LEFT,LOW);

  digitalWrite(IN1_RIGHT,HIGH);
  digitalWrite(IN2_RIGHT,LOW);

  digitalWrite(IN3_RIGHT,HIGH);
  digitalWrite(IN4_RIGHT,LOW);

  analogWrite(ENA_LEFT,speedForward);
  analogWrite(ENB_LEFT,speedForward);

  analogWrite(ENA_RIGHT,speedForward);
  analogWrite(ENB_RIGHT,speedForward);





}

void moveBackwards(double speedBackwards){
  digitalWrite(IN1_LEFT,LOW);
  digitalWrite(IN2_LEFT,HIGH);

  digitalWrite(IN3_LEFT,LOW);
  digitalWrite(IN4_LEFT,HIGH);

  digitalWrite(IN1_RIGHT,LOW);
  digitalWrite(IN2_RIGHT,HIGH);

  digitalWrite(IN3_RIGHT,LOW);
  digitalWrite(IN4_RIGHT,HIGH);

  analogWrite(ENA_LEFT,speedBackwards);
  analogWrite(ENB_LEFT,speedBackwards);

  analogWrite(ENA_RIGHT,speedBackwards);
  analogWrite(ENB_RIGHT,speedBackwards);


}

void stopCar(){
  digitalWrite(IN1_LEFT,LOW);
  digitalWrite(IN2_LEFT,LOW);

  digitalWrite(IN3_LEFT,LOW);
  digitalWrite(IN4_LEFT,LOW);

  digitalWrite(IN1_RIGHT,LOW);
  digitalWrite(IN2_RIGHT,LOW);

  digitalWrite(IN3_RIGHT,LOW);
  digitalWrite(IN4_RIGHT,LOW);

  analogWrite(ENA_LEFT,0);
  analogWrite(ENB_LEFT,0);

  analogWrite(ENA_RIGHT,0);
  analogWrite(ENB_RIGHT,0);



}

void strafeLeft(){
  digitalWrite(IN1_LEFT,LOW);
  digitalWrite(IN2_LEFT,HIGH);

  digitalWrite(IN3_LEFT,HIGH);
  digitalWrite(IN4_LEFT,LOW);

  digitalWrite(IN1_RIGHT,LOW);
  digitalWrite(IN2_RIGHT,HIGH);

  digitalWrite(IN3_RIGHT,HIGH);
  digitalWrite(IN4_RIGHT,LOW);

  analogWrite(ENA_LEFT,225);
  analogWrite(ENB_LEFT,225);

  analogWrite(ENA_RIGHT,225);
  analogWrite(ENB_RIGHT,225);



}

void strafeRight(){
  digitalWrite(IN1_LEFT,HIGH);
  digitalWrite(IN2_LEFT,LOW);

  digitalWrite(IN3_LEFT,LOW);
  digitalWrite(IN4_LEFT,HIGH);

  digitalWrite(IN1_RIGHT,HIGH);
  digitalWrite(IN2_RIGHT,LOW);

  digitalWrite(IN3_RIGHT,LOW);
  digitalWrite(IN4_RIGHT,HIGH);

  analogWrite(ENA_LEFT,225);
  analogWrite(ENB_LEFT,225);

  analogWrite(ENA_RIGHT,225);
  analogWrite(ENB_RIGHT,225);



}

void rotateLeft(){
  digitalWrite(IN1_LEFT,LOW);
  digitalWrite(IN2_LEFT,HIGH);

  digitalWrite(IN3_LEFT,LOW);
  digitalWrite(IN4_LEFT,HIGH);

  digitalWrite(IN1_RIGHT,HIGH);
  digitalWrite(IN2_RIGHT,LOW);

  digitalWrite(IN3_RIGHT,HIGH);
  digitalWrite(IN4_RIGHT,LOW);

  analogWrite(ENA_LEFT,135);
  analogWrite(ENB_LEFT,135);

  analogWrite(ENA_RIGHT,135);
  analogWrite(ENB_RIGHT,135);

}

void rotateRight(){
  digitalWrite(IN1_LEFT,HIGH);
  digitalWrite(IN2_LEFT,LOW);

  digitalWrite(IN3_LEFT,HIGH);
  digitalWrite(IN4_LEFT,LOW);

  digitalWrite(IN1_RIGHT,LOW);
  digitalWrite(IN2_RIGHT,HIGH);

  digitalWrite(IN3_RIGHT,LOW);
  digitalWrite(IN4_RIGHT,HIGH);

  analogWrite(ENA_LEFT,135);
  analogWrite(ENB_LEFT,135);

  analogWrite(ENA_RIGHT,135);
  analogWrite(ENB_RIGHT,135);

}

