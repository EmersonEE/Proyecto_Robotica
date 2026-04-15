import cv2

# 1. Diccionario
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# 2. Definición del Tablero (Medidas Reales)
# Para que quepa en el área segura de una hoja carta:
# 7 columnas de 25mm = 175mm (Cabe bien en los 215mm de ancho)
# 9 filas de 25mm = 225mm (Cabe bien en los 279mm de alto)
square_size = 0.025  # 25mm por cuadro (más fácil de medir con regla)
marker_size = 0.019  # 19mm para el marcador ArUco
board = cv2.aruco.CharucoBoard((7, 9), square_size, marker_size, aruco_dict)

# 3. Resolución para Impresión (300 DPI)
# Hoja Carta completa en píxeles
width_px = int(8.5 * 300)  # 2550 px
height_px = int(11 * 300)  # 3300 px

# 4. Cálculo del margen en píxeles
# Queremos un margen generoso de 20mm (0.78 pulgadas) por lado
# para evitar CUALQUIER recorte de impresora.
margin_px = int(0.78 * 300)  # aprox 234 píxeles

# 5. Generar la imagen centrada
# 'marginSize' en OpenCV define cuántos PÍXELES de borde blanco dejar
img = board.generateImage((width_px, height_px), marginSize=margin_px)

cv2.imwrite("charuco_final.png", img)
print(f"Tablero generado. Cada cuadro debe medir {square_size * 1000}mm")
