import cv2
import numpy as np
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2

dibujo_mp = mp.solutions.drawing_utils
cuerpos_mp = mp.solutions.pose
manos_mp = mp.solutions.hands
rostro_mp = mp.solutions.face_mesh

captura = cv2.VideoCapture(0)
#captura = cv2.VideoCapture('sources/video6.mp4')


resultados = {"manos": None, "cuerpo": None, "rostro": None}



with cuerpos_mp.Pose(model_complexity=1, min_tracking_confidence=0.5 ) as cuerpo, \
manos_mp.Hands(
        max_num_hands=2,
        min_detection_confidence=0.5) as hands, \
rostro_mp.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.5) as face_mesh:

    while(captura.isOpened()):

        _, imagen = captura.read()


        if _  == 0:
            break
        
        else:
            

            #Escalado
            half = cv2.resize(imagen, (0, 0), fx=0.8, fy=0.8)

            #Colocar la imagen en negro
            ju = np.zeros(half.shape, np.uint8) 
           
            #convertir  la imagen  BGR a RGB
            imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

            #resultado de cuerpo
            cuerpoResult = cuerpo.process(imagen)

            #resultado de manos
            manosResult = hands.process(imagen)

            #resultado de rostro
            rostroResult = face_mesh.process(imagen)

            #half = cv2.cvtColor(half, cv2.COLOR_GRAY2BGR)

            if cuerpoResult.pose_landmarks:
                dibujo_mp.draw_landmarks(
                    ju, cuerpoResult.pose_landmarks, cuerpos_mp.POSE_CONNECTIONS,
                    dibujo_mp.DrawingSpec(color=(245, 117, 66), thickness = 1, circle_radius=1),
                    dibujo_mp.DrawingSpec(color=(245, 66, 230), thickness = 1, circle_radius=1),
                )

            if manosResult.multi_hand_landmarks:
                
                for resultadoMano in manosResult.multi_hand_landmarks:
                    #print(resultadoMano)
                    dibujo_mp.draw_landmarks(
                        ju, resultadoMano, manos_mp.HAND_CONNECTIONS,
                        dibujo_mp.DrawingSpec(color=(245, 117, 66), thickness = 1, circle_radius=1),
                        dibujo_mp.DrawingSpec(color=(245, 66, 230), thickness = 1, circle_radius=1),
                    )

            if rostroResult.multi_face_landmarks:
                for rostro in rostroResult.multi_face_landmarks:
                    dibujo_mp.draw_landmarks(
                        ju, rostro, rostro_mp.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None
                        #connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
                        #dibujo_mp.DrawingSpec(color=(245, 117, 66), thickness = 1, circle_radius=1),
                        #dibujo_mp.DrawingSpec(color=(245, 66, 230), thickness = 1, circle_radius=1),

                    )



            cv2.imshow("imagen", imagen)
            cv2.imshow("imagen1", half)
            cv2.imshow("imagen2", ju)


            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

captura.release()
cv2.destroyAllWindows()


