import cv2
import numpy as np
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2

dibujo_mp = mp.solutions.drawing_utils
cuerpos_mp = mp.solutions.pose
manos_mp = mp.solutions.hands
rostro_mp = mp.solutions.face_mesh


#captura = cv2.VideoCapture(0)
captura = cv2.VideoCapture('sources/video5.mp4')


resultados = {"manos": None, "cuerpo": None, "rostro": None}



_, frame = captura.read()
imagen2 = np.zeros(frame.shape, np.uint8)

#Roi Definido por dos puntos
p1, p2 = None, None
estado = 0

#Llamada a eventos del mouse
def seleccionar_area(event, x, y, flags, param):
    global estado, p1, p2

    # Imprimimos la información sobre los eventos que se estén realizando
    

    # Ejemplos de acciones con algunos eventos del mouse
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.putText(imagen2, "Seleccionar", (0, 0), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, cv2.LINE_AA)
        #Seleccionar primer punto
        if estado == 0:
            p1 = (x, y)
            estado += 1
        #selecionar segundo punto
        elif estado == 1:
            p2 = (x, y)
            estado += 1

    if event == cv2.EVENT_RBUTTONUP:
        
        p1, p2 = None, None
        estado = 0
        




with cuerpos_mp.Pose(model_complexity=1, min_tracking_confidence=0.7 ) as cuerpo, \
manos_mp.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7) as hands, \
rostro_mp.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.7) as face_mesh:


    #introducir los callBack del mouse
    cv2.namedWindow('Imagen')
    cv2.setMouseCallback("Imagen", seleccionar_area)
    imagen_area_interes = None
    while(captura.isOpened()):

        _, imagen = captura.read()


        if _  == 0:
            break
        
        else:
            
            # si el roi esta seleccionado dibujelo
            if estado  > 1:
                cv2.rectangle(imagen, p1, p2, (255, 0, 0), 10)


            #Escalado

            
            #half = cv2.resize(imagen, (0, 0), fx=0.8, fy=0.8)
            if p1 != None and p2 !=None:  
                imagen_area_interes = imagen[int(p1[1]) : int(p2[1]), int(p1[0]) : int(p2[0])]
                imagen_area_interes = cv2.resize(imagen_area_interes, (0, 0), fx=3, fy=3)
            else:
                imagen_area_interes = np.zeros(imagen.shape, np.uint8) 
            #Colocar la imagen en negro
            ju = np.zeros(imagen_area_interes.shape, np.uint8) 

           
            #convertir  la imagen  BGR a RGB
            imagen_area_interes = cv2.cvtColor(imagen_area_interes, cv2.COLOR_BGR2RGB)

            #resultado de cuerpo
            cuerpoResult = cuerpo.process(imagen_area_interes)

            #resultado de manos
            manosResult = hands.process(imagen_area_interes)

            #resultado de rostro
            rostroResult = face_mesh.process(imagen_area_interes)

            #half = cv2.cvtColor(half, cv2.COLOR_GRAY2BGR)

            if cuerpoResult.pose_landmarks:
                dibujo_mp.draw_landmarks(
                    ju, cuerpoResult.pose_landmarks, cuerpos_mp.POSE_CONNECTIONS,
                    dibujo_mp.DrawingSpec(color=(245, 117, 66), thickness = 1, circle_radius=0),
                    dibujo_mp.DrawingSpec(color=(0, 0, 255), thickness = 1, circle_radius=0),
                )

            if manosResult.multi_hand_landmarks:
                
                for resultadoMano in manosResult.multi_hand_landmarks:
                    #print(resultadoMano)
                    dibujo_mp.draw_landmarks(
                        ju, resultadoMano, manos_mp.HAND_CONNECTIONS,
                        dibujo_mp.DrawingSpec(color=(245, 117, 66), thickness = 1, circle_radius=0),
                        dibujo_mp.DrawingSpec(color=(0, 0, 255), thickness = 1, circle_radius=0),
                    )

            if rostroResult.multi_face_landmarks:
                for rostro in rostroResult.multi_face_landmarks:
                    dibujo_mp.draw_landmarks(
                        ju, rostro, rostro_mp.FACEMESH_TESSELATION,
                        dibujo_mp.DrawingSpec(color=(245, 117, 66), thickness = 1, circle_radius=0),
                        dibujo_mp.DrawingSpec(color=(0, 0, 255), thickness = 1, circle_radius=0),

                    )

            

            cv2.imshow("Imagen", imagen+imagen2)
            cv2.imshow("imagen1", imagen_area_interes)
            cv2.imshow("Gestualizacion", ju)



            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

captura.release()
cv2.destroyAllWindows()

