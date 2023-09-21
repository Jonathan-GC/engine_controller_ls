import cv2
import numpy as np
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2



captura = cv2.VideoCapture('sources/video3.mp4')


import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.python._framework_bindings import image as image_module

def analizarRostro(FaceLandmarkerResult, image_module):
    print("hola")

base_options = python.BaseOptions(model_asset_path='modelos/face_landmarker.task')
options = vision.FaceLandmarkerOptions(running_mode=3,
                                       base_options=base_options,
                                       output_face_blendshapes=True,
                                       output_facial_transformation_matrixes=True,
                                       num_faces=1,
                                       result_callback=analizarRostro)

with vision.FaceLandmarker.create_from_options(options) as detector:
    
    #introducir los callBack del mouse
    cv2.namedWindow('Imagen')
    while(captura.isOpened()):

        _, imagen = captura.read()
        
        
        #x = mp.ImageFormat(1)
        #mp.ImageFrame(x)
        #print(x)
        if _  == 0:
            break
        
        else:
            
            cv2.imshow("Gestualizacion", imagen)



            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

captura.release()
cv2.destroyAllWindows()



