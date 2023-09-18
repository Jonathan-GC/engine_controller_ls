from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import matplotlib.pyplot as plt
import time



import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision

#Elecccion de la libreria necesxarias para el entrenamiento
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


#Aqui se van a almacenar cada una de las emociones que se transmiten en los frames
emociones = list()


#Opciones del analizador de rotro para video
options = FaceLandmarkerOptions(
  base_options = BaseOptions(model_asset_path="modelos/face_landmarker.task"),
  running_mode = VisionRunningMode.VIDEO,
  output_face_blendshapes=True,
  num_faces=1
)


#Fuente de alimentacion, captura de fps, para poder conseguir el triempo de analisis de los frames
cap = cv2.VideoCapture("sources/video3.mp4")
fps = cv2.CAP_PROP_FPS
timeNow = 0


#Hilo de arranque para el reconocedor de imagen
with FaceLandmarker.create_from_options(options) as landmarker:

  while(1):

    #Lectura
    ret, imagen = cap.read()

    #Salida rapida en caso de error
    if not ret:
      break
    else:
      
      #Transformo la imagen a RGB ya que es una exigencia de la libreria
      imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

      #La reescalo para evitar demoras en el proceso aunque no es necesario pero prefiero tener optimos resultados
      imagen = cv2.resize(imagen, (0,0), fx=0.4, fy=0.4)
      
      #Muestro la imagen original pero aun la convierto a BGR
      cv2.imshow("imagen Original", imagen)

      #Vectorizacion de la imagen con el modelo para el analisis dew las caracteristicas del rostro
      mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imagen)
      
      #Calculo el tiempo ya que va a ser importante para el tiempo del detector, este hasta el momento me da resultados optimos y no traba el proceso como el faceMesh
      timeNow
      face_landmarker_result = landmarker.detect_for_video(mp_image, timeNow)
      timeNow += 1000//fps


      #Las emociones detectadas la añado a lista de emociones para se posteriormente ser almacenadas como entrenamiento
      emociones.append(face_landmarker_result)
        

      if (cv2.waitKey(1) == 27):
        
        break
      




cap.release()
cv2.destroyAllWindows()



#Funcion para plotear las emociones en subplots
fig1 = plt.figure("Filtro")
fig1.subplots_adjust(hspace=2, wspace=2)



# Funcion de graficación
def graficar_emocion(emocion, index):

    #obtencion de caracteristicas
    caracteristicas = emocion.face_blendshapes[0]

    #Captura de las variables principales
    nombreCaracteristicas = [caracteristica.category_name for caracteristica in caracteristicas]
    calificacionCaracteristicas = [calificacion.score for calificacion in caracteristicas] 
    rangos = range(len(nombreCaracteristicas))

    #Inicio del plot
    ax = fig1.add_subplot(index)
    bar = ax.barh(rangos, calificacionCaracteristicas, label=[str(x) for x in rangos])

    ax.set_yticks(rangos, nombreCaracteristicas)
    ax.invert_yaxis()
    
    ax.set_axis_off()

    #etiquetar cada barra
    #for score, patch in zip(calificacionCaracteristicas, bar.patches):
    #    plt.text(patch.get_x() +  patch.get_width(), patch.get_y(), f"{score: .4f}", va = "top")

    #ax.set_label("Calificacion")
    #ax.set_title("Caracteristicas Rostro")
    #plt.tight_layout()
    
    





#Pasar el ploteo para cada emocion
for i, emoticon in enumerate(emociones):
  try:
    graficar_emocion(emoticon, i)
  except:
    pass

 
#Mostrar los resultados
plt.show()