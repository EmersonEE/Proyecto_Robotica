#include <Arduino.h>

void setup() {
  Serial.begin(9600); // Inicia serial a 9600 baudios
}

void loop() {
  if (Serial.available() > 0) {                  // ¿Hay datos disponibles?
    String datos = Serial.readStringUntil('\n'); // Lee hasta el salto de línea
    // Aquí puedes hacer algo con los datos, ej: encender un LED
    Serial.print("Recibido: ");
    Serial.println(datos);
  }
}
