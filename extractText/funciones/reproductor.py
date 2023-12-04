
from PIL import Image
from PIL import ImageTk
import cv2
import numpy as np
import imutils

global last_task #Esta variable permite almacenar la ultima tarea y terminar los procesos he hilos de ejecución

last_task = None

def iniciar_video(ruta, lblVideo):
    global last_task
    
    cap = cv2.VideoCapture(ruta)
    if last_task is not None:
        lblVideo.after_cancel(last_task)
    
    visualizar(cap, lblVideo)

    


def visualizar(captura, lblVideo):
    global last_task
    try:
        #Extraer la velocidad del video en ms
        fps = int(captura.get(cv2.CAP_PROP_FPS))
        #Sacar la velocidadf del video de tipo entero
        velocidad_video = (1000//fps)

        if captura is not None:
            ret, imagen = captura.read()
            if ret == True:
                # 1. Redimensionar al tamaño del GUI
                imagen = imutils.resize(imagen, width=750)
                # 2. Colorear en RGB, ya que originalmente viene en BGR
                imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
                # 3. Convertir en Imagen
                im = Image.fromarray(imagen)
                img = ImageTk.PhotoImage(image=im)
                # 4. colocar en el puntero a la etiqueta Original
                lblVideo.configure(image=img)
                lblVideo.image = img
                # 5. Iniciar el procesamiento en paralelo y guardar el id de la tarea para pararla cuando desee
                last_task = lblVideo.after(velocidad_video, visualizar, captura, lblVideo)
                
            else:
                #Quitar la captura
                captura.release()
    except:
        pass    
