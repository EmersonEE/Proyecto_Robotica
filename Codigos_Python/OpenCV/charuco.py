import cv2

# Configuración del tablero
ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
SQUARES_VERT = 7
SQUARES_HORIZ = 5
SQUARE_LENGTH = 0.04  # Metros (ajusta según tu impresión)
MARKER_LENGTH = 0.02  # Metros

board = cv2.aruco.CharucoBoard(
    (SQUARES_HORIZ, SQUARES_VERT), SQUARE_LENGTH, MARKER_LENGTH, ARUCO_DICT
)

# Generar imagen para imprimir
board_img = board.generateImage((2000, 2800))  # Resolución alta para impresión
cv2.imwrite("charuco_board.png", board_img)
print("Tablero guardado como charuco_board.png")
