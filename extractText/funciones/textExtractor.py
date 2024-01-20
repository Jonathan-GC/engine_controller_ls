from multiprocessing.reduction import duplicate
from operator import index
from tkinter import ttk
import tkinter
import cv2
import easyocr
from sympy import false
import numpy as np
import time

class Extrator_texto:
    
    repositorio_palabras = []
    storage_palabra = []
    palabraAnterior = None
    
    objeto = ""

    def __init__(self, ruta = None, gpu = False) -> None:
        if gpu == False:
            self.salto_de_frames = 15
        else:
            self.salto_de_frames = 5
        self.reader = easyocr.Reader(["es"], gpu=gpu)
        self.cap= cv2.VideoCapture(ruta)


    def find_text(self, borrador = None):
        contador_frames = 0
        while self.cap.isOpened():
            ret, imagen = self.cap.read()

            if ret == False:
                break
            
            if borrador != None:
                #Sistema de Borrador
                for puntos in borrador:
                    cv2.rectangle(imagen, puntos[0], puntos[1], (0, 255, 0), 2)
                    area_for_borrar = imagen[puntos[0][1]: puntos[1][1], puntos[0][0]: puntos[1][0]]
                    # Borrar area con un kernel de (31, 31)
                    area_for_borrar = cv2.blur(area_for_borrar, (31,31), cv2.BORDER_DEFAULT)
                    #Reemplazar esa areas por el nuevo
                    imagen[puntos[0][1]: puntos[1][1], puntos[0][0]: puntos[1][0]] = area_for_borrar

            # Muestra de la imagen
            cv2.imshow("Imagen0", imagen)

            # Analizara el texto cada fotograma dado
            if contador_frames % self.salto_de_frames == 0:
                result = self.reader.readtext(imagen, paragraph=True, text_threshold=0.7 )

                
                if len(result) > 0:
                    

                    try:                    
                        if result[0][1] != "":
                            self.palabraActual = result[0][1]

                            if not self.palabraActual in self.repositorio_palabras:    
                                if len(self.repositorio_palabras) > 1:
                                    self.storage_palabra[-1][-1] = contador_frames 
                                self.repositorio_palabras.append(self.palabraActual)
                                self.storage_palabra.append([contador_frames, self.palabraActual, 0])
                                
                                
                    except:
                        pass

       

                    
                    
    

                        
                            
            
            
            if cv2.waitKey(1)==27:
                break

            # Avanzar el identificador de Frames
            contador_frames += 1
            



        self.cap.release()
        cv2.destroyAllWindows()
        print(self.storage_palabra)

    
class segmentoVideo:
    palabras = []
    def __init__(self):
        pass

    def add(self, frameInicio = 0 , framefin = 0, palabra = None):
        
        if palabra != None:
            if self.palabras.index(palabra) > -1:
                self.palabras.append(palabra)
            
            self.frame_inicial = frameInicio
    
    def get_palabra(self):
        pass
        #return palabra
        
        
        
        

    
    





if __name__ == "__main__":
    
    from reproductor import MediaPlayer
    frame_root = tkinter.Tk()

    #Configuraciones de la ventana
    frame_root.title("Sistema de Mineria TecnoBot")
    frame_root.geometry("1080x720")
    #frame_root.attributes('-alpha', 0.8)

    display = ttk.Frame(frame_root, width=800, height=400)
    display.pack(pady=10, fill='both', expand=True)

    frame_to_barra = ttk.Frame(frame_root, width=800, height=400)
    frame_to_barra.pack(pady=2, fill='x', expand=False)

    inBox_inicio = ttk.Spinbox(frame_to_barra,from_=0, to=100)
    inBox_inicio.pack()

    inBox_Actual = ttk.Spinbox(frame_to_barra, from_ = 0, to=100)
    inBox_Actual.pack()

    inBox_fin = ttk.Spinbox(frame_to_barra, from_=1, to=100)
    inBox_fin.pack()

    boton_buscar_text = ttk.Button(frame_to_barra, text="Extraer Texto")
    boton_buscar_text.pack()

    reproductor = MediaPlayer("sources/feliz-2.mp4", display, frame_to_barra, spinInicio=inBox_inicio, spinFinal=inBox_fin, spinActual=inBox_Actual, mainVideo=False)
    lector=Extrator_texto(ruta="sources/feliz-2.mp4", gpu=True)
    boton_buscar_text.config(command=lambda: lector.find_text([[(70, 54), (280, 170)], [(70, 70), (280, 170)]]))





    frame_root.mainloop()