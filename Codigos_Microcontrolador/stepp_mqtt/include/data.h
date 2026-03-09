#include <Arduino.h>

const char *ssid = "CLARO_h9hU3j";
const char *password = "7474FB19FD";
const char *mqtt_server = "192.168.1.136";
const char *topic_sub = "/suscribirse";
const char *topic_pub = "/saludo";
const char *topic_electroiman = "/electroiman";

const int pasosPorRevolucion = 1600;

// Pinea para los motores STEP-DIR
#define STEP_M1 27
#define DIR_M1 14

#define STEP_M2 25
#define DIR_M2 26

#define STEP_M3 32
#define DIR_M3 33

#define STEP_M4 16
#define DIR_M4 4

#define STEP_M5 18
#define DIR_M5 17

#define STEP_M6 23
#define DIR_M6 19

// Pin electroiman
#define ELECTROIMAN 13
