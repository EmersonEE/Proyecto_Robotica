#ifndef ROBOT_CONTROLLER_H
#define ROBOT_CONTROLLER_H

#include "data.h"
#include <AccelStepper.h>

class RobotController {
private:
  AccelStepper *motors[6];
  float currentAngles[6];
  bool isHomed;
  unsigned long movementStartTime;

  // Conversión grados -> pasos con inversión
  long gradosAPasos(float grados, int motorIdx);

  // Validar que un ángulo esté dentro de límites seguros
  bool validarAngulo(int motorIdx, float grados);

public:
  RobotController();

  // Inicialización
  void init();
  void calibrate(); // Homing / posición inicial

  // Movimiento
  bool moveToAngle(int motor, float grados); // motor: 1-6
  bool moveToPose(float angles[6]);
  void emergencyStop();

  // Actualización (llamar en loop)
  void update();
  bool isMoving();
  bool isHomingComplete() const { return isHomed; }

  // Getters
  float getCurrentAngle(int motor) const { return currentAngles[motor - 1]; }
  const float *getAllAngles() const { return currentAngles; }
};

#endif // ROBOT_CONTROLLER_H
