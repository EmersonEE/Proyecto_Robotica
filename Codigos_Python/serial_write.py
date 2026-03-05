import serial
import time

# Configura el puerto según tu PC (ejemplo: 'COM3' en Windows o '/dev/ttyUSB0' en Linux)
arduino_port = "/dev/ttyUSB0"
baud_rate = 9600

try:
    # Establecer conexión
    arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
    time.sleep(2)  # Esperar a que Arduino se reinicie al conectar
    print(f"Conectado a {arduino_port}")

    while True:
        # Pedir ángulo al usuario
        angulo = input("Introduce el ángulo a mover (o 'salir'): ")

        if angulo.lower() == "salir":
            break

        # Enviar el dato con un salto de línea \n
        # Es vital usar .encode() para convertir el texto a bytes
        arduino.write(f"{angulo}\n".encode())

        # Opcional: leer respuesta de Arduino
        time.sleep(0.1)
        while arduino.in_waiting > 0:
            respuesta = arduino.readline().decode("utf-8").strip()
            print(f"Arduino dice: {respuesta}")

except Exception as e:
    print(f"Error: {e}")

finally:
    if "arduino" in locals():
        arduino.close()
        print("Conexión cerrada.")
