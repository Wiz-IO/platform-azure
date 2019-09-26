/*
  PlatformIO - Arduino 2019 Georgi Angelov
    https://github.com/Wiz-IO/platform-azure
    http://www.wizio.eu/

  More info: https://blynk.io
 */

#include <Arduino.h> 

//#define BLYNK_DEBUG_ALL
#define DEBUG_BLYNK
#define BLYNK_PRINT Serial

#include <BlynkSimpleAzure.h>
BlynkTimer timer;
WidgetLCD lcd(V1);
extern char blynk_auth[];

void sendSensor()
{
  Serial.println("Sensor");

  // Android APP - LCD: SIMPLE
  Blynk.virtualWrite(V5, millis());
  Blynk.virtualWrite(V6, seconds());

  // Android APP - LCD: ADVANCE
  lcd.print(0, 0, "PlatformIO");
  lcd.print(0, 1, "Azure Sphere");
}

void setup()
{
  Serial.begin(115200);
  Serial.printf("\n[APP] BLYNK\n");
  waitWifi();
  Blynk.begin(blynk_auth);
  timer.setInterval(5000, sendSensor);
}

void loop()
{
  Blynk.run();
  timer.run();
}

/*
[APP] BLYNK
[2012] Blynk begin
[2012] 
    ___  __          __
   / _ )/ /_ _____  / /__
  / _  / / // / _ \/  '_/
 /____/_/\_, /_//_/_/\_\
        /___/ v0.6.1 on AzureSphere

[2012] Connecting...
[2013] Connecting to blynk-cloud.com:80
[2093] Ready (ping: 41ms).
[2160] Connected
Sensor
*/