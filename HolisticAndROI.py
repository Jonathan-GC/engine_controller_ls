import cv2
import mediapipe as mp
import numpy as np
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks.python import vision

dibujo = mp.solutions.drawing_utils
estilos_dibujo = mp.solutions.drawing_styles
map_holistico = mp.solutions.holistic

#-------------------------------------------
#        Hiper Parametros de script         |
#-------------------------------------------

# Var de captura
captura = None


# Si MedioCaptura:1 => captura con video
# Si MedioCaptura:0 => captura con camara
MedioCaptura = 1 

if MedioCaptura:
    captura = cv2.VideoCapture('sources/video6.mp4')
else:
    captura = cv2.VideoCapture(0)


#Lectura de imagen incicial para crear un espacio negro del tamaño de la captura
_, img = captura.read()
display_seleccion = np.zeros(img.shape, np.uint8)

#Roi Definido por dos puntos
p1, p2 = None, None
estado = 0



#-------------------------------------------
#                 Funciones                |
#-------------------------------------------

def seleccionar_area(event, x, y, flags, param):
    global estado, p1, p2

    # Imprimimos la información sobre los eventos que se estén realizando
    

    # Ejemplos de acciones con algunos eventos del mouse
    if event == cv2.EVENT_LBUTTONDBLCLK:
        
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


with map_holistico.Holistic( min_detection_confidence = 0.6, min_tracking_confidence=0.6, refine_face_landmarks = True) as modelo_holistico:
   
    #introducir los callBack del mouse
    cv2.namedWindow('Imagen')
    cv2.setMouseCallback("Imagen", seleccionar_area)
    imagen_area_interes = None
   
   
   
   
    while (captura.isOpened()):
        _, imagen = captura.read()

        #Rompa el lazo en caso de no recibir señal
        if not _:
            break

        else:
            # si el roi esta seleccionado dibujelo
            if estado  > 1:
                cv2.rectangle(imagen, p1, p2, (255, 0, 0), 10)

            
            #Escalado de la imagen
            if p1 != None and p2 !=None:  
                imagen_area_interes = imagen[int(p1[1]) : int(p2[1]), int(p1[0]) : int(p2[0])]
                imagen_area_interes = cv2.resize(imagen_area_interes, (0, 0), fx=3, fy=3)
            else:
                imagen_area_interes = np.zeros(imagen.shape, np.uint8) 


            #Colocar la imagen en negro
            display_fondo_oscuro = np.zeros(imagen_area_interes.shape, np.uint8) 


            #Para mejorar el rendimiento, opcionalmente marque la imagen como no grabable para pasarla como referencia.
            imagen_area_interes.flags.writeable = False


            #convertir  la imagen  BGR a RGB
            imagen_area_interes = cv2.cvtColor(imagen_area_interes, cv2.COLOR_BGR2RGB)

            #resultado de cuerpo
            resultado_holistico = modelo_holistico.process(imagen_area_interes)

            # Dibujar anotaciones en la imagen
            imagen_area_interes.flags.writeable = True
            imagen_area_interes = cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)


            dibujo.draw_landmarks(
                display_fondo_oscuro,
                resultado_holistico.face_landmarks,
                map_holistico.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=estilos_dibujo
                .get_default_face_mesh_contours_style())
            dibujo.draw_landmarks(
                display_fondo_oscuro,
                resultado_holistico.pose_landmarks,
                map_holistico.POSE_CONNECTIONS,
                landmark_drawing_spec=estilos_dibujo
                .get_default_pose_landmarks_style())
            dibujo.draw_landmarks(
                display_fondo_oscuro,
                resultado_holistico.left_hand_landmarks,
                map_holistico.HAND_CONNECTIONS,
                landmark_drawing_spec=estilos_dibujo
                .get_default_pose_landmarks_style())
            
            dibujo.draw_landmarks(
                display_fondo_oscuro,
                resultado_holistico.right_hand_landmarks,
                map_holistico.HAND_CONNECTIONS,
                landmark_drawing_spec=estilos_dibujo
                .get_default_pose_landmarks_style())
            

            cv2.imshow("Imagen", imagen+display_seleccion)
            cv2.imshow("imagen1", imagen_area_interes)
            cv2.imshow("Gestualizacion", display_fondo_oscuro)



            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

captura.release()
cv2.destroyAllWindows()

#print(resultado_holistico.pose_landmarks.landmark[0])
#print(resultado_holistico.pose_landmarks.landmark[0].x)

for puntoCuerpo in map_holistico.PoseLandmark:
    print(f" Extremidad {puntoCuerpo.name}\n{resultado_holistico.pose_landmarks.landmark[puntoCuerpo]}")

for i, puntoRostro in enumerate(map_holistico.FACEMESH_CONTOURS):
    print(i, puntoRostro)


import matplotlib.pyplot as plt

def plot_face_blendshapes_bar_graph(face_blendshapes):
  # Extract the face blendshapes category names and scores.
  face_blendshapes_names = [face_blendshapes_category.category_name for face_blendshapes_category in face_blendshapes]
  face_blendshapes_scores = [face_blendshapes_category.score for face_blendshapes_category in face_blendshapes]
  # The blendshapes are ordered in decreasing score value.
  face_blendshapes_ranks = range(len(face_blendshapes_names))

  fig, ax = plt.subplots(figsize=(12, 12))
  bar = ax.barh(face_blendshapes_ranks, face_blendshapes_scores, label=[str(x) for x in face_blendshapes_ranks])
  ax.set_yticks(face_blendshapes_ranks, face_blendshapes_names)
  ax.invert_yaxis()

  # Label each bar with values
  for score, patch in zip(face_blendshapes_scores, bar.patches):
    plt.text(patch.get_x() + patch.get_width(), patch.get_y(), f"{score:.4f}", va="top")

  ax.set_xlabel('Score')
  ax.set_title("Face Blendshapes")
  plt.tight_layout()
  plt.show()

  
plot_face_blendshapes_bar_graph(resultado_holistico.face_blendshapes[0])