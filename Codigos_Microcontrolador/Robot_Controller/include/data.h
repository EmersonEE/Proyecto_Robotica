#ifndef DATA_H
#define DATA_H

#include <Arduino.h>
#include <cstdint>

// ==================== CREDENCIALES ====================
// ✅ Usar 'extern' para declarar (no definir)
extern const char *ssid;
extern const char *password;

// ==================== MQTT ====================
extern const char *mqtt_server;
extern const uint16_t mqtt_port;
extern const char *topic_sub;
extern const char *topic_pub;
extern const char *topic_electroiman;
extern const char *topic_ws2812;
extern const char *topic_estado;

// ==================== PINES ====================
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
#define ROBOT_LISTO 22

// ==================== CONFIGURACIÓN DE MOTORES ====================
extern const long stepsPerRev[6];
extern const float maxSpeed[6];
extern const float acceleration[6];
extern const uint16_t minPulseWidth[6];
extern const bool motorInvertido[6];
extern const float motorMinAngle[6];
extern const float motorMaxAngle[6];

// ==================== PARÁMETROS GENERALES ====================
extern const uint32_t SERIAL_BAUD;
extern const uint16_t WIFI_TIMEOUT_MS;
extern const uint16_t MQTT_RECONNECT_DELAY_BASE;
extern const uint16_t MQTT_MAX_RECONNECT_DELAY;
extern const uint8_t MQTT_MAX_RECONNECT_ATTEMPTS;
extern const uint32_t MOVEMENT_TIMEOUT_MS;
extern const uint16_t DELAY_ENTRE_MOTORES;

// ==================== ESTADO GLOBAL ====================
extern bool robotListo;
extern bool movimientoActivo;
extern float stepsPerDegree[6];
extern float posicionActual[6];

// ==================== DEBUG ====================
#define DEBUG_ENABLED true
#if DEBUG_ENABLED
#define DEBUG_PRINT(x) Serial.print(x)
#define DEBUG_PRINTLN(x) Serial.println(x)
#define DEBUG_PRINTF(...) Serial.printf(__VA_ARGS__)
#else
#define DEBUG_PRINT(x)
#define DEBUG_PRINTLN(x)
#define DEBUG_PRINTF(...)
#endif

#endif // DATA_H
