import cv2
import imutils

# Videostreaming o video de entrada
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Lectura inicial de la imagen a incrustar en el video
image = cv2.imread('camo.jpeg', cv2.IMREAD_UNCHANGED)

# Detector de rostros
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Variable para rastrear el estado de cambio de imagen
change_image = False

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = imutils.resize(frame, width=640)

    # Detección de los rostros presentes en el fotograma
    faces = faceClassif.detectMultiScale(frame, 1.3, 5)

    for (x, y, w, h) in faces:
        # Redimensionar la imagen de entrada de acuerdo al ancho del
        # rostro detectado
        resized_image = imutils.resize(image, width=w)
        filas_image = resized_image.shape[0]
        col_image = w

        # Determinar una porción del alto de la imagen de entrada 
        # redimensionada
        porcion_alto = filas_image // 4

        dif = 0

        # Si existe suficiente espacio sobre el rostro detectado
        # para insertar la imagen de entrada redimensionada,
        # se visualizará dicha imagen
        if y + porcion_alto - filas_image >= 0:
            # Tomamos la sección de frame donde se va a ubicar
            # la imagen a mostrar
            n_frame = frame[y + porcion_alto - filas_image : y + porcion_alto,
                           x : x + col_image]
        else:
            # Determinamos la sección de la imagen que excede al video
            dif = abs(y + porcion_alto - filas_image)
            # Tomamos la sección de frame donde se va a ubicar
            # la imagen a mostrar
            n_frame = frame[0 : y + porcion_alto,
                           x : x + col_image]

        # Determinamos la máscara que posee la imagen de entrada
        # redimensionada y también la invertimos
        mask = resized_image[:, :, 3 if resized_image.shape[2] == 4 else 0]
        mask_inv = cv2.bitwise_not(mask)

        # Creamos una imagen con fondo negro y el gorro/tiara/2021
        # Luego creamos una imagen donde en el fondo esté frame
        # y en negro la imagen a mostrar
        bg_black = cv2.bitwise_and(resized_image, resized_image, mask=mask)
        bg_black = bg_black[dif:, :, 0:3]
        bg_frame = cv2.bitwise_and(n_frame, n_frame, mask=mask_inv[dif:, :])

        # Sumamos las dos imágenes obtenidas
        result = cv2.add(bg_black, bg_frame)
        if y + porcion_alto - filas_image >= 0:
            frame[y + porcion_alto - filas_image : y + porcion_alto, x : x + col_image] = result
        else:
            frame[0 : y + porcion_alto, x : x + col_image] = result

    cv2.imshow('frame', frame)

    k = cv2.waitKey(1) & 0xFF

    # Cambiar de imagen si se presiona la tecla "C"
    if k == ord('c') or k == ord('C'):
        image = cv2.imread('manu.png', cv2.IMREAD_UNCHANGED)
        change_image = True

    if k == ord('v') or k == ord('C'):
        image = cv2.imread('3d.png', cv2.IMREAD_UNCHANGED)
        change_image = True



    # Salir del bucle si se presiona la tecla "Esc"
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
