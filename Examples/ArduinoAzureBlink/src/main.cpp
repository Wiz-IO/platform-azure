/*  
    PlatformIO - Arduino 2019 Georgi Angelov
    https://github.com/Wiz-IO
    http://www.wizio.eu/
 */
#include <Arduino.h>

void setup()
{
    Serial.begin(115200);
    Serial.println("\nAzure Sphere 2019 Georgi Angelov");
    Serial.println("Arduino - Hello World - PlatformIO");
    pinMode(LED_GREEN, OUTPUT);
    pinMode(LED_RED, OUTPUT);
    pinMode(LED_BLUE, OUTPUT);
    Serial.println("Azure Sphere MT3620 Starter AES-MS-MT3620-SK-G by Avnet");
}

void loop()
{
    Serial.printf("Loop %u\n", seconds());
#define T 500
    digitalWrite(LED_GREEN, 1);
    delay(T);
    digitalWrite(LED_GREEN, 0);
    delay(T);
    digitalWrite(LED_RED, 1);
    delay(T);
    digitalWrite(LED_RED, 0);
    delay(T);
    digitalWrite(LED_BLUE, 1);
    delay(T);
    digitalWrite(LED_BLUE, 0);
    delay(T);
}