
from PIL import Image
from PIL import ImageTk
import cv2
import numpy as np
import imutils


class Visualizador_Video:

    # Esta variable permite almacenar la ultima tarea 
    # y terminar los procesos he hilos de ejecución
    last_task = None

    def __init__(self, etiquetaVideo) -> None:
        self.etiquetaVideo = etiquetaVideo
        


    def iniciar_video(self, ruta):
                
        cap = cv2.VideoCapture(ruta)
        if self.last_task is not None:
            self.etiquetaVideo.after_cancel(self.last_task)
        
        self._visualizar(cap)

        


    def _visualizar(self, captura):
    
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
                    self.etiquetaVideo.configure(image=img)
                    self.etiquetaVideo.image = img
                    # 5. Iniciar el procesamiento en paralelo y guardar el id de la tarea para pararla cuando desee
                    self.last_task = self.etiquetaVideo.after(velocidad_video, self._visualizar, captura)
                    
                else:
                    #Quitar la captura
                    captura.release()
        except:
            pass    
