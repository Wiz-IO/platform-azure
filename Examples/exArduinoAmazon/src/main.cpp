/*
    Created on: 20.09.2019
    Author: Georgi Angelov
      http://www.wizio.eu/
      https://github.com/Wiz-IO/platform-azure 

    Need: EXPERIMENTAL MODE for SSL/TLS, read here:
      https://github.com/Wiz-IO/platform-azure/wiki/Arduino-INI-file#experimental-mode
*/

#include <Arduino.h>

#include "amazon.h" /* open and edit your AWS settings */

#include <ClientSecure.h> /* need experimental mode to be enabled */
ClientSecure cs;

#define MQTT_PUB_PERIOD_SECONDS (10)
#define MQTT_PUB_TOPIC "outTopic"
#define MQTT_SUB_TOPIC "inTopic"

#include <PubSubClient.h> // by Nick O'Leary
PubSubClient mqtt(AWS_HOST, AWS_PORT, cs);
void callback(char *topic, byte *payload, unsigned int length)
{
  Serial.printf("[MSG] <%s> %.*s", topic, length, payload);
}

void reconnect()
{
  while (!mqtt.connected())
  {
    Serial.println("[MQTT] Connecting to Amazon...");
    if (mqtt.connect("client_arduino"))
    {
      Serial.println("[MQTT] Connected");
      mqtt.publish(MQTT_PUB_TOPIC, "Hello from Azure Sphere 2019");
      mqtt.subscribe(MQTT_SUB_TOPIC);
    }
    else
    {
      Serial.print("[ERROR] MQTT Connect: ");
      Serial.println(mqtt.state());
      delay(60 * 1000); // Wait retrying in ms
    }
  }
}

void setup()
{
  Serial.begin(115200);
  Serial.println("Azure Sphere MQTT Amazon");
  waitWifi();
  delay(1000);
  mqtt.setCallback(callback);
  cs.setCertificate(AWS_CERTIFICATE);
  cs.setPrivateKey(AWS_PRIVATE_KEY);
}

void loop()
{
  static uint32_t t = 0;
  if (!mqtt.connected())
    reconnect();
  mqtt.loop();

  /* sending data to cloud */
  if ((seconds() - t) > MQTT_PUB_PERIOD_SECONDS)
  {
    char buf[256];
    sprintf(buf, "{\"data\":\"%u\"}", millis()); // create test data
    mqtt.publish(MQTT_PUB_TOPIC, buf);
    Serial.println("[MQTT] Data Sent");
    t = seconds();
  }

  if (!mqtt.connected())
    Serial.printf("[ERROR] %d Reconnecting...\n", mqtt.state());
  delay(100);
}