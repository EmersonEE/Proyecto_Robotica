#include <AccelStepper.h>
#include <Arduino.h>
#define STEP_PIN 3
#define DIR_PIN 4

long pasosActuales = 0;
float pasosPorGrado = 200.0 / 360.0;
const float pasoRevolucion = 200.0;
AccelStepper motor(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);
// void moverMotor(long pasos) {
//
//   if (pasos > 0)
//     digitalWrite(DIR_PIN, HIGH);
//   else
//     digitalWrite(DIR_PIN, LOW);
//
//   pasos = abs(pasos);
//
//   for (long i = 0; i < pasos; i++) {
//     digitalWrite(STEP_PIN, HIGH);
//     delayMicroseconds(800);
//     digitalWrite(STEP_PIN, LOW);
//     delayMicroseconds(800);
//   }
// }
void setup() {
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  Serial.begin(115200);
  motor.setMaxSpeed(1000);
  motor.setAcceleration(500);
}

void loop() {
  if (Serial.available()) {

    float angulo = Serial.parseFloat();
    // long pasosObjetivo = angulo * pasosPorGrado;
    long pasosM = (angulo * pasoRevolucion) / 360.0;
    motor.move(pasosM);
    // moverMotor(pasosObjetivo - pasosActuales);
    // pasosActuales = pasosObjetivo;
  }
}
