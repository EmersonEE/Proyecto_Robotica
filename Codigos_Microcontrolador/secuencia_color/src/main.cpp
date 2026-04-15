
#include "Esp.h"
#include "HardwareSerial.h"
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <FastLED.h>
#include <PubSubClient.h>

#define LED_PIN D4
#define RELAY_PIN D5
#define NUM_LEDS 128
#define LED_TYPE WS2812B
#define COLOR_ORDER GRB

CRGB leds[NUM_LEDS];

const char *ssid = "CLARO_h9hU3j";
const char *password = "7474FB19FD";
const char *mqtt_server = "192.168.1.136";
const int mqtt_port = 1883;
const char *topic_leds = "/ws2812";
const char *topic_rele = "/rele";

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastReconnectAttempt = 0;
unsigned long lastLedUpdate = 0;
bool mqttConnected = false;
bool relayState = false;

CRGB colorActual = CRGB::Black;

void cambiarColor(CRGB color) {
  if (colorActual == color)
    return;
  colorActual = color;
  fill_solid(leds, NUM_LEDS, color);
  FastLED.show();
}

void callback(char *topic, byte *payload, unsigned int length) {
  // Manejar tópico de LEDs existente
  if (strcmp(topic, topic_leds) == 0) {
    if (length < 1)
      return;
    char mensaje = (char)payload[0];

    switch (mensaje) {
    case '1':
      cambiarColor(CRGB::Red);
      Serial.println("🔴 LED ROJO");
      break;
    case '2':
      cambiarColor(CRGB::Blue);
      Serial.println("🔵 LED AZUL");
      break;
    case '3':
      cambiarColor(CRGB::Yellow);
      Serial.println("🟡 LED AMARILLO");
      break;
    case '0':
      cambiarColor(CRGB::Black);
      Serial.println("⚫ LED APAGADO");
      break;
    default:
      Serial.println("❌ Comando desconocido");
      return;
    }

    char confirmacion[20];
    sprintf(confirmacion, "LED:%c", mensaje);
    client.publish("/led_status", confirmacion);
  }

  // ✅ NUEVO: Manejar tópico /rele
  else if (strcmp(topic, topic_rele) == 0) {
    // Convertir payload a String para comparar fácilmente
    String comando = "";
    for (unsigned int i = 0; i < length; i++) {
      comando += (char)payload[i];
    }
    comando.trim(); // Eliminar espacios o saltos de línea

    if (comando == "START") {
      relayState = true;
      digitalWrite(RELAY_PIN, HIGH); // Encender LED/rele
      Serial.println("🔌 RELE: START (ENCENDIDO)");
      client.publish("/rele_status", "ON");
    } else if (comando == "STOP") {
      relayState = false;
      digitalWrite(RELAY_PIN, LOW); // Apagar LED/rele
      Serial.println("🔌 RELE: STOP (APAGADO)");
      client.publish("/rele_status", "OFF");
    } else {
      Serial.print("❌ Comando /rele no válido: ");
      Serial.println(comando);
      client.publish("/rele_status", "ERROR");
    }
  }
}
void setup_wifi() {
  Serial.print("📡 Conectando a WiFi");
  WiFi.mode(WIFI_STA);
  WiFi.setSleepMode(WIFI_NONE_SLEEP); // Desactivar ahorro de energía
  WiFi.begin(ssid, password);

  int intentos = 0;
  while (WiFi.status() != WL_CONNECTED && intentos < 20) {
    delay(500);
    Serial.print(".");
    intentos++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ WiFi conectado");
    Serial.print("📡 IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n❌ Error WiFi");
  }
}

void reconnect() {
  if (millis() - lastReconnectAttempt < 5000) {
    return;
  }

  lastReconnectAttempt = millis();
  Serial.print("🔄 Intentando conexión MQTT...");

  String clientId = "ESP8266_LED_";
  clientId += String(random(0xffff), HEX);

  if (client.connect(clientId.c_str())) {
    Serial.println(" ✅ Conectado");
    client.subscribe(topic_leds);
    client.subscribe(topic_rele);
    mqttConnected = true;

    client.publish("/led_status", "CONNECTED");
    client.publish("/rele_status", relayState ? "ON" : "OFF");

    char colorMsg = '0';
    if (colorActual == CRGB::Red)
      colorMsg = '1';
    else if (colorActual == CRGB::Blue)
      colorMsg = '2';
    else if (colorActual == CRGB::Yellow)
      colorMsg = '3';
    char statusMsg[20];
    sprintf(statusMsg, "RECONNECTED:%c", colorMsg);
    client.publish("/led_status", statusMsg);
  } else {
    Serial.println(" ❌ Falló");
    mqttConnected = false;
  }
}

void setup() {
  Serial.begin(115200);
  delay(100);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);

  Serial.println("\n\n🎨 Sistema LED MQTT Iniciado");
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  FastLED.setBrightness(100);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, 2000);
  FastLED.clear();
  FastLED.show();
  cambiarColor(CRGB::Green);
  delay(500);
  cambiarColor(CRGB::Black);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  client.setKeepAlive(60);
  client.setBufferSize(256);
  client.subscribe(topic_rele);
  Serial.println("✅ Sistema listo");
  Serial.println(
      "🎨 Comandos disponibles: 1=Rojo, 2=Azul, 3=Amarillo, 0=Apagar");
}
void loop() {
  if (!client.connected()) {
    if (mqttConnected) {
      Serial.println("⚠️ Conexión MQTT perdida");
      mqttConnected = false;
    }
    reconnect();
  } else {
    client.loop();
  }
  delay(10);
  static unsigned long lastDebug = 0;
  if (millis() - lastDebug > 5000) {
    lastDebug = millis();
    if (client.connected()) {
      Serial.print("✅ MQTT Activo - ");
      if (colorActual == CRGB::Red)
        Serial.println("LED: ROJO");
      else if (colorActual == CRGB::Blue)
        Serial.println("LED: AZUL");
      else if (colorActual == CRGB::Yellow)
        Serial.println("LED: AMARILLO");
      else
        Serial.println("LED: APAGADO");
    } else {
      Serial.println("⚠️ MQTT Desconectado");
    }
  }
}
