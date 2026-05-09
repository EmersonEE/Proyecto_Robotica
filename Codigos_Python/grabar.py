import cv2


def grabar_video():
    # Iniciar la captura de video (el 0 indica la cámara web predeterminada)
    cap = cv2.VideoCapture(1)

    # Verificar si la cámara se abrió correctamente
    if not cap.isOpened():
        print("Error: No se pudo acceder a la cámara.")
        return

    # Forzar la resolución a 720p (1280x720) para cumplir con el requisito de la SAT
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Definir el codec y crear el objeto VideoWriter para guardar el archivo
    # Usamos 'mp4v' para generar un archivo .mp4 estándar
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    # Configuramos el archivo de salida a 20 FPS (cuadros por segundo)
    # 20 FPS es fluido pero ayuda a que el archivo pese menos de 10MB
    out = cv2.VideoWriter("video_sat.mp4", fourcc, 20.0, (1280, 720))

    print("\n--- GRABANDO ---")
    print("Por favor, mira a la ventana del video.")
    print(
        "Presiona la tecla 'q' dentro de la ventana de video para detener y guardar.\n"
    )

    while cap.isOpened():
        # Leer frame por frame
        ret, frame = cap.read()

        if ret == True:
            # Escribir el frame en nuestro archivo de video
            out.write(frame)

            # Mostrar lo que la cámara está viendo en una ventana emergente
            cv2.imshow('Grabando para la SAT - Presiona "q" para detener', frame)

            # Esperar a que el usuario presione la tecla 'q' para salir
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            print("Error al leer el frame de la cámara.")
            break

    # Liberar los recursos de la cámara y cerrar ventanas al terminar
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print("¡Listo! Tu video ha sido guardado exitosamente como 'video_sat.mp4'")


# Ejecutar la función
if __name__ == "__main__":
    grabar_video()
