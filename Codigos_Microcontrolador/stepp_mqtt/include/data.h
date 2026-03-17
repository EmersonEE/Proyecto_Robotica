#include <Arduino.h>

const char *ssid = "CLARO_h9hU3j";
const char *password = "7474FB19FD";

const char *mqtt_server = "192.168.1.136";
const char *topic_sub = "/suscribirse";
const char *topic_pub = "/saludo";
const char *topic_electroiman = "/electroiman";

#define STEP_M1 27
#define DIR_M1 14

#define STEP_M2 25
#define DIR_M2 26

#define STEP_M3 32
#define DIR_M3 33

#define STEP_M4 4
#define DIR_M4 16

#define STEP_M5 17
#define DIR_M5 18

#define STEP_M6 19
#define DIR_M6 23

#define ELECTROIMAN 13

int ordenMotores[6] = {5, 1, 3, 4, 2, 0};
const int DELAY_ENTRE_MOTORES = 100;
const long stepsPerRev[6] = {1600, 1600, 1600, 1600, 3200, 3200};

float stepsPerDegree[6];

float posicionActual[6] = {0, 0, 0, 0, 0, 0};
