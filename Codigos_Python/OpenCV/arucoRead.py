import cv2

# Abrir cámara

# cap = cv2.VideoCapture(1)

# url = "http://192.168.1.191:4747/video/mjpegfeed?1080x720"
# cap = cv2.VideoCapture(10, cv2.CAP_V4L2)
cap = cv2.VideoCapture(10)
# Diccionario

diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# Detector
parametros = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(diccionario, parametros)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    corners, ids, rejected = detector.detectMarkers(frame)

    if ids is not None:
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        for i in range(len(ids)):
            print("Detectado ID:", ids[i][0])

    cv2.imshow("Aruco Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
