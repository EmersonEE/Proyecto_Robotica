import os
import json

ruta_a_listar = (
    "/home/emerson/Documentos/Proyecto_Robotica/Codigos_Python/posiciones_solas"
)
ruta_secuencias_automaticas = (
    "/home/emerson/Documentos/Proyecto_Robotica/Codigos_Python/secuencias_automaticas"
)
nombres = []
valores = []
nuevo_dicc = {}
ruta_home = os.path.join(ruta_a_listar, "home.json")
with open(ruta_home, encoding="utf-8") as home:
    archivo_home = json.load(home)[0]
print(archivo_home)
if os.path.exists(ruta_a_listar):
    for a in os.listdir(ruta_a_listar):
        ruta_archivo = os.path.join(ruta_a_listar, a)

        nombre_archivo = a.replace(".json", "")
        nombres.append(nombre_archivo)

        with open(ruta_archivo, encoding="utf-8") as archivos:
            contenido = json.load(archivos)[0]
            valores.append(contenido)

else:
    print(f"La ruta {ruta_a_listar} no existe")

for i in range(len(nombres)):
    nuevo_dicc[nombres[i]] = valores[i]

print(nuevo_dicc)
print(type(nuevo_dicc["1"]))
print(nuevo_dicc["1"])

a = input("Infrese un numero: ")
b = input("infrese otro numero: ")

patron_fijo = [
    archivo_home,
    nuevo_dicc[a],
    archivo_home,
    nuevo_dicc[b],
    archivo_home,
]
ruta_guardado = os.path.join(ruta_secuencias_automaticas, "secuencia.json")

with open(ruta_guardado, "w", encoding="utf-8") as archivo:
    json.dump(patron_fijo, archivo)

print("Archivo guardado correctamente")
print(patron_fijo)
print(type(patron_fijo))
json_string = json.dumps(patron_fijo)
print(json_string)

