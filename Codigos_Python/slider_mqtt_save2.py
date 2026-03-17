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
electroiman_encendido = False
client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    print("MQTT conectado")
    client.subscribe(topic_sub)
    client.subscribe(topic_electro)


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

    delay = float(entry_delay.get())

    movimiento = 0

    for pose in trayectoria:
        enviar_pose(pose)

        #   if not es_home(pose):
        #       movimiento += 1

        #       if movimiento == 1:
        #           activar_electroiman(1)
        #           print("Electroiman ON")

        #       elif movimiento == 2:
        #           activar_electroiman(0)
        #           print("Electroiman OFF")

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


def ajustar_slider(motor_num, delta):
    slider = sliders[motor_num - 1]
    valor_actual = slider.get()
    nuevo_valor = valor_actual + delta

    if nuevo_valor < -360:
        nuevo_valor = -360
    elif nuevo_valor > 360:
        nuevo_valor = 360

    slider.set(nuevo_valor)

    enviar_mqtt(f"M{motor_num}:{nuevo_valor}")


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

frame_delay = tk.Frame(ventana)
frame_delay.pack(pady=10)

tk.Label(frame_delay, text="Delay entre poses (s)").grid(row=0, column=0)

entry_delay = tk.Entry(frame_delay)
entry_delay.insert(0, "4")
entry_delay.grid(row=0, column=1)

ventana.mainloop()
