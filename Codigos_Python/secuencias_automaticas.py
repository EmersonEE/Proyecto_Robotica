import json
from pathlib import Path

# Configuracion de rutas usando Pathlib
BASE_PATH = Path("/home/emerson/Documentos/Proyecto_Robotica/Codigos_Python")
RUTA_POSICIONES = BASE_PATH / "posiciones_solas"
RUTA_SECUENCIAS = BASE_PATH / "secuencias_automaticas"

# Asegurar que la ruta de salida existe
RUTA_SECUENCIAS.mkdir(parents=True, exist_ok=True)


def cargar_posiciones(ruta_directorio):
    posiciones = {}
    if not ruta_directorio.exists():
        print(f"Error: La ruta {ruta_directorio} no existe")
        return posiciones

    for archivo_path in ruta_directorio.glob("*.json"):
        try:
            with open(archivo_path, encoding="utf-8") as f:
                # Cargamos el primer elemento directamente
                posiciones[archivo_path.stem] = json.load(f)[0]
        except (json.JSONDecodeError, IndexError):
            print(f"Error al leer: {archivo_path.name}")

    return posiciones


# 1. Cargar datos base
nuevo_dicc = cargar_posiciones(RUTA_POSICIONES)
archivo_home = nuevo_dicc.get("home")  # Extrae 'home' del diccionario si existe

# 2. Datos de prueba (Simulando lo que vendrá del dispositivo)
lista_posicion = [18, 19, 20, 12, 5, 24]
lista_color = ["rojo", "amarillo", "azul", "azul", "amarillo", "rojo"]

print(f"Diccionario cargado con {len(nuevo_dicc)} posiciones.")

# 3. Generación de secuencias
# Usamos zip() para iterar sobre ambas listas al mismo tiempo
for i, (pos, color) in enumerate(zip(lista_posicion, lista_color)):
    str_pos = str(pos)

    # Verificamos que las llaves existan para evitar errores en tiempo de ejecución
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
            json.dump(patron_fijo, archivo, indent=4)  # indent=4 para que sea legible

        print(f"Guardado: {nombre_archivo}")
    else:
        print(
            f"Error: No se encontró la posición '{str_pos}' o el color '{color}' en los archivos."
        )
