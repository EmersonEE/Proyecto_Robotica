import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import time
import paho.mqtt.client as mqtt

broker = "192.168.1.136"
port = 1883
topic_pub = "/suscribirse"
topic_sub = "/saludo"

client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    print("MQTT conectado")
    client.subscribe(topic_sub)


def on_message(client, userdata, msg):
    print("ESP32:", msg.payload.decode())


client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(broker, port, 60)
    client.loop_start()
    mqtt_ok = True
except:
    mqtt_ok = False
    print("⚠️ No se pudo conectar a MQTT")


carpeta = "trayectorias"
trayectoria = []

if not os.path.exists(carpeta):
    os.makedirs(carpeta)


def enviar_mqtt(mensaje):
    if not mqtt_ok:
        print("MQTT no conectado")
        return

    print("TX:", mensaje)
    client.publish(topic_pub, mensaje)


def leer_sliders():
    return [
        slider1.get(),
        slider2.get(),
        slider3.get(),
        slider4.get(),
        slider5.get(),
        slider6.get(),
    ]


def enviar_pose(pose):
    comando = f"P:{pose[0]},{pose[1]},{pose[2]},{pose[3]},{pose[4]},{pose[5]}"
    enviar_mqtt(comando)


def home_robot():
    for s in sliders:
        s.set(0)

    for i in range(1, 7):
        enviar_mqtt(f"M{i}:0")

    print("Robot enviado a HOME")


def guardar_pose():
    pose = leer_sliders()
    trayectoria.append(pose)

    lista.insert(tk.END, pose)


def eliminar_pose():
    seleccion = lista.curselection()

    if not seleccion:
        return

    index = seleccion[0]

    lista.delete(index)
    trayectoria.pop(index)


def ejecutar_trayectoria():
    if len(trayectoria) == 0:
        messagebox.showwarning("Vacío", "No hay poses")
        return

    delay = float(entry_delay.get())

    for pose in trayectoria:
        enviar_pose(pose)

        ventana.update()
        time.sleep(delay)


def limpiar():
    global trayectoria

    trayectoria = []
    lista.delete(0, tk.END)

    for s in sliders:
        s.set(0)

    for i in range(1, 7):
        enviar_mqtt(f"M{i}:0")


def guardar_archivo():
    if len(trayectoria) == 0:
        return

    archivo = filedialog.asksaveasfilename(
        initialdir=carpeta,
        defaultextension=".json",
        filetypes=[("JSON", "*.json")],
    )

    if archivo:
        with open(archivo, "w") as f:
            json.dump(trayectoria, f)

        print("Trayectoria guardada")


def cargar_archivo():
    global trayectoria

    archivo = filedialog.askopenfilename(
        initialdir=carpeta,
        filetypes=[("JSON", "*.json")],
    )

    if not archivo:
        return

    with open(archivo) as f:
        trayectoria = json.load(f)

    lista.delete(0, tk.END)

    for pose in trayectoria:
        lista.insert(tk.END, pose)


def slider_release(event, motor):
    valor = event.widget.get()

    enviar_mqtt(f"M{motor}:{valor}")


def limpiar_trayectoria():
    global trayectoria

    if len(trayectoria) == 0:
        return

    confirmar = messagebox.askyesno("Confirmar", "¿Borrar toda la trayectoria?")

    if confirmar:
        trayectoria = []

        lista.delete(0, tk.END)

        print("Trayectoria borrada")


ventana = tk.Tk()
ventana.title("Control Brazo Robótico Profesional")
ventana.geometry("600x600")

sliders = []

for i in range(6):
    tk.Label(ventana, text=f"Motor {i + 1}").pack()

    s = tk.Scale(
        ventana,
        from_=-180,
        to=180,
        resolution=5,
        orient=tk.HORIZONTAL,
        length=400,
    )

    s.set(0)
    s.pack()

    s.bind("<ButtonRelease-1>", lambda e, m=i + 1: slider_release(e, m))

    sliders.append(s)

slider1, slider2, slider3, slider4, slider5, slider6 = sliders

frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Guardar Pose", command=guardar_pose).grid(
    row=0, column=0
)

tk.Button(frame_botones, text="Eliminar Pose", command=eliminar_pose).grid(
    row=0, column=1
)

tk.Button(
    frame_botones, text="Ejecutar Trayectoria", command=ejecutar_trayectoria
).grid(row=0, column=2)

frame_archivo = tk.Frame(ventana)
frame_archivo.pack()

tk.Button(frame_archivo, text="Guardar Archivo", command=guardar_archivo).grid(
    row=0, column=0
)

tk.Button(frame_archivo, text="Cargar Archivo", command=cargar_archivo).grid(
    row=0, column=1
)
tk.Button(frame_botones, text="HOME (0,0,0)", command=home_robot).grid(row=0, column=3)

tk.Button(frame_botones, text="Limpiar Trayectoria", command=limpiar_trayectoria).grid(
    row=0, column=4
)
tk.Label(text="Trayectoria").pack()

lista = tk.Listbox(ventana, width=60)
lista.pack()

frame_delay = tk.Frame(ventana)
frame_delay.pack(pady=10)

tk.Label(frame_delay, text="Delay entre poses (s)").grid(row=0, column=0)

entry_delay = tk.Entry(frame_delay)
entry_delay.insert(0, "1")
entry_delay.grid(row=0, column=1)

ventana.mainloop()
