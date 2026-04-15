#include "ws2812mqtt.h"
#include "HardwareSerial.h"
#include "crgb.h"

WS2812MQTT::WS2812MQTT(uint16_t numLeds) {
  _numLeds = numLeds;
  // Creamos el array de LEDs en memoria dinámica
  _leds = new CRGB[_numLeds];
}

void WS2812MQTT::wsinit(uint8_t pin) {
  _pin = pin;
  FastLED.addLeds<WS2812B, 23, GRB>(_leds, _numLeds);
}

void WS2812MQTT::mostrarColor(uint8_t colorId) {
  CRGB color;
  switch (colorId) {
  case 1:
    color = CRGB::Red;
    break;
  case 2:
    color = CRGB::Blue;
    break;
  case 3:
    color = CRGB::Yellow;
    break;
  case 4:
    color = CRGB::Black;
    break;
  default:
    color = CRGB::Black;
    break;
  }

  fill_solid(_leds, _numLeds, color);
  FastLED.show();
}
