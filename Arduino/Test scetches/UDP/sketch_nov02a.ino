#include <SPI.h>
#include <ESP8266WiFi.h>
char *ssid = "cracklan";
char *pass = "bruhplsno";

int status = WL_IDLE_STATUS;
char *pihostname = "raspberrypi";
IPAddress server(192,168,43,185);

WiFiClient client;

class StateClass{
  public:
  bool IS_IDLE = true;
  bool IS_CONNECTED = false;
  bool REGISTERING = false;
  bool SENDING_DATA = false;

  StateClass(){}
  
};

void setup() {
//  StateClass State;
//  delay(1000);
//  Serial.begin(115200);
//  Serial.println("\ngonnagotosleep");
//  ESP.deepSleep(10e6);
  Serial.begin(115200);
  WiFi.begin(ssid, pass);
  Serial.print("\nConnecting to "); 
  Serial.println(ssid);
  uint8_t i = 0;
  while (WiFi.status() != WL_CONNECTED && i++ < 50){
    Serial.print("could not connect ");
    Serial.print(i);
    Serial.println(" out of 50 attempts\n");
    delay(500);
  }
  if(i == 21){
    Serial1.print("Could not connect to"); Serial1.println(ssid);
    while(1) delay(500);
  } else {
    Serial.println("Connection established");
    Serial.println("Connecting to hub");
    if (client.connect(pihostname, 5005)){
      Serial.println("Hub connection established");
      Serial.println("Sending data");
      client.write("hello world");
      client.stop();
    } else {
      Serial.println("Could not connect to server");
    }
  }
}

void loop() {
  // put your main code here, to run repeatedly:

}
