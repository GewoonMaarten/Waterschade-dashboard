#include <EEPROM.h>

int raddr=0;
int cnt=0;
int waddr=0;
const int MAX_N = 50;
const byte var = 'b';
const int SIZE = 512;

void setup() {
Serial.begin(115200);
delay(1000);
EEPROM.begin(SIZE);
if((char)EEPROM.read(0) == var){
  Serial.println("not writing character");
} else {
  Serial.println("Writing character");
  EEPROM.write(0, var);
}
Serial.println((char)EEPROM.read(0));
EEPROM.end();
//delay(1000);
//EEPROM.begin(SIZE);
//if ((byte)EEPROM.read(0)!=NUMBER){
//  Serial.println("Empty. Will write now the number " + NUMBER);
//  //Serial.flush();
//  for (int n=0;n<MAX_N;n++){
//    EEPROM.write(waddr,NUMBER);
//    waddr++;
//  }
//}
//EEPROM.end();
//waddr=0;
}

void loop() {
//  Serial.println("");
//  //Serial.flush();
//  cnt++;
//  raddr=0;
//  if (cnt>10) {ESP.restart();}
//  
//  for (int n=0;n<MAX_N;n++){
//    Serial.print(EEPROM.read(raddr));
//    Serial.print(' ');
//    raddr++;
//  }
//  //Serial.flush();
//  EEPROM.end();
//  delay(200);
}
