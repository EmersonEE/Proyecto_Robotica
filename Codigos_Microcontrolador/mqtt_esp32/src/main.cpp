#include "HardwareSerial.h"
#include "MQTTClient.h"
#include "WString.h"
#include "WiFiClient.h"
#include "data.h"
#include "esp32-hal.h"
#include "esp_wifi_types.h"
#include <AccelStepper.h>
#include <Arduino.h>
#include <MQTT.h>
#include <PubSubClient.h>
#include <WiFi.h>
#include <WiFiMulti.h>
WiFiMulti wifiMulti;

WiFiClient net;
MQTTClient clienteMQTT;
int pot = 33;
int lectura = 0;
unsigned long tiempoAnterior = 0;
unsigned long ultimoReintento = 0;
const unsigned long intervaloReintento = 5000; // 5 segundos
String payload_anterior = "";
int LED_OK = 14;
int LED_ERROR = 12;
int BUZZER = 27;
unsigned long tiempoDeApagado = 0;
bool esperandoApagar = false;
void encenderLed(const String &payload) {
  switch (payload.toInt()) {
  case 1:
    Serial.println("Se envio el 1");
    break;
  case 2:
    Serial.println(" Se envio el 2");
    break;

  default:
    Serial.println("No se envio nada ");
  }
}

void mensajeMQTT(String topic, String payload) {
  if (topic == "/suscribirse") {
    encenderLed(payload);
  } else {
    Serial.println("Topic no encontrado");
  }
}

void conectar() {
  const unsigned long timeoutWiFi = 30000; // 30 segundos timeout
  unsigned long inicio = millis();

  Serial.print("Conectando con WiFi...");
  while (wifiMulti.run() != WL_CONNECTED && millis() - inicio < timeoutWiFi) {
    // Feedback visual mejorado
    static uint8_t counter = 0;
    Serial.print(".");
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    delay(250 + (counter++ % 3) * 100); // Patrón de espera variable
  }

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("\nFallo en conexión WiFi");
    ESP.restart(); // O manejar de otra manera
    return;
  }

  Serial.println("\nConectado a WiFi: " + WiFi.SSID());
  Serial.println("IP local: " + WiFi.localIP().toString());

  Serial.print("Conectando a MQTT...");
  while (!clienteMQTT.connect(NombreESP)) {
    Serial.print("*");
    digitalWrite(LED_BUILTIN, HIGH);
    delay(200);
    digitalWrite(LED_BUILTIN, LOW);
    delay(200);
  }
  Serial.println("\nConectado a MQTT");

  // ✅ Suscripciones
  clienteMQTT.subscribe("/suscribirse");
}

void setup() {

  Serial.begin(115200);
  wifiMulti.addAP(ssid_1, password_1);
  wifiMulti.addAP(ssid_2, password_2);
  clienteMQTT.begin(BrokerMQTT, net);
  clienteMQTT.onMessage(mensajeMQTT);
}

void loop() {

  clienteMQTT.loop();
  delay(10);
  if (!clienteMQTT.connected()) {
    if (millis() - ultimoReintento > intervaloReintento) {
      ultimoReintento = millis();
      conectar();
    }
    return;
  }
}
