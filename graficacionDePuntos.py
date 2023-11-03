import pandas as pd
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import plotly.express as px

import time as t


dibujo_mp = mp.solutions.drawing_utils
cuerpos_mp = mp.solutions.pose
manos_mp = mp.solutions.hands
rostro_mp = mp.solutions.face_mesh


# ****************************************************
#                   Variables de Data
# ****************************************************

puntos = None
puntos_df = pd.DataFrame(columns= ["X", "Y", "Z", "Puntos", "fotograma"])
parte_Cuerpo = [
    "NOSE"	,
"LEFT_EYE_INNER"	,
 "LEFT_EYE"	,
 "LEFT_EYE_OUTER"	,
 "RIGHT_EYE_INNER"	,
 "RIGHT_EYE"	,
  "RIGHT_EYE_OUTER"	,
 "LEFT_EAR"	,
  "RIGHT_EAR"	,
  "MOUTH_LEFT"	,
  "MOUTH_RIGHT"	,
  "LEFT_SHOULDER"	,
  "RIGHT_SHOULDER"	,
  "LEFT_ELBOW"	,
  "RIGHT_ELBOW"	,
  "LEFT_WRIST"	,
  "RIGHT_WRIST"	,
  "LEFT_PINKY" 	,
  "RIGHT_PINKY"	,
  "LEFT_INDEX"	,
  "RIGHT_INDEX"	,
  "LEFT_THUMB"	,
  "RIGHT_THUMB"	,
  "LEFT_HIP"	,
  "RIGHT_HIP"	,
  "LEFT_KNEE"	,
  "RIGHT_KNEE"	,
  "LEFT_ANKLE" 	,
  "RIGHT_ANKLE"	,
  "LEFT_HEEL"	,
  "RIGHT_HEEL"	,
  "LEFT_FOOT_INDEX"	,
  "RIGHT_FOOT_INDEX"
]


#*********************************************************


#captura = cv2.VideoCapture(0)

#captura = cv2.VideoCapture('sources/emocionesVideo1.mp4')

#captura = cv2.VideoCapture('sources/feliz-2.mp4')
captura = cv2.VideoCapture('sources/feliz_3.mp4')

#captura = cv2.VideoCapture('sources/video6.mp4')

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
        




contador = 0

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
                #imagen_area_interes = cv2.resize(imagen_area_interes, (0, 0), fx=3, fy=3)
                imagen_area_interes = cv2.resize(imagen_area_interes, (0, 0), fx=1, fy=1)
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

            

           
            #print(cuerpoResult.pose_landmarks)
            #print(cuerpoResult.pose_world_landmarks)
            
            try:
                contador += 1
                
                #puntos = cuerpoResult.pose_landmarks.landmark
                puntos = cuerpoResult.pose_world_landmarks.landmark
                #Imprimir todos los puntos
                datos = [i for i in puntos]

                ejeX = [i.x for i in datos]
                ejeY = [i.y for i in datos]
                ejeZ = [i.z for i in datos]

                ejeX = np.asarray(ejeX)
                ejeY = np.asarray(ejeY)
                ejeZ = np.asarray(ejeZ)

                puntos_df_temp = pd.DataFrame({"X": ejeX, "Y": ejeY, "Z": ejeZ, "Puntos": parte_Cuerpo, "fotograma": contador})

                #print(puntos_df_temp)
                puntos_df = pd.concat([puntos_df, puntos_df_temp], ignore_index=True)
                
            except:
                pass

            #cv2.putText(image, 'OpenCV', org, font,  
            #       fontScale, color, thickness, cv2.LINE_AA) 
            
            imagen = cv2.putText(imagen,str(contador), (50,50),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,0,255), 2, cv2.LINE_AA)
            cv2.imshow("Imagen", imagen+imagen2)
            cv2.imshow("imagen1", imagen_area_interes)
            cv2.imshow("Gestualizacion", ju)




            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

captura.release()
cv2.destroyAllWindows()

#for punto in cuerpos_mp.PoseLandmark:
#    print(punto)


#puntos = cuerpoResult.pose_landmarks.landmark

#print(type(puntos))

#Imprimir todos los puntos
#datos = [i for i in puntos]

#ejeX = [i.x for i in datos]
#ejeY = [i.y for i in datos]
#ejeZ = [i.z for i in datos]

#ejeX = np.asarray(ejeX)
#ejeY = np.asarray(ejeY)
#ejeZ = np.asarray(ejeZ)

#print(ejeX)
#print(ejeY)
#print(ejeZ)
#puntos_df = pd.DataFrame({"X": ejeX, "Y": ejeY, "Z": ejeZ, "Puntos": parte_Cuerpo})

print(puntos_df)

puntos_df.to_excel("datos/dataEmociones.xlsx")
#puntos_df.to_excel("datos/dataVideo6.xlsx")

#fig = px.scatter_3d(puntos_df, x='X', y='Y', z='Z', color=parte_Cuerpo)
#fig.show()

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Crear una figura 3D
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Crear un mapeo de colores
cmap = plt.get_cmap('tab20b')  # Puedes cambiar 'tab10' por otro mapa de colores
colors = [cmap(i) for i in range(len(puntos_df['Puntos'].unique()))]


# Asignar un color diferente a cada categoría
colormap = {}
for i, category in enumerate(puntos_df['Puntos'].unique()):
    colormap[category] = colors[i]

# Plotear los puntos con colores diferentes
for category in puntos_df['Puntos'].unique():
    subset = puntos_df[puntos_df['Puntos'] == category]
    ax.scatter(subset['X'], subset['Y'], subset['Z'], label=category, color=colormap[category], alpha=0.7)



# Plotear los puntos
ax.scatter(puntos_df['X'], puntos_df['Y'], puntos_df['Z'])

# Etiquetar cada punto
#for i, txt in enumerate(puntos_df['Puntos']):
#    ax.text(puntos_df['X'][i], puntos_df['Y'][i], puntos_df['Z'][i], txt)


# Configurar etiquetas
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')


# Mostrar leyenda
ax.legend()


# Mostrar el gráfico
plt.show()
