#include <Arduino.h>
#include <WiFi.h>
 
const char* ssid = "BreezeHill999";
const char* password =  "0806-449";
 
const uint16_t port = 23456;
const char * host = "192.168.0.15";
int iCnt = 999;
bool bStartPub = false;
const char zGreetingSig[10] = { 0xFF, 0, 0, 0, 0, 0, 0, 0, 1, 0x7F };
const char zGreetingVer[2]  = { 3, 0};
const char zGreetingEnd[52] = { 'N','U','L','L',  0,0,0 };
const char zReadyPUB[27]    = { 0x04,0x19,0x05,0x52,0x45,0x41,0x44,0x59,0x0B,0x53, 
                                0x6F,0x63,0x6B,0x65,0x74,0x2D,0x54,0x79,0x70,0x65,0x00,0x00,0x00,
                                0x03,0x50,0x55,0x42
                              };
const char zReadySUB[27]    = { 0x04,0x19,0x05,0x52,0x45,0x41,0x44,0x59,0x0B,0x53, 
                                0x6F,0x63,0x6B,0x65,0x74,0x2D,0x54,0x79,0x70,0x65,0x00,0x00,0x00,
                                0x03,0x53,0x55,0x42
                              };                              
const char zSubStart[3]     = {0x00, 0x01, 0x01};       
char zMsgHead[2]            = {0x00, 0x00};                  
char zBuf[256];

void setup()
{
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
    }
  Serial.print("\nWiFi connected with IP: ");
  Serial.println(WiFi.localIP());
}
 
static long lLast=0; 
void loop()
{
    WiFiClient client;
    if (!client.connect(host, port)) {
        Serial.println("Connection to host failed"); 
        delay(1000);
        return;
        }
    Serial.printf("\nConnected to %s:%d successful!\n\n", host, port);
    client.write(zGreetingSig, sizeof(zGreetingSig));
    while (client.connected()) {
      int iBytes = client.readBytes(zBuf, 16); //read data into zBuf
      if (iBytes) {  
        Serial.printf("[%02d] ", iBytes);
        for (int i=0;i<iBytes;i++) {
          Serial.printf("|%02X", zBuf[i]);
          }
        Serial.println("|");     
        //Check zGreeting-------------------------------------------  
        if (memcmp(zBuf, zGreetingSig, sizeof(zGreetingSig)) == 0) {
          Serial.println("Got zGreeting!");
          client.write(zGreetingVer, sizeof(zGreetingVer)); //Send Ver
          client.write(zGreetingEnd, sizeof(zGreetingEnd)); //Send Mech
          client.write(zReadyPUB, sizeof(zReadyPUB));       //Send Ready PUB 
          }
        if (memcmp(zBuf, zSubStart, sizeof(zSubStart)) == 0) { //Got SubStart
          Serial.println("Got zSubStart!");   
          bStartPub = true;
          }   
        }       
      if (bStartPub && ((millis()-lLast)>1000) ) { //Start publish from here
        lLast = millis();
        char msg[64];
        sprintf(msg, "zMessage-%04d", iCnt++);
        zMsgHead[1] = strlen(msg);
        client.write(zMsgHead, sizeof(zMsgHead));
        client.write(msg, strlen(msg)+2);
        Serial.println(msg);
        }    
      }    
    Serial.println("Disconnecting...");
    client.stop();
}