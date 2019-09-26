/*
    PlatformIO - Arduino 2019 Georgi Angelov
    https://github.com/Wiz-IO
    http://www.wizio.eu/

Chrome - MQTTLens
    https://chrome.google.com/webstore/detail/mqttlens/hemojaaeigabkbcookmlgmdigohjobjm?hl=en

Eclipse    
    https://iot.eclipse.org/getting-started/

Nick O'Leary Library 
    http://knolleary.net        
 */

#include <Arduino.h>
#include <applibs/networking.h>
#include <wifiClient.h>
wifiClient cc;
#include <PubSubClient.h>

#define MQTT_PORT 1883
#define ECLIPSE "mqtt.eclipse.org"
//#define ECLIPSE "iot.eclipse.org"

#define MQTT_PUB_PERIOD_SECONDS (30)
#define MQTT_PUB_TOPIC "wizio/outTopic"
#define MQTT_SUB_TOPIC "wizio/inTopic"

PubSubClient mqtt(ECLIPSE, MQTT_PORT, cc); // app_manifest.json "AllowedConnections"

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
    snprintf(client_id, 64, "CLIENT_ID_%d", millis()); // create unique mqtt client id
    Serial.printf("[MQTT] ClientID: %s\n", client_id);
    if (mqtt.connect(client_id))
    {
      Serial.println("[MQTT] Connected");
      mqtt.publish(MQTT_PUB_TOPIC, "Hello world");
      mqtt.subscribe(MQTT_SUB_TOPIC);
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
  Serial.redirect(stderr); // Log_Debug
  Log_Debug("\nAzure Sphere 2019 Georgi Angelov\n");
  Serial.println("Arduino - PubSub - PlatformIO");

  //Log_Debug("%d\n", millis());
  waitWifi(); // ~15 seconds on board reset
  //Log_Debug("%d\n", millis());

  mqtt.setCallback(callback);
  pinMode(LED_GREEN, OUTPUT);
}

void loop()
{
  static uint32_t old = 0;
  static uint32_t blink = 0;
  static int led_state = 0;

  if (!mqtt.connected())
    reconnect();
  mqtt.loop();

  /* sending data to cloud */
  if ((seconds() - old) > MQTT_PUB_PERIOD_SECONDS)
  {
    char buf[256];
    sprintf(buf, "{\"data\":\"%u\"}", millis()); // create test data
    mqtt.publish(MQTT_PUB_TOPIC, buf);
    Log_Debug("[MQTT] Data Sent\n");
    old = seconds();
  }

  if ((millis() - blink) > 200)
  {
    digitalWrite(LED_GREEN, led_state);
    led_state ^= 1;
    blink = millis();
  }
}
