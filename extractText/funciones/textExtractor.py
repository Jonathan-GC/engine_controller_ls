from multiprocessing.reduction import duplicate
from operator import index
from sys import exception
from tkinter import ttk
import tkinter
import cv2
import easyocr
from sympy import false
import numpy as np
import time

# Libreria de Scikit-learn para similitud de vectores
from scipy.spatial.distance import cosine
from torch import randint
class Extrator_texto:
    aperturador_de_frase = False
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
        aperturador_de_frase = False
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
                result = self.reader.readtext(imagen, paragraph=True, text_threshold=0.8, batch_size=2)

                # Apertura del candado de frase
                if len(result) > 0:
                    # Abrir el candado
                    aperturador_de_frase = True
                    try:                    
                        if result[0][1] != "":
                            #Extraer la palabra
                            self.palabraActual = result[0][1]

                            #Normalizar la palabra para evitar tildes
                            self.palabraActual = self.normalize(self.palabraActual)
                            
                            # Averiguar si ya hay una palabra similar, si la hay no la almacena y continua
                            if self.repositorio_palabras:
                                print(self.palabraActual)
                                size_word_actual    = len(self.palabraActual)
                                size_word_backward  = len(self.repositorio_palabras[-1])
                                
                                if size_word_actual == size_word_backward:
                                    #Antes de agregar calcula si la palabra es similar a otra
                                    if self.simulitud_de_palabras(self.palabraActual, self.repositorio_palabras[-1]) > 0.1:
                                        # Agregar palabra a los resultados
                                        #self.storage_palabra.append([contador_frames, self.palabraActual, 0])
                                        self._agregar_palabra(contador_frames)

                                elif size_word_actual - size_word_backward > 0 and size_word_actual - size_word_backward <= 2:
                                    
                                    # si es mas grande, elimine un caracteres aleatorios
                                    # no mas que el tamaño de la lista mas pequeña y calcule similitud.
                                    if self.simulitud_de_palabras(self.palabraActual, self.repositorio_palabras[-1], igualarVectores=True) > 0.0045:
                                        # a la palabra anterior coloquele el fin del frame
                                        self._agregar_palabra(contador_frames)
                                    
                                elif size_word_actual - size_word_backward >= -2 and size_word_actual - size_word_backward < 0:
                                    
                                    if self.simulitud_de_palabras(self.palabraActual, self.repositorio_palabras[-1], igualarVectores=True) > 0.0045:
                                        self._agregar_palabra(contador_frames)


                                else:
                                    
                                    # cuando la palabra es diferente en todo sentido se agrega y se actualiza el repositorio de palabras
                                    self._agregar_palabra(contador_frames)

                                
                            else:
                                #Corresponde a la primera entrada, cuando no hay nada en el Array
                                self.storage_palabra.append([contador_frames, self.palabraActual, 0])
                                self.repositorio_palabras.append(self.palabraActual)
                            
                    except Exception as error:
                        print(error)
                    

                    

            if cv2.waitKey(1)==27:
                break

            # Avanzar el identificador de Frames
            contador_frames += 1
            
        self.cap.release()
        cv2.destroyAllWindows()
        for element in self.storage_palabra:
            print(element)




    def normalize(self, cadena):
        """Modulo para eliminar tildes de cada palabra"""
        replacements = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
            ("@", "e"),
        )

        for a, b in replacements:
            cadena = cadena.replace(a, b).replace(a.upper(), b.upper())
        
        return cadena

    def simulitud_de_palabras(self, texto_in_1, texto_in_2, igualarVectores = False, caracteres_para_eliminar = 0):
        """
        Convierte las cadenas en ordinales para ser analizadas como numeros
        Se aplica el coseno para conocer que tan  similares son las dos cadenas
        las pruebas experimentales muestras 

        coseno "mi cadena", "mi cadena" = 0 : Similitud exacta
        coseno "mi caneca", "mi cadena" = 0.0013031388355694284 : palabras vecxtorialmente similares
        coseno "mi cadena", "la novena" = 0.0031400294279362306 : palabras vectorialmente mas alejadas
        """
        texto_in_1 = texto_in_1.replace(" ", "")
        texto_in_2 = texto_in_2.replace(" ", "")
        x = [ord(letra) for letra in texto_in_1]
        y = [ord(letra) for letra in texto_in_2]

        if len(x) > len(y):
            import random
            for i in range(len(x) - len(y)):
                x.pop(random.randint(0, len(x) - len(y)))
        elif len(y) > len(x):
            import random
            for i in range(len(y) - len(x)):
                y.pop(random.randint(0, len(y) - len(x)))

        a = np.array(x)
        b = np.array(y)
        #print("coseno de vectores: ", cosine(a, b))
        return cosine(a, b)

    def _agregar_palabra(self, contador_frames):
        # a la palabra anterior coloquele el fin del frame
        self.storage_palabra[-1][-1] = contador_frames-self.salto_de_frames
        self.storage_palabra.append([contador_frames, self.palabraActual, 0])
        self.repositorio_palabras.append(self.palabraActual)
        




    
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