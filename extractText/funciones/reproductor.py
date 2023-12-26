
from PIL import Image
from PIL import ImageTk
import cv2
import numpy as np
import imutils

import easyocr
import threading

import vlc
from datetime import timedelta
import tkinter as tk
import time
#lector en español
reader = easyocr.Reader(["es"], gpu = True)
from tkinter import *


class Visualizador_Video:

    # Esta variable permite almacenar la ultima tarea 
    # y terminar los procesos he hilos de ejecución
    last_task = None

    #Roi Definido por dos puntos
    p1, p2 = None, None # Roi Persona

    list_puntos_difuminar = []
    p3, p4 = None, None # Roi Texto
    
    estado = 0
    estado1 = 0
    dimensiones = (480, 640)
    imagen_general = np.zeros(dimensiones, np.uint8)
    imagen_respaldo = np.zeros(dimensiones, np.uint8)

    mostrar_ventana = False
    
    #Bandera para los eventos cuando se presiona la tecla 'ALT'
    bandera_ALT = 0

    # Fotograma de Inicio y Fin
    Senias_encontradas = []
    palabraAnterior = None
    contador = 0

    def __init__(self, etiquetaVideo, etiquetaRoiPersonaje, etiquetaRoiText, etiquetaBodyPoints ) -> None:
        self.etiquetaVideo = etiquetaVideo
        self.etiquetaRoiPersonaje = etiquetaRoiPersonaje
        self.etiquetaRoiText = etiquetaRoiText
        self.etiquetaBodyPoints = etiquetaBodyPoints
        


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
                    #Extraer las dimensiones y colocarlas en el tablero general
                    self.dimensiones = imagen.shape
                    self.imagen_general=imagen.copy()
                    self.imagen_respaldo=imagen.copy()

                    if self.mostrar_ventana:
                        # si el roi esta seleccionado dibujelo
                        if self.estado  > 1:
                            cv2.rectangle(self.imagen_general, self.p1, self.p2, (255, 0, 0), 2)
                            imagen_persona = self.imagen_general[int(self.p1[1]) : int(self.p2[1]), int(self.p1[0]) : int(self.p2[0])]
                            imagen_persona = imutils.resize(imagen_persona, height=250)
                            imagen_persona = cv2.cvtColor(imagen_persona, cv2.COLOR_BGR2RGB)
                            im_persona = Image.fromarray(imagen_persona)
                            img_persona = ImageTk.PhotoImage(image=im_persona)
                            self.etiquetaRoiPersonaje.configure(image=img_persona)
                            self.etiquetaRoiPersonaje.image = img_persona
                        
                        for puntos in self.list_puntos_difuminar:
                            cv2.rectangle(self.imagen_general, puntos[0], puntos[1], (0, 255, 0), 2)
                            area_for_borrar = self.imagen_general[puntos[0][1]: puntos[1][1], puntos[0][0]: puntos[1][0]]
                            # Borrar area con un kernel de (31, 31)
                            area_for_borrar = cv2.blur(area_for_borrar, (31,31), cv2.BORDER_DEFAULT)
                            imagen[puntos[0][1]: puntos[1][1], puntos[0][0]: puntos[1][0]] = area_for_borrar

                            """
                            cv2.rectangle(self.imagen_general, self.p3, self.p4, (0, 255, 0), 5)
                            imagen_texto = self.imagen_general[int(self.p3[1]) : int(self.p4[1]), int(self.p3[0]) : int(self.p4[0])]
                            imagen_texto = imutils.resize(imagen_texto, height=250)
                            imagen_texto = cv2.cvtColor(imagen_texto, cv2.COLOR_BGR2RGB)
                            im_texto = Image.fromarray(imagen_texto)
                            img_texto = ImageTk.PhotoImage(image=im_texto)
                            self.etiquetaRoiText.configure(image=img_texto)
                            self.etiquetaRoiText.image = img_texto
                            """
                        cv2.imshow("Imagen", self.imagen_general)
                        
                        palabra = self.analisiText(imagen)
                        print(palabra)
                        
                        """
                        if palabra:
                            fotograma_inicio = self.contador
                            
                            self.Senias_encontradas.append()
                        """
                        


                    else:
                        cv2.destroyAllWindows()

                    # 1. Redimensionar al tamaño del GUI
                    imagen = imutils.resize(imagen, height=480)
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
                    cv2.destroyAllWindows()
        except:
            pass    

    # Llamada a eventos del mouse
    def seleccionar_area(self, event, x, y, flags, param):

        if flags == cv2.EVENT_FLAG_ALTKEY:
            self.bandera_ALT = 1
        
        # Ejemplos de acciones con algunos eventos del mouse   
        if event == cv2.EVENT_LBUTTONDBLCLK:
            
            if  self.bandera_ALT and  self.estado1 == 0:
                self.p3 = (x, y)
                self.estado1 = 1
            
            elif self.bandera_ALT and self.estado1 == 1:
                self.p4 = (x, y)
                self.list_puntos_difuminar.append([self.p3, self.p4])
                self.estado1 = 0
                self.bandera_ALT = 0
            
            #Seleccionar primer punto
            elif self.estado == 0:
                self.p1 = (x, y)
                self.estado = 1
            
            #selecionar segundo punto
            elif self.estado == 1:
                self.p2 = (x, y)
                self.estado = 2
            


        if self.bandera_ALT and event == cv2.EVENT_RBUTTONUP:
            self.p3, self.p4 = None, None
            self.list_puntos_difuminar = []

            # Llamado a la limpieza de la imagen
            self.limpiarImagen()

        elif event == cv2.EVENT_RBUTTONUP:
            self.p1, self.p2 = None, None
            self.estado = 0
            
            

    def motrar_roi(self):
        # Activar la ventana de opencv
        self.mostrar_ventana = True
        cv2.namedWindow('Imagen')  
        
        # Introducir los callBack del mouse
        cv2.setMouseCallback("Imagen", self.seleccionar_area)

    def limpiarImagen(self):
        self.imagen_general = self.imagen_respaldo

        
        
        
        

    def quitar_ventana(self):
        self.mostrar_ventana = False

    def analisiText(self, img, frame_inicio, frame_fin):
        try:
            # Ralizacion del analisis de texto sobre imagen
            result = reader.readtext(img, paragraph=False)

            # If encuentra algo con una certeza mayor del 60%
            if(result[0][1] > 0.6):
                # Retorne el numero del fotograma y la palabra
                return result[0][1]
                
        #return result
        except:
            return ""
    
    
