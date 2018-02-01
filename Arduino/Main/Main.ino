#include <SoftwareSerial.h>
#include <EEPROM.h>
#include <ESP8266WiFi.h>
//Initialize the pins that read bluetooth
SoftwareSerial Sserial(D6, D7);

//Initialize pins for the LED and the button
constexpr auto bled_pin = D4;
constexpr auto button_pin = D2;

//Initialize the pin for the sensor
constexpr auto sensor_pin = A0;

//Define EEPROM size in bytes
constexpr const uint16_t EEPROM_SIZE = 512;

//Boolean that tells the system if a warning has to be sent.
bool trigger = false;

// Strings that store general data. put here because they would be out of socope if defined in the Setup functien
// Or would constanly be recreated if defined inside the loop function.
String bluetooth_data;
String ssid;
String pass;
String sensorname;
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

enum SensorTypes {
  level=0,
  presence,
};

// Contains state of the state machine default stat is startup
States state = States::startup;

// Sensortype for clarity
SensorTypes sensortype = SensorTypes::level;

//integer that contains the status of the wifi module
int status = WL_IDLE_STATUS;

//Initialize the wifi client and set the hub hostname.
WiFiClient client;
String server = "rpi-waterschade-hub";

bool connect_wifi(){
  WiFi.begin(ssid.c_str(), pass.c_str());
  Serial.print("Connecting to ");
  Serial.print(ssid);
  Serial.print(" with pass ");
  Serial.print(pass);
  uint8_t i = 0;
  
  while (WiFi.status() != WL_CONNECTED && i++ < 50){
    Serial.print("could not connect ");
    Serial.print(i);
    Serial.println(" out of 50 attempts\n");
    delay(500);
  }
  delay(10000);
  if (i > 50){
    return false;
  }
  return true;
}

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
pinMode(sensor_pin, INPUT);
digitalWrite(bled_pin, LOW);
Serial.println("\nSetup done\n\n\n");
}

void loop() {
delay(1000);
//Serial.print("Loop");
//Serial.println(state);
if (state == States::idle){
 client.stop();
 Serial.println("state = idle");
 digitalWrite(bled_pin, LOW);
 ESP.deepSleep(10e6);
 
}
  
if (state == States::startup){
  Serial.println("state = startup");
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
  Serial.println("state = reading bluetooth");
  bluetooth_data = ReadBluetooth();
  if (bluetooth_data.length() > 0){
    state = States::writing_eeprom;
    //Serial.println("going to write");
  } else {
    //Serial.println("going to read");
    state = States::reading_eeprom;
  }
}

if (state == States::reading_eeprom){
  Serial.println("state = reading eeprom");
  //Serial.println("hallo");
  //Serial.flush();
 // String Tdata = "Pizza\r\npizza321\r\nSensor1\r\n";
  String Tdata = Read_EEPROM();
  uint16_t point1 = Tdata.indexOf('\n');
  uint16_t point2 = Tdata.indexOf('\n', point1 + 1);
  uint16_t point3 = Tdata.indexOf('\n', point2 + 1);
  
  
  ssid = Tdata.substring(0, point1);
  pass = Tdata.substring(point1 + 1, point2);
  //pass = "pizza321";
  sensorname = Tdata.substring(point2 + 1, point3);
    
  Serial.println("did the reading eeprom");
  state = States::reading_sensor;
}

if (state == States::reading_sensor){
  Serial.println("state = reading sensor");
  int val = 0;
    for (int i = 0; i < 10; i++){
      val += analogRead(sensor_pin);
      delay(100);
    }
  if (sensortype == SensorTypes::level){
    if ((val / 10) > 300){
     trigger = true;  
    }
  if (sensortype == SensorTypes::presence)
    if (val > 5){
      trigger = true;
    }
  }
  state = States::connecting_to_network;
}

if (state == States::writing_eeprom){
  Serial.println("state = writing eeprom");
  Write_EEPROM(bluetooth_data);
  state = States::reading_eeprom;
  Serial.println("did the writing eeprom");
}

if (state == States::connecting_to_network){
  Serial.println("state = connecting to network");
  if (connect_wifi()){
    state = States::sending_data;
  } else {
    Serial.println("cant connect to network");
    state = States::idle;
  }
}

if (state == States::sending_data){
  Serial.println("state = sending data");
  String tmp;
  if (trigger){
    tmp = sensorname + " 1";
  } else {
    tmp = sensorname + " 0";
  }
  Serial.println(tmp);
  if (client.connect(server, 5005)){
    Serial.println("actual sending");
    client.write(tmp.c_str());
  } else {
    Serial.println("cant connect to hub");
   // state = States::error;
  }
  state = States::idle;
}
//if (state == States::error){
//  for (int i = 0; i < 50; i++){
//    digitalWrite(bled_pin, HIGH);
//    delay(200);
//    digitalWrite(bled_pint, LOW)
//  }
//}
}
