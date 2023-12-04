
from PIL import Image
from PIL import ImageTk
import cv2
import numpy as np
import imutils

global last_task #Esta variable permite almacenar la ultima tare y terminar los procesos he hilos de ejecución

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
        velocidad_video = (1000//fps)

        if captura is not None:
            ret, frame = captura.read()
            if ret == True:
                frame = imutils.resize(frame, width=750)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=im)
                lblVideo.configure(image=img)
                lblVideo.image = img
                last_task = lblVideo.after(velocidad_video, visualizar, captura, lblVideo)
                
            else:
                #lblVideo.image = ""
                captura.release()
    except:
        pass    
