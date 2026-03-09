#include "Arduino.h"
#include "data.h"
#include "esp32-hal-gpio.h"
#include <AccelStepper.h>
#include <MultiStepper.h>
#include <PubSubClient.h>
#include <WiFi.h>

WiFiClient espClient;
PubSubClient client(espClient);

// STEP, DIR
AccelStepper m1(1, STEP_M1, DIR_M1);
AccelStepper m2(1, STEP_M2, DIR_M2);
AccelStepper m3(1, STEP_M3, DIR_M3);
AccelStepper m4(1, STEP_M4, DIR_M4);
AccelStepper m5(1, STEP_M5, DIR_M5);
AccelStepper m6(1, STEP_M6, DIR_M6);

MultiStepper grupo;
float posicionActual[6] = {0, 0, 0, 0, 0, 0};
long posiciones[6];

long gradosAPasos(float grados) {
  return (long)(grados * pasosPorRevolucion / 360.0);
}
void moverPose(float g1, float g2, float g3, float g4, float g5, float g6) {

  long p1 = gradosAPasos(g1);
  long p2 = gradosAPasos(g2);
  long p3 = gradosAPasos(g3);
  long p4 = gradosAPasos(g4);
  long p5 = gradosAPasos(g5);
  long p6 = gradosAPasos(g6);

  m1.moveTo(p1);
  m2.moveTo(p2);
  m3.moveTo(p3);
  m4.moveTo(p4);
  m5.moveTo(p5);
  m6.moveTo(p6);
}

void moverMotor(int motor, float grados) {
  posicionActual[motor - 1] = grados;

  long pasos = gradosAPasos(grados);

  switch (motor) {
  case 1:
    m1.moveTo(pasos);
    break;
  case 2:
    m2.moveTo(pasos);
    break;
  case 3:
    m3.moveTo(pasos);
    break;
  case 4:
    m4.moveTo(pasos);
    break;
  case 5:
    m5.moveTo(pasos);
    break;
  case 6:
    m6.moveTo(pasos);
    break;
  }
}

void procesarMensaje(String msg) {

  Serial.println("Mensaje recibido:");
  Serial.println(msg);

  if (msg.startsWith("M")) {
    int motor = msg.substring(1, 2).toInt();
    float valor = msg.substring(3).toFloat();

    moverMotor(motor, valor);
  }

  if (msg.startsWith("P")) {
    msg.remove(0, 2);

    float valores[6];

    for (int i = 0; i < 6; i++) {
      int index = msg.indexOf(',');

      if (index != -1) {
        valores[i] = msg.substring(0, index).toFloat();
        msg = msg.substring(index + 1);
      } else {
        valores[i] = msg.toFloat();
      }
    }

    moverPose(valores[0], valores[1], valores[2], valores[3], valores[4],
              valores[5]);
  }
}

void callback(char *topic, byte *payload, unsigned int length) {

  String mensaje;

  for (int i = 0; i < length; i++)
    mensaje += (char)payload[i];

  if (String(topic) == topic_electroiman) {

    if (mensaje == "1") {
      digitalWrite(ELECTROIMAN, HIGH);
      Serial.println("Electroiman ENCENDIDO");
    }

    if (mensaje == "0") {
      digitalWrite(ELECTROIMAN, LOW);
      Serial.println("Electroiman APAGADO");
    }

    return;
  }

  procesarMensaje(mensaje);
}

void setup_wifi() {
  delay(10);

  Serial.println("Conectando WiFi");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
}

void reconnect() {
  while (!client.connected()) {
    Serial.println("Conectando MQTT...");

    if (client.connect("ESP32_ROBOT")) {
      Serial.println("MQTT conectado");

      client.subscribe(topic_sub);
      client.subscribe(topic_electroiman);

      client.publish(topic_pub, "ESP32 conectado");
    } else {
      delay(2000);
    }
  }
}

void setup() {

  Serial.begin(115200);

  setup_wifi();

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  pinMode(ELECTROIMAN, OUTPUT);
  m1.setMaxSpeed(2000);
  m2.setMaxSpeed(2000);
  m3.setMaxSpeed(2000);
  m4.setMaxSpeed(2000);
  m5.setMaxSpeed(2000);
  m6.setMaxSpeed(2000);

  m1.setAcceleration(800);
  m2.setAcceleration(800);
  m3.setAcceleration(800);
  m4.setAcceleration(800);
  m5.setAcceleration(800);
  m6.setAcceleration(800);
}

void loop() {

  if (!client.connected())
    reconnect();

  client.loop();
  m1.run();
  m2.run();
  m3.run();
  m4.run();
  m5.run();
  m6.run();
}
