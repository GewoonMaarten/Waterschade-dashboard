#include <SoftwareSerial.h>
#include <EEPROM.h>
#include <ESP8266WiFi.h>
//Initialize the pins that read bluetooth
SoftwareSerial Sserial(D6, D7);

//Initialize pins for the LED and the button
constexpr auto bled_pin = D4;
constexpr auto button_pin = D2;

//Define EEPROM size in bytes
constexpr const uint16_t EEPROM_SIZE = 512;

// Strings that store general data. put here because they would be out of socope if defined in the Setup functien
// Or would constanly be recreated if defined inside the loop function.
String bluetooth_data;
String ssid;
String pass;
String pihostname = "pi-waterschade-hub";

// Enum that contains the different states of the state machines to give descriptive names to the states.
enum States {
  idle = 0,
  startup,
  reading_bluetooth,
  reading_eeprom,
  reading_sensor,
  writing_eeprom,
  connecting_to_network,
  sending_data
};

// Contains state of the state machine
States state = States::startup;

//integer that contains the status of the wifi module
int status = WL_IDLE_STATUS

//Initialize the wifi client
WiFiClient client;

String ReadBluetooth(){
  //Serial.println("startinble");
  digitalWrite(bled_pin, HIGH);
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
  digitalWrite(bled_pin, LOW);
  return data;
}

void Write_EEPROM(String data){
  for(uint8_t x = 0; x < data.length(); x++){
     EEPROM.write(x, (byte)data[x]);
  }
  EEPROM.write(data.length(), (byte)'\0');
}

String Read_EEPROM(){
  uint16_t counter = 0;
  String data;
  while((char)EEPROM.read(counter) != '\0'){
     data += (char)EEPROM.read(counter);
     counter++;
  }
  EEPROM.end();
  return data;
}

void setup() {
delay(2000);
Sserial.begin(9600);
Serial.begin(115200);
EEPROM.begin(EEPROM_SIZE);
pinMode(bled_pin, OUTPUT);
pinMode(button_pin, INPUT);
digitalWrite(bled_pin, LOW);
Serial.println("\nSetup done\n\n\n");
}

void loop() {
  
if (state == States::startup){
  int timeout = 10000;
  state = States::reading_eeprom;
  while (timeout > 0){
    if (digitalRead(button_pin)){
      state = States::reading_bluetooth;
      timeout = 0;
    }
    if (timeout % 500 == 0){
      if (digitalRead(bled_pin)){
        digitalWrite(bled_pin, LOW);
      } else {
        digitalWrite(bled_pin, HIGH);
      }
    }
    delay(1);
    timeout--;
  }
  digitalWrite(bled_pin, LOW);
}

if (state == States::reading_bluetooth){
  bluetooth_data = ReadBluetooth();
  if (bluetooth_data.length() > 0){
    state = States::writing_eeprom;
  } else {
    state = States::reading_eeprom;
  }
}

if (state == States::writing_eeprom){
  //Write_EEPROM(bluetooth_data);
  state = States::reading_eeprom;
  Serial.println("did the writing eeprom");
}

if (state == States::reading_eeprom){
  state = States::idle;
  String Tdata = "Pizza\r\npizza123\r\nSensor1\r\n";
  uint16_t point1 = Tdata.indexOf('\r\n');
  uint16_t point2 = Tdata.indexOf('\r\n', point1 + 1);
  uint16_t point3 = Tdata.indexOf('\r\n', point2 + 1);
  
  
  ssid = Tdata.substring(0, point1);
  Tdata.substring(point1 + 1, point2));
  Serial.println(Tdata.substring(point2 + 1, point3));
  
  
  //String data = Read_EEPROM();
  Serial.println("did the reading eeprom");
}


}
