
from turtle import left, width
from PIL import Image
from PIL import ImageTk
import cv2
import numpy as np
import imutils

import easyocr
import threading
from sympy import false, true

import vlc
from datetime import timedelta
import tkinter as tk
import time
#lector en español
reader = easyocr.Reader(["es"], gpu = True)
from tkinter import *
from tkinter import ttk


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
    progress_bar = None
    
    # Hiper variable de control
    _length                 =   0
    _FPS                    =   0
    _sliding                =   False
    _playing_video          =   False
    _pausing_video          =   False
    _tick_ms                =   100
    _cont_frames            =   0
    _frames_totales         =   0


    def __init__(self, ruta, puntero_frame, frame_to_scale, spinInicio=None, spinFinal=None, spinActual=None):
        
        self._frame_rango_inicial = tk.IntVar()
        self._frame_rango_final = tk.IntVar()
        self._frame_actual = tk.IntVar()
        self._frame_actual.trace_add("write", self.set_video_position)
        
        self.spinInicio=spinInicio
        self.spinFinal=spinFinal
        self.spinActual=spinActual
        self.barra_de_progreso=frame_to_scale
        self.crear_widgets()
        self.initialize_player(puntero_frame, ruta)

        self.spinActual.config(textvariable=self._frame_actual)
        


    def crear_widgets(self):
        self.button_play = BotonesControl(self.barra_de_progreso, "C:/Users/Usuario/Downloads/engine_controller_ls/extractText/app_sources/icons/play.png", self.play_video)
        self.button_play.pack(padx=5, side='left')
        self.button_pausa = BotonesControl(self.barra_de_progreso, "C:/Users/Usuario/Downloads/engine_controller_ls/extractText/app_sources/icons/pausa.png", self.pause_video)
        self.button_pausa.pack(padx=5, side='left')
        self.button_stop = BotonesControl(self.barra_de_progreso, "C:/Users/Usuario/Downloads/engine_controller_ls/extractText/app_sources/icons/stop.png", self.stop_video)
        self.button_stop.pack(padx=5, side='left')
        self.button_anterior = BotonesControl(self.barra_de_progreso, "C:/Users/Usuario/Downloads/engine_controller_ls/extractText/app_sources/icons/anterior.png", self.frame_atras)
        self.button_anterior.pack(padx=5, side='left')
        self.button_adelante = BotonesControl(self.barra_de_progreso, "C:/Users/Usuario/Downloads/engine_controller_ls/extractText/app_sources/icons/adelante.png", self.frame_adelante)
        self.button_adelante.pack(padx=5, side='left')
        
        self.progress_bar = VideoProgressBar(self.barra_de_progreso, self.set_video_position, bg="#e0e0e0", highlightthickness=0, variable=self._frame_actual)
        self.progress_bar.pack(fill=tk.X, padx=10, pady=5)
    

    def eliminar_widgets(self):
        # Destruccion de la barra de progreso y botones
        self.progress_bar.destroy()
        self.button_play.destroy()
        self.button_pausa.destroy()
        self.button_stop.destroy()
        self.button_anterior.destroy()
        self.button_adelante.destroy()

    
    def initialize_player(self, frame, ruta):
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()
        #self.current_file = None
        self.playing_video = False
        self.video_paused = False
        #self.create_widgets()
        media = self.vlc_instance.media_new(ruta)
        
        self.media_player.set_media(media)
        self.media_player.set_hwnd(frame.winfo_id())
        self.play_video()
                  

    def frameActual(self):
        return self.media_player.get_time()//(self.media_player.get_fps() or 1)
    
    
    def frames_totales(self):
        try:
            self.media_player.duration()//self.media_player.get_fps()
        except:
            pass
    
    def set_video_position(self, value, *args):
    
        if self.progress_bar.is_cliked() and  self.playing_video == True:
            # Pausa el video para evitar que se siga reproduciendo 
            # no es necesario pero el programa se ve mas consistente
            self.pause_video()
            self._sliding = False

            # Cancela el hilo de actualización
            self.progress_bar.after_cancel(self.tick_f)
            
            
            # Se calcula el numero de Frames a tiempo y se establece el reproductor
            numero_de_frame = self.calcular_frame_to_time(self.progress_bar.get())
            self.media_player.set_time(numero_de_frame)

            #Iniciar nuevamente la reproduccion y actualizacion de la barra de progreso
            self.play_video()
            self.update_progres_video()

        elif self.progress_bar.is_cliked() and self._pausing_video:
            self._frame_actual = self.progress_bar.get()
            
            #if self.spinActual:
            #    self.spinActual.set(self.progress_bar.get())
            # Se calcula el numero de Frames a tiempo y se establece el reproductor
            numero_de_frame = self.calcular_frame_to_time(self.progress_bar.get())
            self.media_player.set_time(numero_de_frame)
        
        elif self._pausing_video:
            value = self._frame_actual.get()
            # Se calcula el numero de Frames a tiempo y se establece el reproductor
            numero_de_frame = self.calcular_frame_to_time(value)
            self.media_player.set_time(numero_de_frame)
    

    
    def update_progres_video(self):
        
        if self.media_player and self.playing_video:
            barra = self.progress_bar
            p = self.media_player
            
            if self._length > 0:
                
                if not self._sliding:                    
                    t = max(0, self.calcular_time_to_frame(p.get_time()))
                    if t != barra.get():
                        # Actualizar Barra de progreso
                        #barra.set(t)

                        self._frame_actual.set(t)

                        # Actualizar etiqueta
                        #if self.spinActual:
                        #    self.spinActual.set(t)
                        
            else:
                self._length = tamanio_ms = self.media_player.get_length()
                
                if tamanio_ms > 0:
                    # Obtener los FPS
                    self._FPS = fps = self.media_player.get_fps()
                    
                    # Obtener Frecuencia de Actualización
                    self._tick_ms = 1000//fps
                    
                    # fps totales calculados de (FPS * tamanio_total_ms/1000ms)
                    self._frames_totales = fps*tamanio_ms/1000

                    
                    barra.config(to=self._frames_totales)
                    self.spinActual.config(to=self._frames_totales)
                    

            # re-start cada fotograma
            self.tick_f = self.progress_bar.after(int(self._tick_ms), self.update_progres_video)
            #self.tick_f = self.progress_bar.after(250, self.update_progres_video)
    
    def calcular_frame_to_time(self, numero_de_frame):
        pendiente = 1000//self._FPS
        position_ms = pendiente * numero_de_frame
        return int(position_ms)
    
    def calcular_time_to_frame(self, tiempo):
        return tiempo // self._tick_ms
        

    def play_video(self):
        if not self.playing_video:
            self.media_player.play()
            self.playing_video = True
            self._pausing_video=False
            self.update_progres_video()

    def pause_video(self):
        if self.playing_video == True:
            self.progress_bar.after_cancel(self.tick_f)
            self.media_player.pause()
            self.playing_video = False
            self._pausing_video=True
            
            """
            if self.video_paused == True:
                self.video_paused = False
                self.play_video()
            else:
                self.media_player.pause()
                self.video_paused = True
    
            """
    
    
    def stop_video(self):
        if self.playing_video == True:
            self.media_player.stop()
            self.playing_video = False
            self.progress_bar.set(0)
        
    def frame_adelante(self):
        self.pause_video()
        if self._pausing_video == True:
            #self.media_player.next_frame()
            tiempo_adelante = self.media_player.get_time() + self._tick_ms
            self.media_player.set_time(int(tiempo_adelante))
            self.progress_bar.set(self.media_player.get_time() // self._tick_ms)
            
            self._frame_actual.set(self.media_player.get_time() // self._tick_ms)
            #if self.spinActual:
            #    self.spinActual.set(self.media_player.get_time() // self._tick_ms)
    
    def frame_atras(self):
        self.pause_video()
        if self._pausing_video == True:
            tiempo_anterior = self.media_player.get_time() - self._tick_ms
            self.media_player.set_time(int(tiempo_anterior))
            self.progress_bar.set(tiempo_anterior // self._tick_ms)
            #if self.spinActual:
            #    self.spinActual.set(tiempo_anterior // self._tick_ms)
            




    def ClosePlayer(self):
        
        #print("FPS: ",self.media_player.get_fps())
        #print("Time now ", self.media_player.get_time())
        #print("Tiempo Total", self.media_player.get_length())
        
        # Detener el video
        self.media_player.stop()
        self.playing_video = False
        #Parar la barra de progreso
        self.progress_bar.after_cancel(self.progress_bar)
        #Destruccion de la barra de progreso y botones
        self.eliminar_widgets()
        # Destruccion del reproductor
        self.media_player.release()
        

    
   
            
        
    
    def funcionBandera(self):
        print("Nooo jodaa")
        self._sliding = False
            
        
        

class VideoProgressBar(tk.Scale):
    def __init__(self, master,command, **kwargs):
        #kwargs["showvalue"] = False
        super().__init__(
            master,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            #sliderlength=15,
            cursor='dot',
            command=command,
            **kwargs,
        )
        self.bind("<ButtonRelease-1>", self.on_click)
        self.clicking = False
    
    def on_click(self, event):
        
        if self.cget("state") == tk.NORMAL:
            """
            -> Evento en X obtiene el valor desde 0 hasta el ancho maximo de la ventana
            -> self config('to') devuelve el ultimo valor asignado al ancho
            -> self.winfo_width() devuelve el ancho de la ventana
            Se calcula usando regla de tres para obtener el contexto de click en toda la barra de progreso
            """
            value = (event.x * self.config('to')[-1]) / self.winfo_width()
            self.set(value)
            self.clicking = True   
            #Promesa de ejecucion despues de 1500 ms
            self.after(1000, self._desactivarClicked)
    
    
    def is_cliked(self):
        # Pregunta si esta activado el evento
        return self.clicking
    
    def _desactivarClicked(self):
        # Desactivar el evento
        self.clicking = False
    

class BotonesControl(tk.Button):
    def __init__(self, master, icono, command, **kwargs):
        # Importar y remuestrear a 30X30 px
        from PIL import Image, ImageTk
        imagen = Image.open(icono)
        imagen = imagen.resize((30, 30))

        # Conver the image in TkImage
        self.imagen_boton = ImageTk.PhotoImage(imagen)
        super().__init__(
            master,
            image=self.imagen_boton,
            command=command,
            **kwargs
            )


    
        

            
        


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

    frame_to_barra = Frame(frame_root, bg="black", width=800, height=400)
    frame_to_barra.pack(pady=2, fill='x', expand=False)
    
    reproductor = MediaPlayer("sources/Martin Miller.mp4", display, frame_to_barra)
    #reproductor = MediaPlayer("sources/feliz-2.mp4", display, frame_to_barra)
    #reproductor = MediaPlayer("sources/feliz_3.mp4", display, frame_to_barra)
    #reproductor = MediaPlayer("sources/pexels.mp4", display, frame_to_barra)
    #reproductor.update_progres_video()
    

    frame_root.mainloop()

    


