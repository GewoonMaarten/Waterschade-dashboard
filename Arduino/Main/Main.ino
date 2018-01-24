#include <SoftwareSerial.h>
SoftwareSerial Sserial(D6, D7);

enum States {
  idle = 0,
  startup,
  reading_bluetooth,
};

States state = States::reading_bluetooth;

String Readbluetooth(){
  Serial.println("startinble");
  int tmp = -1;
  String data;
  int timeout = 20000;
  while(timeout > 0){
    tmp = Sserial.read();
    if (tmp != -1){
      data += (char)tmp;
      timeout++;
    }
    delay(1);
    timeout--;
  }
  Serial.println("endingble");
  return data;
}

void setup() {
delay(1000);
Sserial.begin(9600);
Serial.begin(115200);
Serial.println("\n\n\nab");
Serial.println(state);


}

void loop() {

if (state == States::reading_bluetooth){
  String test;
  Serial.println(test.length());
  String ding = Readbluetooth();
  Serial.println(ding);
  Serial.println(ding.length());
  state = States::idle;
}
  // put your main code here, to run repeatedly

//tmp = Sserial.read();
//if (tmp != -1){
//  ad[indexx++] = (char)tmp;
//Serial.println(ad);
//  Serial.println();
//}
}
