// data.cpp - ÚNICO archivo donde se DEFINEN las variables globales
#include "data.h"

// ==================== CREDENCIALES ====================
const char *ssid = "CLARO_h9hU3j";
const char *password = "7474FB19FD";

// ==================== MQTT ====================
const char *mqtt_server = "192.168.1.136";
const uint16_t mqtt_port = 1883;
const char *topic_sub = "/suscribirse";
const char *topic_pub = "/saludo";
const char *topic_electroiman = "/electroiman";
const char *topic_ws2812 = "/ws2812";
const char *topic_estado = "/estado";

// ==================== CONFIGURACIÓN DE MOTORES ====================
const long stepsPerRev[6] = {1600, 1600, 1600, 6400, 3200, 3200};
const float maxSpeed[6] = {1500, 1500, 1500, 1000, 800, 800};
const float acceleration[6] = {600, 600, 600, 400, 300, 300};
const uint16_t minPulseWidth[6] = {2, 2, 2, 5, 5, 5};
const bool motorInvertido[6] = {false, false, false, true, true, false};
const float motorMinAngle[6] = {-360, -360, -360, -360, -360, -360};
const float motorMaxAngle[6] = {360, 360, 360, 360, 360, 360};

// ==================== PARÁMETROS GENERALES ====================
const uint32_t SERIAL_BAUD = 115200;
const uint16_t WIFI_TIMEOUT_MS = 30000;
const uint16_t MQTT_RECONNECT_DELAY_BASE = 2000;
const uint16_t MQTT_MAX_RECONNECT_DELAY = 30000;
const uint8_t MQTT_MAX_RECONNECT_ATTEMPTS = 10;
const uint32_t MOVEMENT_TIMEOUT_MS = 30000;
const uint16_t DELAY_ENTRE_MOTORES = 20;

// ==================== ESTADO GLOBAL ====================
bool robotListo = false;
bool movimientoActivo = false;
float stepsPerDegree[6] = {0};
float posicionActual[6] = {0};
