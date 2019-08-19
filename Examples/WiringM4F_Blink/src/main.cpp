/*
    PlatformIO - Arduino 2019 Georgi Angelov
    https://github.com/Wiz-IO
    http://www.wizio.eu/
 */

#include <Wiring.h>

void setup()
{
    Serial.begin(); // 115200-8-N-1 ... need more info about uart
    Serial.println("\nWiring MT3620 Cortex-M4F 2019 Georgi Angelov");
    pinMode(LED_RED, OUTPUT);
    Serial.printf("SETUP %d\n", 42);
}

void loop()
{
    static int c = 0;
    Serial.printf("millis() = %u\n", millis());

    uint32_t adc = analogRead(0);
    uint32_t mV = (adc * 2500) / 0xFFF;
    Serial.printf("analogRead() = %u.%u\n", adc / 1000, mV % 1000);

    digitalWrite(LED_RED, 1 & c++);
    delay(1000);
}
