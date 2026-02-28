import tkinter as tk
import os
from tkinter import filedialog
from tkinter import messagebox
import json
import serial
import time

carpeta = "trayectorias"

if not os.path.exists(carpeta):
    os.makedirs(carpeta)
try:
    ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
    time.sleep(2)
except:
    ser = None
    print("⚠️ ESP32 no conectado")


def guardar_posicion():
    m1 = slider1.get()
    m2 = slider2.get()
    m3 = slider3.get()
    m4 = slider4.get()
    m5 = slider5.get()
    m6 = slider6.get()

    pose = [[m1, m2, m3, m4, m5, m6]]
    archivos = os.listdir(carpeta)
    numero = len(archivos)

    nombre = f"{carpeta}/pose_{numero}.json"

    with open(nombre, "w") as f:
        json.dump(pose, f)

    label_estado.config(text=f"Pose guardada: pose_{numero}.json")


def seleccionar_archivo():
    global posiciones

    archivo = filedialog.askopenfilename(
        initialdir=carpeta,
        title="Seleccionar pose",
        filetypes=(("JSON files", "*.json"),),
    )

    if archivo:
        with open(archivo, "r") as f:
            posiciones = json.load(f)

        label_estado.config(text=f"Cargado: {os.path.basename(archivo)}")


def enviar_posiciones():
    if ser is None:
        messagebox.showerror("Error", "ESP32 no conectado")
        return

    if len(posiciones) == 0:
        messagebox.showwarning("Vacío", "No hay pose cargada")
        return

    pose = posiciones[0]

    comando = f"P:{pose[0]},{pose[1]},{pose[2]},{pose[3]},{pose[4]},{pose[5]}\n"
    print(comando.strip())
    ser.write(comando.encode())

    label_estado.config(text="Pose enviada al ESP32")


def limpiar():
    global posiciones
    posiciones = []

    slider1.set(0)
    slider2.set(0)
    slider3.set(0)
    slider4.set(0)
    slider5.set(0)
    slider6.set(0)

    if ser:
        for i in range(1, 7):
            comando = f"M{i}:0\n"
            ser.write(comando.encode())

    label_estado.config(text="Memoria y sliders reseteados")


def enviar_tiempo_real(motor, valor):
    if ser is None:
        return

    comando = f"M{motor}:{valor}\n"
    print(comando.strip())

    ser.write(comando.encode())


ventana = tk.Tk()
ventana.title("Control Brazo Robótico")
ventana.geometry("400x450")

tk.Label(text="Motor 1").pack()
slider1 = tk.Scale(
    ventana,
    from_=-180,
    to=180,
    length=400,
    orient=tk.HORIZONTAL,
    command=lambda v: enviar_tiempo_real(1, v),
)
slider1.set(0)
slider1.pack()

tk.Label(text="Motor 2").pack()
slider2 = tk.Scale(
    ventana,
    from_=-180,
    to=180,
    length=400,
    orient=tk.HORIZONTAL,
    command=lambda v: enviar_tiempo_real(2, v),
)
slider2.set(0)
slider2.pack()

tk.Label(text="Motor 3").pack()
slider3 = tk.Scale(
    ventana,
    from_=-180,
    to=180,
    length=400,
    orient=tk.HORIZONTAL,
    command=lambda v: enviar_tiempo_real(3, v),
)
slider3.set(0)
slider3.pack()


tk.Label(text="Motor 4").pack()
slider4 = tk.Scale(
    ventana,
    from_=-180,
    to=180,
    length=400,
    orient=tk.HORIZONTAL,
    command=lambda v: enviar_tiempo_real(4, v),
)
slider4.set(0)
slider4.pack()


tk.Label(text="Motor 5").pack()
slider5 = tk.Scale(
    ventana,
    from_=-180,
    to=180,
    length=400,
    orient=tk.HORIZONTAL,
    command=lambda v: enviar_tiempo_real(5, v),
)
slider5.set(0)
slider5.pack()


tk.Label(text="Motor 6").pack()
slider6 = tk.Scale(
    ventana,
    from_=-180,
    to=180,
    length=400,
    orient=tk.HORIZONTAL,
    command=lambda v: enviar_tiempo_real(6, v),
)
slider6.set(0)
slider6.pack()

tk.Button(
    ventana, text="Guardar Posición", command=guardar_posicion, bg="green", fg="white"
).pack(pady=5)

tk.Button(
    ventana, text="Enviar al ESP32", command=enviar_posiciones, bg="blue", fg="white"
).pack(pady=5)

tk.Button(ventana, text="Limpiar Memoria", command=limpiar).pack(pady=5)
tk.Button(ventana, text="Seleccionar Trayectoria", command=seleccionar_archivo).pack(
    pady=5
)
label_estado = tk.Label(text="Listo", fg="red")
label_estado.pack(pady=10)

ventana.mainloop()
