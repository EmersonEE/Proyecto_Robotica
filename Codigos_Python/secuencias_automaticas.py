import json
import os
from os.path import join
from pathlib import Path
import time
import glob
import paho.mqtt.client as mqtt

broker = "192.168.1.136"
port = 1883
celdas_ocupadas = []
color_objeto = []
topic_ws1228 = "/ws2812"
topic_pub = "/suscribirse"
topic_sub = "/saludo"
topic_electro = "/electroiman"
topic_ws1228 = "/ws2812"
client = mqtt.Client()
home = [0, 135, 0, 190, 155, 0]
a = ""
archivos = glob.glob("*.json")
secuencia_final = []
casillas_color = None


def on_connect(client, userdata, flags, rc):
    print("")
    client.subscribe(topic_ws1228)


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print("ESP32:", payload)


client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(broker, port, 60)
    client.loop_start()
    mqtt_ok = True
except:
    mqtt_ok = False
    print("⚠️ No se pudo conectar a MQTT")


def enviar_mqtt_color(color):
    if not mqtt_ok:
        return
    info = client.publish(topic_ws1228, color, qos=1)  # QoS 1 asegura la entrega
    info.wait_for_publish()  # Esto obliga al código a esperar a que el broker confirme


BASE_PATH = Path("/home/emerson/Documentos/Proyecto_Robotica/Codigos_Python")
RUTA_POSICIONES = BASE_PATH / "posiciones_solas"
RUTA_SECUENCIAS = BASE_PATH / "secuencias_automaticas"
RUTA_CASILLAS_COLOR = BASE_PATH / "casillas_color"
BASE_PATH.mkdir(parents=True, exist_ok=True)
RUTA_POSICIONES.mkdir(parents=True, exist_ok=True)
RUTA_SECUENCIAS.mkdir(parents=True, exist_ok=True)
RUTA_CASILLAS_COLOR.mkdir(parents=True, exist_ok=True)
for nombre_archivo in os.listdir(RUTA_CASILLAS_COLOR):
    casillas_color = RUTA_CASILLAS_COLOR / nombre_archivo


def cargar_posiciones(ruta_directorio):
    posiciones = {}
    if not ruta_directorio.exists():
        print(f"Error: La ruta {ruta_directorio} no existe")
        return posiciones

    for archivo_path in ruta_directorio.glob("*.json"):
        try:
            with open(archivo_path, encoding="utf-8") as f:
                posiciones[archivo_path.stem] = json.load(f)[0]
        except (json.JSONDecodeError, IndexError):
            print(f"Error al leer: {archivo_path.name}")

    return posiciones


nuevo_dicc = cargar_posiciones(RUTA_POSICIONES)
archivo_home = nuevo_dicc.get("home")

with open(f"{casillas_color}", "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

lista_de_datos = []
for objetos in datos["objetos"]:
    celdas_ocupadas.append(objetos["celda"])
    color_objeto.append(objetos["color"].lower())


def enviar_mqtt(mensaje):
    if not mqtt_ok:
        print("MQTT no conectado")
        return

    print("TX:", mensaje)
    client.publish(topic_pub, mensaje)


def enviar_pose(pose):
    comando = f"P:{pose[0]},{pose[1]},{pose[2]},{pose[3]},{pose[4]},{pose[5]}"
    enviar_mqtt(comando)


print(f"Diccionario cargado con {len(nuevo_dicc)} posiciones.")

for i, (pos, color) in enumerate(zip(celdas_ocupadas, color_objeto)):
    str_pos = str(pos)
    if str_pos in nuevo_dicc and color in nuevo_dicc:
        patron_fijo = [
            archivo_home,
            nuevo_dicc[str_pos],
            archivo_home,
            nuevo_dicc[color],
            archivo_home,
        ]

        nombre_archivo = f"{i}_secuencia.json"
        ruta_guardado = RUTA_SECUENCIAS / nombre_archivo

        with open(ruta_guardado, "w", encoding="utf-8") as archivo:
            json.dump(patron_fijo, archivo, indent=4)
        print(f"Guardado: {nombre_archivo}")
    else:
        print(
            f"Error: No se encontró la posición '{str_pos}' o el color '{color}' en los archivos."
        )
ultima_pose_enviada = None
ultimo_color_enviado = None  # Variable para rastrear el cambio de color

mapa_colores = {"rojo": "1", "azul": "2", "amarillo": "3"}

for nombre_archivo in sorted(os.listdir(RUTA_SECUENCIAS)):
    ruta_completa = RUTA_SECUENCIAS / nombre_archivo

    try:
        indice = int(nombre_archivo.split("_")[0])
        color_actual = color_objeto[indice]
        codigo_mqtt = mapa_colores.get(color_actual, "0")
    except (ValueError, IndexError):
        continue

    with open(ruta_completa, "r", encoding="utf-8") as f:
        datos = json.load(f)
        print(f"\n--- Procesando: {nombre_archivo} (Color: {color_actual}) ---")

        for pose in datos:
            if pose != ultima_pose_enviada:
                if codigo_mqtt != ultimo_color_enviado:
                    print(
                        f">>> Cambiando LED a: {color_actual} (Código: {codigo_mqtt})"
                    )
                    enviar_mqtt_color(codigo_mqtt)
                    ultimo_color_enviado = codigo_mqtt

                enviar_pose(pose)
                print(f"Enviando Pose: {pose}")

                time.sleep(1.5)
                ultima_pose_enviada = pose
            else:
                print("Home repetido")
