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
topic_electro = "/electroiman"
topic_ws1228 = "/ws2812"
electroiman_encendido = False
client = mqtt.Client()
robot_listo = False
home = [0, 135, 0, 190, 155, 0]


def on_connect(client, userdata, flags, rc):
    print("")
    client.subscribe(topic_sub)
    client.subscribe(topic_electro)
    client.subscribe("/estado")
    client.subscribe(topic_ws1228)


def on_message(client, userdata, msg):
    global robot_listo

    payload = msg.payload.decode()
    print("ESP32:", payload)

    if msg.topic == "/estado" and payload == "DONE":
        robot_listo = True


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


def esperar_robot():
    global robot_listo
    robot_listo = False

    while not robot_listo:
        time.sleep(0.01)


def enviar_mqtt(mensaje):
    if not mqtt_ok:
        print("MQTT no conectado")
        return

    print("TX:", mensaje)
    client.publish(topic_pub, mensaje)


def activar_electroiman(valor):
    if not mqtt_ok:
        print("MQTT no conectado")
        return

    client.publish(topic_electro, valor)


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


def electroiman_fun():
    global electroiman_encendido

    if not electroiman_encendido:
        activar_electroiman(1)
        electroiman_encendido = True
    else:
        activar_electroiman(0)
        electroiman_encendido = False


def eliminar_pose():
    seleccion = lista.curselection()

    if not seleccion:
        return

    index = seleccion[0]

    lista.delete(index)
    trayectoria.pop(index)


def es_home(pose):
    # return pose == [0, 0, 0, 0, 0, 0]
    return


def ejecutar_trayectoria():
    if len(trayectoria) == 0:
        messagebox.showwarning("Vacio", "No hay poses para enviar")
        return

    for i, pose in enumerate(trayectoria):
        enviar_pose(pose)
        esperar_robot()  # 🔥 sincronización real

        if i == 1:  # PICK
            activar_electroiman(1)
            print("Electroiman ON")

        elif i == 3:  # PLACE
            activar_electroiman(0)
            print("Electroiman OFF")


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
        limpiar_trayectoria()


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

    # --- NUEVA LÓGICA DE SINCRONIZACIÓN ---
    if len(trayectoria) > 0:
        primera_pose = trayectoria[0]
        actualizar_interfaz_y_robot(primera_pose)
        print(f"Sliders sincronizados con la primera pose: {primera_pose}")


def actualizar_interfaz_y_robot(pose):
    for i in range(6):
        sliders[i].set(pose[i])
    enviar_pose(pose)


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
botones_mas = []
botones_menos = []
grados_boton = 3

for i in range(6):
    frame_motor = tk.Frame(ventana)
    frame_motor.pack(pady=4, padx=10, fill="x")

    tk.Label(frame_motor, text=f"Motor {i + 1}", width=10, anchor="w").pack(
        side=tk.LEFT
    )

    btn_menos = tk.Button(
        frame_motor, text="-5", width=4, command=lambda m=i + 1: ajustar_slider(m, -5)
    )
    btn_menos.pack(side=tk.LEFT, padx=(0, 4))

    s = tk.Scale(
        frame_motor,
        from_=-360,
        to=360,
        resolution=5,
        orient=tk.HORIZONTAL,
        length=340,
        showvalue=True,
    )
    s.set(0)
    s.pack(side=tk.LEFT, fill="x", expand=True)

    btn_mas = tk.Button(
        frame_motor, text="+5", width=4, command=lambda m=i + 1: ajustar_slider(m, +5)
    )
    btn_mas.pack(side=tk.LEFT, padx=(4, 0))

    s.bind("<ButtonRelease-1>", lambda e, mot=i + 1: slider_release(e, mot))

    sliders.append(s)
    botones_menos.append(btn_menos)
    botones_mas.append(btn_mas)

slider1, slider2, slider3, slider4, slider5, slider6 = sliders


def actualizar_y_enviar(motor_num, nuevo_valor):
    nuevo_valor = max(-360, min(360, nuevo_valor))

    sliders[motor_num - 1].set(nuevo_valor)

    enviar_mqtt(f"M{motor_num}:{nuevo_valor}")


def ajustar_slider(motor_num, delta):
    valor_actual = sliders[motor_num - 1].get()
    actualizar_y_enviar(motor_num, valor_actual + delta)


def slider_release(event, motor_num):
    valor = event.widget.get()
    actualizar_y_enviar(motor_num, valor)


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

tk.Button(frame_archivo, text="Electroiman", command=electroiman_fun).grid(
    row=0, column=3
)

lista = tk.Listbox(ventana, width=60)
lista.pack()


def al_seleccionar_lista(event):
    seleccion = lista.curselection()
    if not seleccion:
        return

    index = seleccion[0]
    pose_seleccionada = trayectoria[index]

    actualizar_interfaz_y_robot(pose_seleccionada)


lista.bind("<<ListboxSelect>>", al_seleccionar_lista)

frame_delay = tk.Frame(ventana)
frame_delay.pack(pady=10)

tk.Label(frame_delay, text="Delay entre poses (s)").grid(row=0, column=0)

entry_delay = tk.Entry(frame_delay)
entry_delay.insert(0, "4")
entry_delay.grid(row=0, column=1)
for s in sliders:
    s.set(0)
trayectoria = []
ventana.mainloop()