class MediaPlayer:
    ruta = None
    def __init__(self, ruta, puntero_frame, frame_to_scale):
        self.initialize_player(puntero_frame, ruta)
        self.progress_bar = VideoProgressBar(frame_to_scale, self.joder(), bg="#e0e0e0", highlightthickness=0)
        self.progress_bar.pack(fill=tk.X, padx=10, pady=5)
        
    
    def initialize_player(self, frame, ruta):
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()
        #self.current_file = None
        #self.playing_video = False
        #self.video_paused = False
        #self.create_widgets()
        media = self.vlc_instance.media_new(ruta)
        
        self.media_player.set_media(media)
        self.media_player.set_hwnd(frame.winfo_id())
        self.media_player.play()
        
        
        print(self.media_player.get_time())
        print(self.media_player.get_length())

    def ClosePlayer(self):
        self.media_player.stop()
        self.progress_bar.destroy()
        #self.media_player.close()
    
    def joder(self):
        print("Joder Tio")

class VideoProgressBar(tk.Scale):
    def __init__(self, master, command, **kwargs):
        kwargs["showvalue"] = False
        super().__init__(
            master,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            sliderlength=15,
            cursor='dot',
            **kwargs,
        )
        #self.bind("<Button-1>", self.on_click)
    
    def on_click(self, event):
        """
        if self.cget("state") == tk.NORMAL:
            value = (event.x / self.winfo_width()) * 100
            self.set(value)
        """
        pass


if __name__ == "__main__":
    #app = MediaPlayer()
    #app.update_video_progress()
    #app.mainloop()

    #Ventana principal
    frame_root = Tk()

    #Configuraciones de la ventana
    frame_root.title("Sistema de Mineria TecnoBot")
    frame_root.geometry("1080x720")
    frame_root.config(bg='white')

    display = Frame(frame_root, bg="black", width=800, height=400)
    display.pack(pady=10, fill=tk.BOTH, expand=True)
    print(display.winfo_id())
    print(frame_root.winfo_id())
    reproductor = MediaPlayer("sources/Martin Miller.mp4", display )

    frame_root.mainloop()

    


