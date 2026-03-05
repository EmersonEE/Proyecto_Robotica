import paho.mqtt.client as mqtt
import time

# Configuración MQTT
broker = "192.168.1.136"  # IP del broker (Ej: Mosquitto, Raspberry Pi)
port = 1883
topic_sub = "/saludo"  # Topic para recibir mensajes
topic_pub = "/suscribirse"  # Topic para enviar mensajes


# Callback al conectarse al broker
def on_connect(client, userdata, flags, rc):
    print(f"Conectado al broker. Código: {rc}")
    client.subscribe(topic_sub)  # Suscripción automática


# Callback al recibir un mensaje
def on_message(client, userdata, msg):
    print(f"\n[MENSAJE RECIBIDO] Topic: {msg.topic} -> Payload: {msg.payload.decode()}")


# Configuración del cliente
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Conexión
client.connect(broker, port, 60)
client.loop_start()  # Inicia el loop en segundo plano (no bloqueante)

# Menú interactivo
try:
    while True:
        print("\n--- Menú MQTT ---")
        print("1. Enviar mensaje")
        print("2. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            mensaje = input("Escribe el mensaje a enviar: ")
            client.publish(topic_pub, mensaje)
            print(f"[MENSAJE ENVIADO] Topic: {topic_pub} -> Payload: {mensaje}")
        elif opcion == "2":
            break
        else:
            print("Opción no válida.")

except KeyboardInterrupt:
    print("\nDesconectando...")
finally:
    client.loop_stop()
