import cv2

# /dev/video10 → índice 10
cap = cv2.VideoCapture(10, cv2.CAP_V4L2)

if not cap.isOpened():
    print("Error: no se pudo abrir la cámara")
    exit()

# Opcional: forzar resolución
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Frame perdido")
        continue

    # Ejemplo: dibujar texto
    cv2.putText(
        frame, "Android Camera", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
    )

    cv2.imshow("Camara Celular", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
