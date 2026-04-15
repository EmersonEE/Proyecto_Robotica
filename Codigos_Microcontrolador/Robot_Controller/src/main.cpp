// ==================== INCLUDES ====================
#include "RobotController.h"
#include "data.h"
#include <Arduino.h>
#include <PubSubClient.h>
#include <WiFi.h>
#include <esp_task_wdt.h>

WiFiClient espClient;
PubSubClient client(espClient);
RobotController robot;

void callback(char *topic, byte *payload, unsigned int length)
{
  // Construir mensaje eficientemente
  String mensaje;
  mensaje.reserve(length + 1);
  for (unsigned int i = 0; i < length; i++)
  {
    mensaje += (char)payload[i];
  }

  DEBUG_PRINTF("📩 MQTT [%s]: %s\n", topic, mensaje.c_str());

  if (String(topic) == topic_electroiman)
  {
    if (mensaje == "1")
    {
      digitalWrite(ELECTROIMAN, HIGH);
      DEBUG_PRINTLN("🧲 Electroimán: ON");
    }
    else if (mensaje == "0")
    {
      digitalWrite(ELECTROIMAN, LOW);
      DEBUG_PRINTLN("🧲 Electroimán: OFF");
    }
    return;
  }

  // Comandos de movimiento
  if (mensaje.startsWith("M"))
  {
    // Formato: M1,90.5 -> Motor 1 a 90.5°
    int motor = mensaje.substring(1, 2).toInt();
    float valor = mensaje.substring(3).toFloat();

    if (!robot.moveToAngle(motor, valor))
    {
      client.publish(topic_estado, "ERROR: Comando inválido");
    }
    return;
  }

  if (mensaje.startsWith("P"))
  {
    // Formato: P0,90,0,180,90,0 -> Pose completa
    String datos = mensaje.substring(2); // Remover "P"
    float valores[6] = {0};

    for (int i = 0; i < 6; i++)
    {
      int commaIndex = datos.indexOf(',');
      if (commaIndex != -1)
      {
        valores[i] = datos.substring(0, commaIndex).toFloat();
        datos = datos.substring(commaIndex + 1);
      }
      else
      {
        valores[i] = datos.toFloat(); // Último valor
      }
    }

    if (!robot.moveToPose(valores))
    {
      client.publish(topic_estado, "ERROR: Pose inválida");
    }
    return;
  }

  // Comando de emergencia
  if (mensaje == "STOP" || mensaje == "EMERGENCY")
  {
    robot.emergencyStop();
    client.publish(topic_estado, "EMERGENCY_STOP");
    return;
  }
}

void reconnectMQTT()
{
  uint8_t intentos = 0;
  uint32_t delayActual = MQTT_RECONNECT_DELAY_BASE;

  while (!client.connected() && intentos < MQTT_MAX_RECONNECT_ATTEMPTS)
  {
    intentos++;
    DEBUG_PRINTF("🔄 Conectando MQTT (intento %d/%d)...\n", intentos,
                 MQTT_MAX_RECONNECT_ATTEMPTS);

    if (client.connect("ESP32_ROBOT"))
    {
      DEBUG_PRINTLN("✅ MQTT conectado");
      client.subscribe(topic_sub);
      client.subscribe(topic_electroiman);
      client.publish(topic_pub, "ESP32 conectado y listo");
      return;
    }

    DEBUG_PRINTF("❌ Falló. Reintentando en %dms...\n", delayActual);
    delay(delayActual);
    delayActual = (delayActual * 2 < MQTT_MAX_RECONNECT_DELAY) ? (delayActual * 2) : MQTT_MAX_RECONNECT_DELAY;
    esp_task_wdt_reset();
  }

  DEBUG_PRINTLN(
      "💥 ERROR: No se pudo conectar a MQTT después de múltiples intentos");
}

void setupWiFi()
{
  DEBUG_PRINT("📡 Conectando a WiFi");
  WiFi.begin(ssid, password);

  uint32_t inicio = millis();
  while (WiFi.status() != WL_CONNECTED)
  {
    if (millis() - inicio > WIFI_TIMEOUT_MS)
    {
      DEBUG_PRINTLN("\n❌ Timeout WiFi");
      return;
    }
    delay(500);
    DEBUG_PRINT(".");
  }

  DEBUG_PRINTF("\n✅ WiFi conectado | IP: %s\n",
               WiFi.localIP().toString().c_str());
}

// ==================== SETUP ====================
void setup()
{
  // Inicializar Serial y Watchdog
  Serial.begin(SERIAL_BAUD);
  esp_task_wdt_init(10, true); // 10 segundos timeout
  esp_task_wdt_add(NULL);

  DEBUG_PRINTLN("\n🤖 ESP32 Robot Arm - Iniciando...");

  // Configurar pines
  pinMode(ELECTROIMAN, OUTPUT);
  pinMode(ROBOT_LISTO, INPUT_PULLUP);
  digitalWrite(ELECTROIMAN, LOW);

  // Inicializar WiFi y MQTT
  setupWiFi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);

  // Inicializar controlador de robot
  robot.init();

  // Calibrar (homing) con timeout
  DEBUG_PRINTLN("⏳ Esperando señal de inicio...");
  unsigned long setupStart = millis();

  while (!digitalRead(ROBOT_LISTO))
  {
    if (millis() - setupStart > 60000)
    { // 1 minuto timeout
      DEBUG_PRINTLN("⚠️ Timeout esperando señal de inicio, continuando...");
      break;
    }
    delay(100);
    esp_task_wdt_reset();
  }

  // Ejecutar calibración
  robot.calibrate();
  robotListo = true;

  DEBUG_PRINTLN("🎉 Sistema listo para operar");
  client.publish(topic_pub, "Robot inicializado");
}

// ==================== LOOP PRINCIPAL ====================
void loop()
{
  // Reset watchdog en cada iteración
  esp_task_wdt_reset();

  // Mantener conexión MQTT
  if (!client.connected())
  {
    reconnectMQTT();
  }
  client.loop();

  // Solo operar si el robot está habilitado
  if (digitalRead(ROBOT_LISTO) && robotListo)
  {

    // Actualizar movimiento de motores
    robot.update();

    // Detectar fin de movimiento
    if (movimientoActivo && !robot.isMoving())
    {
      movimientoActivo = false;
      DEBUG_PRINTLN("✨ Movimiento completado");
      client.publish(topic_estado, "DONE");
    }
  }
  else
  {
    // Si no está listo, asegurar que los motores estén detenidos
    if (robot.isMoving())
    {
      robot.emergencyStop();
    }
  }

  // Pequeño delay para estabilidad
  delay(2);
}
