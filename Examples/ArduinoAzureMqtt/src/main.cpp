/*
    PlatformIO - Arduino 2019 Georgi Angelov
    https://github.com/Wiz-IO
    http://www.wizio.eu/
 */

#include <Arduino.h>
#include <applibs/networking.h>
#include <wifiClient.h>
wifiClient cc;

/* 
Chrome - MQTTLens
    https://chrome.google.com/webstore/detail/mqttlens/hemojaaeigabkbcookmlgmdigohjobjm?hl=en

Eclipse    
    https://iot.eclipse.org/getting-started/

Nick O'Leary Library 
    http://knolleary.net    
*/

#include <PubSubClient.h>
PubSubClient mqtt("iot.eclipse.org", 1883, cc); // look app_manifest.json "AllowedConnections"

int led_state = 0;

void callback(char *topic, byte *payload, unsigned int length)
{
  Serial.printf("[MSG] <%s> %.*s\n", topic, length, payload);
}

void reconnect()
{
  while (!mqtt.connected())
  {
    Serial.println("[MQTT] Connecting to Eclipse...");
    char client_id[64];
    snprintf(client_id, 64, "WIZIO_%d", millis()); // create unique mqtt client id
    Serial.printf("[MQTT] ClientID: %s\n", client_id);
    if (mqtt.connect(client_id))
    {
      Serial.println("[MQTT] Connected");
      mqtt.publish("wizio/output", "Hello world");  // PUB
      mqtt.subscribe("wizio/input");                // SUB
    }
    else
    {
      Serial.printf("[ERROR] MQTT Connect: %d", (int)mqtt.state());
      delay(10000); // time wait reconnect
      Serial.println("[MQTT] Reconnecting");
    }
  }
}

void setup()
{
  Serial.begin(115200);
  pinMode(LED_GREEN, OUTPUT);
  Serial.println("\nAzure Sphere 2019 Georgi Angelov");
  Serial.println("Arduino - PubSub - PlatformIO");
  Serial.println("Azure Sphere MT3620 Starter AES-MS-MT3620-SK-G by Avnet");
  Serial.println("Waithing WIFI");
  bool outIsNetworkingReady = 0;
  /* wait wifi */
  if (Networking_IsNetworkingReady(&outIsNetworkingReady) < 0 && 0 == outIsNetworkingReady)
  {
    Serial.print(".");
    digitalWrite(LED_GREEN, led_state);
    led_state ^= 1;
    delay(100);
  }
  mqtt.setCallback(callback);
}

void loop()
{
  static int t = 0;
  if (!mqtt.connected())
    reconnect();
  mqtt.loop();
  if (0 == t % 100)
  {
    digitalWrite(LED_GREEN, led_state); // blink toggle
    led_state ^= 1;
  }
}
