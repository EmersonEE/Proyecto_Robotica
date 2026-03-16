#include "esp32-hal-gpio.h"
#include "esp32-hal.h"
#include <Arduino.h>
#define ELECTROIMAN 13
void setup() { pinMode(ELECTROIMAN, OUTPUT); }

void loop() {

  digitalWrite(ELECTROIMAN, HIGH);
  delay(500);
  digitalWrite(ELECTROIMAN, LOW);
  delay(500);
}
