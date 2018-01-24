#include <SoftwareSerial.h>
char ad[100];
int tmp = -1;
int indexx = 0;
SoftwareSerial Sserial(D6, D7);

enum States {
  Idle = 0,
  Startup,
  Bluetooth,
};


void setup() {
delay(1000);
Sserial.begin(9600);
Serial.begin(115200);
Serial.println("\n\n\nab");
Serial.println(States::Startup);


}

void loop() {
  // put your main code here, to run repeatedly

//tmp = Sserial.read();
//if (tmp != -1){
//  ad[indexx++] = (char)tmp;
//Serial.println(ad);
//  Serial.println();
//}
}
