#ifndef __WS2812MQTT__
#define __WS2812MQTT__

#include <FastLED.h>
#include <cstdint>

class WS2812MQTT {
public:
  WS2812MQTT(uint16_t numLeds);
  void wsinit(uint8_t pin);
  void mostrarColor(uint8_t colorId);

private:
  uint16_t _numLeds;
  uint8_t _pin;
  CRGB *_leds;
};

#endif
