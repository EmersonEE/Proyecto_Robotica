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


lista_str_posicion = []
lista_posicion = [1, 5, 9, 12, 18, 10]
for i in range(len(lista_posicion)):
    lista_str_posicion.append(str(lista_posicion[i]))

print("Lista a Strings")
print(lista_str_posicion)
lista_color = ["rojo", "amarillo", "azul", "azul", "amarillo", "rojo"]
lista_enviar = []
print(nuevo_dicc[lista_str_posicion[2]])
for a in range(len(lista_posicion)):
    lista_enviar = [lista_posicion[a], lista_color[a]]
    print(lista_enviar)

for i in range(len(lista_str_posicion)):
    patron_fijo = [
        archivo_home,
        nuevo_dicc[lista_str_posicion[i]],
        archivo_home,
        nuevo_dicc[lista_color[i]],
        archivo_home,
    ]
    ruta_guardado = os.path.join(ruta_secuencias_automaticas, f"{i}_secuencia.json")

    with open(ruta_guardado, "w", encoding="utf-8") as archivo:
        json.dump(patron_fijo, archivo)

    print("Archivo guardado correctamente")
    json_string = json.dumps(patron_fijo)
    print(json_string)
