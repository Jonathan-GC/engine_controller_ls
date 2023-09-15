
import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

# Inicializar el modelo de seguimiento de la cara
face_mesh = mp_face_mesh.FaceMesh()

# Abre el archivo de video o utiliza la cámara en vivo (0 para la cámara predeterminada)
cap = cv2.VideoCapture('sources/video3.mp4')  # Reemplaza 'video.mp4' con el nombre de tu video

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convierte la imagen a escala de grises (MediaPipe espera una imagen en escala de grises)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Realiza el seguimiento de la cara en la imagen
    results = face_mesh.process(gray)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Aquí puedes acceder a los puntos clave de la cara y calcular los valores de blendShapes
            # Por ejemplo, puedes calcular la diferencia entre las posiciones de los puntos clave
            # antes y después de un movimiento facial para determinar el valor de un blendShape específico.
            
            # Por ejemplo, si deseas acceder a los puntos clave de la boca:
            mouth_landmarks = face_landmarks.landmark[48:68]

            # Realiza cálculos para blendShapes aquí

    # Dibuja los puntos clave en la imagen
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for landmark in face_landmarks.landmark:
                x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

    # Muestra la imagen en una ventana
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
