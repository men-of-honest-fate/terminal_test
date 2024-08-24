#include "setup.h"

void setup() {
  initialazeScreenAndCamera();
 Serial.begin(9600);
}

void loop() {
 char buffer[] = {' ',' ',' ',' ',' ',' ',' '}; // Receive up to 7 bytes
 while (!Serial.available()); // Wait for characters
 Serial.readBytesUntil('\n', buffer, 7);
 int incomingValue = atoi(buffer);
 
 for (int i = 0; i < 7; i++){
  if (buffer[i] != ' '){
    Serial.println(buffer[i]);
  }
  
 }
 processFrame();
}