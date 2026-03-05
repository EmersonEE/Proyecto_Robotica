import paho.mqtt.client as mqtt
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


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


def enviar_tiempo_real(motor, v):
    comando = f"M{motor}: valor{v}"
    valor_enviar = v
    print(comando.strip())
    client.publish(topic_sub, valor_enviar)


# Configuración del cliente
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(broker, port, 60)
    client.loop_start()
except Exception as e:
    print(f"No se puedo conectar al broker : {e}")

ventana = tk.Tk()
ventana.title("Slider ESP32 MQTT")
ventana.geometry("500x600")
# Conexión

# Menú interactivo
tk.Label(text="Motor Prueba").pack()
slider1 = tk.Scale(
    ventana,
    from_=180,
    to=180,
    length=400,
    resolution=5,
    orient=tk.HORIZONTAL,
    command=lambda v: enviar_tiempo_real(1, v),
)
slider1.set(0)
slider1.pack()


def on_closing():
    client.loop_stop()
    client.disconnect()
    ventana.destroy()


ventana.protocol("WM_DELETE_WINDOW", on_closing)
ventana.mainloop()
