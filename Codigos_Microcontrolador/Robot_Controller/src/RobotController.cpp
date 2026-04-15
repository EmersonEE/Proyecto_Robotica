#include "RobotController.h"
#include <esp_task_wdt.h>

// ==================== CONSTRUCTOR ====================
RobotController::RobotController() : isHomed(false), movementStartTime(0) {
  // Inicializar punteros a nullptr
  for (int i = 0; i < 6; i++) {
    motors[i] = nullptr;
    currentAngles[i] = 0;
  }
}

// ==================== INICIALIZACIÓN ====================
void RobotController::init() {
  DEBUG_PRINTLN("🔧 Inicializando RobotController...");

  // Crear instancias de AccelStepper
  motors[0] = new AccelStepper(AccelStepper::DRIVER, STEP_M1, DIR_M1);
  motors[1] = new AccelStepper(AccelStepper::DRIVER, STEP_M2, DIR_M2);
  motors[2] = new AccelStepper(AccelStepper::DRIVER, STEP_M3, DIR_M3);
  motors[3] = new AccelStepper(AccelStepper::DRIVER, STEP_M4, DIR_M4);
  motors[4] = new AccelStepper(AccelStepper::DRIVER, STEP_M5, DIR_M5);
  motors[5] = new AccelStepper(AccelStepper::DRIVER, STEP_M6, DIR_M6);

  // Configurar cada motor
  for (int i = 0; i < 6; i++) {
    // Calcular pasos por grado
    stepsPerDegree[i] = stepsPerRev[i] / 360.0;

    // Configurar velocidad y aceleración PERSONALIZADAS
    motors[i]->setMaxSpeed(maxSpeed[i]);
    motors[i]->setAcceleration(acceleration[i]);
    motors[i]->setMinPulseWidth(minPulseWidth[i]);

    // Resetear posición
    motors[i]->setCurrentPosition(0);
    currentAngles[i] = 0;

    DEBUG_PRINTF("✅ Motor %d: %d pasos/rev, %.1f°/s máx, %.0f pasos/s²\n",
                 i + 1, stepsPerRev[i], maxSpeed[i] / stepsPerDegree[i],
                 acceleration[i]);
  }

  DEBUG_PRINTLN("✅ RobotController inicializado");
}

// ==================== CONVERSIONES Y VALIDACIONES ====================
long RobotController::gradosAPasos(float grados, int motorIdx) {
  long pasos = lround(grados * stepsPerDegree[motorIdx]);
  return motorInvertido[motorIdx] ? -pasos : pasos;
}

bool RobotController::validarAngulo(int motorIdx, float grados) {
  return grados >= motorMinAngle[motorIdx] && grados <= motorMaxAngle[motorIdx];
}

// ==================== CALIBRACIÓN / HOMING ====================
void RobotController::calibrate() {
  DEBUG_PRINTLN("🔄 Iniciando calibración (homing)...");

  // Mover todos los motores a posición cero de forma segura
  const float homePose[6] = {0,   90, 0,
                             200, 90, 0}; // ✅ AJUSTAR A TU POSE "HOME"

  if (!moveToPose(const_cast<float *>(homePose))) {
    DEBUG_PRINTLN("❌ Error en calibración");
    return;
  }

  // Esperar con timeout que terminen los movimientos
  movementStartTime = millis();
  while (isMoving()) {
    update();
    if (millis() - movementStartTime > MOVEMENT_TIMEOUT_MS) {
      DEBUG_PRINTLN("⚠️ Timeout en calibración");
      emergencyStop();
      return;
    }
    yield();              // Permitir tareas de fondo del ESP32
    esp_task_wdt_reset(); // Reset watchdog
  }

  // Establecer posición actual como cero
  for (int i = 0; i < 6; i++) {
    motors[i]->setCurrentPosition(0);
    currentAngles[i] = 0;
  }

  isHomed = true;
  DEBUG_PRINTLN("✅ Calibración completada");
}

// ==================== MOVIMIENTO INDIVIDUAL ====================
bool RobotController::moveToAngle(int motor, float grados) {
  if (motor < 1 || motor > 6) {
    DEBUG_PRINTF("❌ Motor inválido: %d\n", motor);
    return false;
  }

  int idx = motor - 1;

  if (!validarAngulo(idx, grados)) {
    DEBUG_PRINTF(
        "❌ Ángulo %.1f° fuera de límites para motor %d [%.1f°, %.1f°]\n",
        grados, motor, motorMinAngle[idx], motorMaxAngle[idx]);
    return false;
  }

  long pasos = gradosAPasos(grados, idx);
  motors[idx]->moveTo(pasos);
  currentAngles[idx] = grados;

  DEBUG_PRINTF("🎯 Motor %d -> %.1f° (%ld pasos)\n", motor, grados, pasos);
  return true;
}

// ==================== MOVIMIENTO DE POSE COMPLETA ====================
bool RobotController::moveToPose(float angles[6]) {
  // Validar todos los ángulos primero (fail-fast)
  for (int i = 0; i < 6; i++) {
    if (!validarAngulo(i, angles[i])) {
      DEBUG_PRINTF("❌ Pose rechazada: ángulo %.1f° inválido para motor %d\n",
                   angles[i], i + 1);
      return false;
    }
  }

  // Aplicar movimientos
  for (int i = 0; i < 6; i++) {
    long pasos = gradosAPasos(angles[i], i);
    motors[i]->moveTo(pasos);
    currentAngles[i] = angles[i];
  }

  movementStartTime = millis();
  movimientoActivo = true;

  DEBUG_PRINTLN("🚀 Pose enviada a motores");
  return true;
}

// ==================== PARADA DE EMERGENCIA ====================
void RobotController::emergencyStop() {
  DEBUG_PRINTLN("🛑 PARADA DE EMERGENCIA");
  for (int i = 0; i < 6; i++) {
    motors[i]->stop();
    motors[i]
        ->disableOutputs(); // Liberar motores para evitar sobrecalentamiento
  }
  movimientoActivo = false;
}

// ==================== ACTUALIZACIÓN EN LOOP ====================
void RobotController::update() {
  for (int i = 0; i < 6; i++) {
    if (motors[i]->distanceToGo() != 0) {
      motors[i]->run();
    }
  }
}

bool RobotController::isMoving() {
  for (int i = 0; i < 6; i++) {
    if (motors[i]->distanceToGo() != 0) {
      return true;
    }
  }
  return false;
}
