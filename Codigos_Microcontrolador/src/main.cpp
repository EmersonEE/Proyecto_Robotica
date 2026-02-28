#include "HardwareSerial.h"
#include <AccelStepper.h>

// ============================
// CONFIG MOTORES
// ============================

// DRIVER = STEP + DIR
AccelStepper m1(AccelStepper::DRIVER, 2, 4);
AccelStepper m2(AccelStepper::DRIVER, 16, 17);
AccelStepper m3(AccelStepper::DRIVER, 5, 18);
AccelStepper m4(AccelStepper::DRIVER, 19, 21);
AccelStepper m5(AccelStepper::DRIVER, 22, 23);
AccelStepper m6(AccelStepper::DRIVER, 25, 26);

AccelStepper *motores[6] = {&m1, &m2, &m3, &m4, &m5, &m6};

// ============================
// CONFIG PASOS POR GRADO
// ============================

float pasosPorGrado = 10.0; // AJUSTAR según mecánica

// ============================

String input = "";

// ============================
// ============================
// LECTURA SERIAL
// ============================

void moverIndividual(String cmd) {

  int motor = cmd.substring(1, 2).toInt();
  int valor = cmd.substring(3).toInt();

  float pasos = valor * pasosPorGrado;

  motores[motor - 1]->moveTo(pasos);
}

void moverPose(String cmd) {

  cmd.remove(0, 2); // quitar "P:"

  int valores[6];
  int index = 0;

  while (cmd.length() > 0) {
    int coma = cmd.indexOf(',');

    if (coma == -1) {
      valores[index++] = cmd.toInt();
      break;
    }

    valores[index++] = cmd.substring(0, coma).toInt();
    cmd = cmd.substring(coma + 1);
  }

  for (int i = 0; i < 6; i++) {
    float pasos = valores[i] * pasosPorGrado;
    motores[i]->moveTo(pasos);
  }
}

void procesar(String cmd) {

  cmd.trim();

  if (cmd.startsWith("M")) {
    moverIndividual(cmd);
  }

  if (cmd.startsWith("P")) {
    moverPose(cmd);
  }
}
void leerSerial() {

  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\n') {
      procesar(input);
      input = "";
      Serial.print(c);
    } else {
      input += c;

      Serial.print(c);
    }
  }
}

// ============================
// PROCESAR COMANDOS
// ============================

// ============================
// MODO JOG
// ============================
// ============================
// MODO POSE
// ============================
void setup() {
  Serial.begin(115200);

  for (int i = 0; i < 6; i++) {
    motores[i]->setMaxSpeed(2000);
    motores[i]->setAcceleration(800);
  }
}

// ============================

void loop() {

  leerSerial();

  for (int i = 0; i < 6; i++) {
    motores[i]->run();
  }
}
