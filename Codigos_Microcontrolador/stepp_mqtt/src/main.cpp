#include "esp32-hal-gpio.h"
#include "esp32-hal.h"
#include <AccelStepper.h>
#include <Arduino.h>
#include <PubSubClient.h>
#include <WiFi.h>
#include <data.h>
WiFiClient espClient;
PubSubClient client(espClient);
AccelStepper m1(1, STEP_M1, DIR_M1);
AccelStepper m2(1, STEP_M2, DIR_M2);
AccelStepper m3(1, STEP_M3, DIR_M3);
AccelStepper m4(1, STEP_M4, DIR_M4);
AccelStepper m5(1, STEP_M5, DIR_M5);
AccelStepper m6(1, STEP_M6, DIR_M6);

AccelStepper *motors[6] = {&m1, &m2, &m3, &m4, &m5, &m6};

long gradosAPasos(float grados, int motor) {
  return lround(grados * stepsPerDegree[motor]);
}

void moverPose(float g1, float g2, float g3, float g4, float g5, float g6) {
  float g[6] = {g1, g2, g3, g4, g5, g6};

  for (int i = 0; i < 6; i++) {
    long pasos = gradosAPasos(g[i], i);

    if (i == 4 || i == 3)
      pasos = -pasos;

    motors[i]->moveTo(pasos);
  }

  movimientoActivo = true;
}
void moverMotor(int motor, float grados) {
  int idx = motor - 1;

  posicionActual[idx] = grados;

  long pasos = gradosAPasos(grados, idx);

  if (idx == 4)
    pasos = -pasos;
  if (idx == 3)
    pasos = -pasos;

  motors[idx]->moveTo(pasos);
}

void procesarMensaje(String msg) {
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
      Serial.println("Electroiman ON");
    }

    if (mensaje == "0") {
      digitalWrite(ELECTROIMAN, LOW);
      Serial.println("Electroiman OFF");
    }

    return;
  }
  procesarMensaje(mensaje);
}

void setup_wifi() {
  Serial.println("Conectando WiFi");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("WiFi conectado");
}

void reconnect() {
  while (!client.connected()) {
    Serial.println("Conectando MQTT");

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

  for (int i = 0; i < 6; i++) {
    stepsPerDegree[i] = stepsPerRev[i] / 360.0;
  }

  for (int i = 0; i < 6; i++) {
    motors[i]->setMaxSpeed(2000);
    motors[i]->setAcceleration(800);
  }

  m4.setMinPulseWidth(5);
  m5.setMinPulseWidth(5);
  m6.setMinPulseWidth(5);

  moverPose(0, 135, 0, 190, 155, 0);
  bool moviendo = true;
  while (moviendo) {
    moviendo = false;
    for (int i = 0; i < 6; i++) {
      if (motors[i]->distanceToGo() != 0) {
        motors[i]->run();
        moviendo = true;
      }
    }
  }
  for (int i = 0; i < 6; i++) {
    motors[i]->setCurrentPosition(0);
  }
}

void loop() {
  if (!client.connected())
    reconnect();

  client.loop();

  bool alguienMoviendose = false;

  for (int i = 0; i < 6; i++) {
    if (motors[i]->distanceToGo() != 0) {
      motors[i]->run();
      alguienMoviendose = true;
    }
  }

  if (movimientoActivo && !alguienMoviendose) {
    movimientoActivo = false;

    Serial.println("MOVIMIENTO TERMINADO");
    client.publish("/estado", "DONE");
  }
}
