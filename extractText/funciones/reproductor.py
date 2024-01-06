from PIL import Image
from PIL import ImageTk
import cv2
import numpy as np
import imutils

import easyocr
from sympy import capture, false, true

import vlc
from datetime import timedelta
import tkinter as tk
import time
#lector en español
reader = easyocr.Reader(["es"], gpu = True)
from tkinter import *
from tkinter import ttk


class visualizador_video2:
    _activate_borrador      = False
    _activate_roi_on_person = False
    name_window = "Ventana Edición"
    
    #Roi Definido por dos puntos
    p1, p2 = None, None # Roi Persona
    list_marcos_persona = []

    list_puntos_difuminar = []
    p3, p4 = None, None # Roi Texto
    
    _estado = 0 #Biestable para los clicks del mouse
    _estado1 = 0 #Biestable para los clicks del mouse
    _len_actual = 0 #Permite conocer el tamaño la lista de puntos difuminados
    _len_anterior = 0#Permite conocer si el tamaño la lista cambió
    _destruir_window = False
    
    contador_frames = 0

    def __init__(self, ruta):
        self.tamanio_video = 0.5
        self.ruta = ruta
    
    def mostrarImagen(self, route):
        """
        Mostrar la imagen sobre la que se van a realizar los respectivos marcos de borrado y areas de interes
            route -> str: Recibe la ruta donde se almacena el archivo temporal que se va a leer y marcar
        """
        img = cv2.imread(route)
        # Respaldar la imagen
        self.imagen_respaldo=img.copy()
        self.imagen_general=img.copy()
        self.imagen_persona = img.copy() 
        while True:

            # Extraer el tamaño de los puntos a difuminar
            self._len_actual = len(self.list_puntos_difuminar)

            if self._len_actual != self._len_anterior:

                # Roi para eliminar texto inecesario de los videos
                for puntos in self.list_puntos_difuminar:
                    cv2.rectangle(img, puntos[0], puntos[1], (0, 255, 0), 2)
                    area_for_borrar = self.imagen_general[puntos[0][1]: puntos[1][1], puntos[0][0]: puntos[1][0]]
                    # Borrar area con un kernel de (31, 31)
                    area_for_borrar = cv2.blur(area_for_borrar, (31,31), cv2.BORDER_DEFAULT)
                    #Reemplazar esa areas por el nuevo
                    self.imagen_general[puntos[0][1]: puntos[1][1], puntos[0][0]: puntos[1][0]] = area_for_borrar
                

                # Actualizar el valor de la lista
                self._len_anterior = self._len_actual

            
            # Para dar un roi sobre Persona
            if self._estado  == 2:
                cv2.rectangle(self.imagen_general, self.p1, self.p2, (255, 0, 0), 2)
                self.imagen_persona = self.imagen_general[int(self.p1[1]) : int(self.p2[1]), int(self.p1[0]) : int(self.p2[0])]
                
            
            
            if self.mostrar_ventana:
                cv2.imshow(self.name_window, self.imagen_general)

                # Espera a que el usuario procione una tecla para continuar
                if cv2.waitKey(50) == 27 or self._destruir_window:
                    self._len_anterior = 0 # Reiniciar la variable para que al abrir nuevamente la ventana haga el checking de los puntos establecidos
                    self._destruir_window = False
                    break
            

        cv2.destroyWindow(self.name_window)

    
    def mostrarVideo(self):
        """
        Abre una ventana OpenCV que permite el analisis de imagen
        """
        #Iniciacion del video
        self.capture = cv2.VideoCapture(self.ruta)
        
        while true:
            ret, img = self.capture.read()
            if not ret:
                break
            else:
                self.imagen_general=img.copy()
                self.imagen_respaldo=img.copy()
                
                # Para dar un roi sobre Persona
                if self._estado  == 2:
                    img = cv2.rectangle(img, self.p1, self.p2, (255, 0, 0), 2)
                    self.imagen_persona = self.imagen_general[int(self.p1[1]) : int(self.p2[1]), int(self.p1[0]) : int(self.p2[0])]
                    

                # Roi para eliminar texto inecesario de los videos
                for puntos in self.list_puntos_difuminar:
                    # Dibujar Rectangulo
                    cv2.rectangle(img, puntos[0], puntos[1], (0, 255, 0), 2)
                    area_for_borrar = self.imagen_general[puntos[0][1]: puntos[1][1], puntos[0][0]: puntos[1][0]]
                    # Borrar area con un kernel de (31, 31)
                    area_for_borrar = cv2.blur(area_for_borrar, (31,31), cv2.BORDER_DEFAULT)
                    #Reemplazar esa areas por el nuevo
                    img[puntos[0][1]: puntos[1][1], puntos[0][0]: puntos[1][0]] = area_for_borrar


                if self.mostrar_ventana:
                    cv2.imshow(self.name_window, img)
                    if cv2.waitKey(1) == ord("q"):
                        break
        self.capture.release()
        cv2.destroyWindow(self.name_window)

    # Llamada a eventos del mouse
    def seleccionar_area(self, event, x, y, flags, param):

        # Ejemplos de acciones con algunos eventos del mouse   
        if event == cv2.EVENT_LBUTTONDBLCLK:
            
            if  self._activate_borrador and  self._estado1 == 0:
                self.p3 = (x, y)
                self._estado1 = 1
            
            elif self._activate_borrador and self._estado1 == 1:
                self.p4 = (x, y)
                #Pasar por el filtro de orden y evitar errores a la hora de dibujar
                p3, p4 = self.organizador_de_puntos(self.p3, self.p4)
                self.list_puntos_difuminar.append([p3, p4])
                self._estado1 = 0
            
            #Seleccionar primer punto
            elif self._activate_roi_on_person and self._estado == 0:
                self.p1 = (x, y)
                self._estado = 1
            
            #selecionar segundo punto
            elif self._activate_roi_on_person and self._estado == 1:
                self.p2 = (x, y)
                self.p1, self.p2 = self.organizador_de_puntos(self.p1, self.p2)
                self._estado = 2

        if self._activate_borrador and event == cv2.EVENT_RBUTTONUP:
            # Llamado a la limpieza de la imagen
            self.limpiarImagen()
            self.p3, self.p4 = None, None
            self.list_puntos_difuminar.clear()
            

        elif self._activate_roi_on_person and event == cv2.EVENT_RBUTTONUP:
            self._estado = 0
            self.p1, self.p2 = None, None
            self.imagen_persona = self.imagen_respaldo.copy()
            self._destruir_window = True

        

            
    def organizador_de_puntos(self, punto1, punto2):
        """
        Esta funcion permite organizar el orden de los puntos para que todo dibujo
        que se haga siempre vaya de menor a mayor y devuelve una tupla con esos
        puntos ordenados 
        """
        xmin, ymin = punto1
        xmax, ymax = punto2

        if ymin < ymax:
            if xmin < xmax:
                return (xmin, ymin), (xmax, ymax)
            else:
                return (xmax, ymin), (xmin, ymax)
        else:
            if xmin > xmax:
                return (xmax, ymax), (xmin, ymin)
            else:
                return (xmin, ymax), (xmax, ymin)

    def motrar_roi(self, mode):
        """
        Funcion para activar los roi de borrador y persona
        value->int: 1. ativar borrador
                    2. activar roi persona
        """
        # Activar la ventana de opencv
        self.mostrar_ventana = True
        if mode == 1:
            self.activar_Roi_on_person(False)
            self.activar_borrador(True)
        elif mode == 2:
            self.activar_borrador(False)
            self.activar_Roi_on_person(True)

        cv2.namedWindow(self.name_window)  
        # Introducir los callBack del mouse
        cv2.setMouseCallback(self.name_window, self.seleccionar_area)
    def limpiarImagen(self):
        self.imagen_general = self.imagen_respaldo.copy()
    def activar_borrador(self, value):
        """
        Activar o desactivar borrador
        value: int -> True.  activar; 
                      False. desactivar 
        """
        self._activate_borrador = True if value else False
    def activar_Roi_on_person(self, value):
        """
        Activar o desactivar ROI sobre el personaje principal a analizar
        Sino se activa el tomara el personaje unico o el mas "grande" existente 
        por inferencia
        value: int -> True.  activar; 
                      False. desactivar 
        """
        self._activate_roi_on_person = True if value else False


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

    def __init__(self, etiquetaVideo=None, etiquetaRoiPersonaje=None, etiquetaRoiText=None, etiquetaBodyPoints=None ) -> None:
        self.etiquetaVideo = etiquetaVideo
        self.etiquetaRoiPersonaje = etiquetaRoiPersonaje
        self.etiquetaRoiText = etiquetaRoiText
        self.etiquetaBodyPoints = etiquetaBodyPoints
        self.motrar_roi()
    
    def iniciar_imagen(self, ruta):
        imagen = cv2.imread(ruta)
        cv2.imshow("Imagen", imagen)
        cv2.waitKey()
        cv2.destroyWindow("Imagen")


    def iniciar_video(self, ruta):
                
        self.cap = cv2.VideoCapture(ruta)
        if self.last_task is not None:
            self.etiquetaVideo.after_cancel(self.last_task)
        
        self._visualizar()



    def _visualizar(self):
        captura=self.cap
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
                            #self.etiquetaRoiPersonaje.configure(image=img_persona)
                            #self.etiquetaRoiPersonaje.image = img_persona
                        
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
                        
                        #palabra = self.analisiText(imagen)
                        #print(palabra)
                        
                        """
                        if palabra:
                            fotograma_inicio = self.contador
                            
                            self.Senias_encontradas.append()
                        """
                        


                    else:
                        cv2.destroyAllWindows()

                    """
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
                    """
                    
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
    _snapshot               =   "1aa5cd5e16848db5fd9be65a0ed17ec2"
    _path_temp              =   "temp/"
    

    def __init__(self, ruta, puntero_frame, frame_to_scale, spinInicio=None, spinFinal=None, spinActual=None, mainVideo = True):
        """
        El reproductor recibe la ruta del video y consigue desplazarce por todos los puntos, asi mismo segmenta el video y lo reproduce
        ruta: Ruta del video
        puntero_frame: Elemento donde se va a instalar el reproductor
        frame_to_scale: Elemento Tk donde se instalará la Barra de progreso
        spinInicio: spinbox tkk donde se aloja el valor de inicio
        spinFinal: spinbox tkk donde se aloja el valor de final
        spinActual: spinbox tkk donde se aloja el valor actual del puntero del reproductor
        mainVideo: Permite elegir el video si es principal, (elegido del TreeView principal) o no proncipal, que sostenra los fragmentos del video
        """
        self.ruta = ruta
        self._mainVideo = mainVideo

        self._frame_rango_inicial = tk.IntVar()
        self._frame_rango_inicial.trace_add("write", self.restric_inicial)

        self._frame_rango_final = tk.IntVar()
        self._frame_rango_final.trace_add("write", self.restric_final)
        
        self._frame_actual = tk.IntVar()
        self._frame_actual.trace_add("write", self.set_video_position)
        
        self.spinInicio=spinInicio
        self.spinFinal=spinFinal
        self.spinActual=spinActual
        self.barra_de_progreso=frame_to_scale
        self.crear_widgets()

        self.spinActual.config(textvariable=self._frame_actual)
        self.spinInicio.config(textvariable=self._frame_rango_inicial)
        self.spinFinal.config(textvariable=self._frame_rango_final)

        self._frame_rango_inicial.set(0)
        self._frame_rango_final.set(1)
        
        # Visualizador openCV para procesamiento dedicado
        self.visualizador = visualizador_video2(self.ruta)

        # Iniciar el reproductor de vista previa
        self.initialize_player(puntero_frame, self.ruta)

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
            
            # Se calcula el numero de Frames a tiempo y se establece el reproductor
            numero_de_frame = self.calcular_frame_to_time(self.progress_bar.get())
            self.media_player.set_time(numero_de_frame)
        
        elif self._pausing_video:
            try:
                value = self._frame_actual.get()
                # Se calcula el numero de Frames a tiempo y se establece el reproductor
                numero_de_frame = self.calcular_frame_to_time(value)
                self.media_player.set_time(numero_de_frame)
            except:
                pass
        
        if not self._mainVideo:
            """
            Si el objeto se establece como un video No principal realizará
            un loop sobre los parametros elejidos, esto sirve fundamentalmente
            para que el usuario pueda ver los fragmentos del video y los pueda editar a gusto
            asi mismo la maquina puede recortar por IA y seleccionar automaticamente los parametro 
            de entrada y salida del video
            """
            inicio = self._frame_rango_inicial.get()
            fin = self._frame_rango_final.get()
            actual = self._frame_actual.get()

            if actual > fin:
                # Se calcula el numero de Frames a tiempo y se establece el reproductor
                numero_de_frame = self.calcular_frame_to_time(inicio)
                self.media_player.set_time(numero_de_frame)
            elif actual < inicio:
                # Se calcula el numero de Frames a tiempo y se establece el reproductor
                numero_de_frame = self.calcular_frame_to_time(inicio)
                self.media_player.set_time(numero_de_frame)
    
    def update_progres_video(self):
        
        if self.media_player and self.playing_video:
            barra = self.progress_bar
            p = self.media_player
            
            if self._length > 0:
                
                if not self._sliding:                    
                    t = max(0, self.calcular_time_to_frame(p.get_time()))
                    if t != barra.get():
                        try:
                            # Actualizar Barra de progreso y el spin_actual
                            self._frame_actual.set(t)
                        except:
                            barra.set(t)
            else:
                self._length = tamanio_ms = self.media_player.get_length()
                
                if tamanio_ms > 0:
                    # Obtener los FPS
                    self._FPS = fps = self.media_player.get_fps()
                    
                    # Obtener Frecuencia de Actualización
                    self._tick_ms = 1000//fps
                    
                    # fps totales calculados de (FPS * tamanio_total_ms/1000ms)
                    self._frames_totales = fps*tamanio_ms/1000

                    # Configurar los frames maximos
                    barra.config(to=self._frames_totales)
                    self.spinActual.config(to=int(self._frames_totales))
                    self.spinInicio.config(to=int(self._frames_totales-1))
                    self.spinFinal.config(to=int(self._frames_totales))

                    self._frame_rango_inicial.set(0)
                    self._frame_rango_final.set(int(self._frames_totales))
                    
                    

            # re-start cada fotograma
            self.tick_f = self.progress_bar.after(int(self._tick_ms), self.update_progres_video)

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

        if not self._pausing_video:
            # Se pausa el video para tener control en todo momento
            self.pause_video()
        
        
        if self._pausing_video == True:
            # Suma a el valor actual un frame
            tiempo_adelante = self.media_player.get_time() + self._tick_ms
            
            # Establecer el puntero del reproductor
            self.media_player.set_time(int(tiempo_adelante))
            
            # Establecer la barra y el spin actual 
            value_frame = int(tiempo_adelante // self._tick_ms)   
            self._frame_actual.set(value_frame)
            
    def frame_atras(self):
        if not self._pausing_video:
            # Se pausa el video para tener control en todo momento
            self.pause_video()

        if self._pausing_video == True:
            # Resta a el valor actual un frame
            tiempo_anterior = self.media_player.get_time() - self._tick_ms

            # Establecer el puntero del reproductor
            self.media_player.set_time(int(tiempo_anterior))
            
            # Establecer la barra y el spin actual
            value_frame = int(tiempo_anterior // self._tick_ms)
            self._frame_actual.set(value_frame)
            
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

    def restric_inicial(self, *args):
        try:
        
            if self._frame_actual.get() < self._frame_rango_inicial.get():
                #obtencion del valor en el inicial
                t = self._frame_rango_inicial.get()

                #Colocar la variable al punto inicial siempre y cuando el puntero actual sea menor que el impuesto
                self._frame_actual.set(t)

                #Convertir frames a tiempo
                numero_de_frame = self.calcular_frame_to_time(t)
                
                #Colocar el  video en el punto de tiempo calculado
                self.media_player.set_time(numero_de_frame)
        except:
            pass
    
    def restric_final(self, *args):
        
        try:
            #print(self._frame_actual.get())
            #print(self._frame_rango_final.get())
            if self._frame_actual.get() > self._frame_rango_final.get():
                #obtencion del valor en el final
                t = self._frame_rango_final.get()

                #Colocar la variable al punto final siempre y cuando el puntero actual sea mayor que el impuesto
                self._frame_actual.set(t)

                #Convertir frames a tiempo
                numero_de_frame = self.calcular_frame_to_time(t)
                
                #Colocar el  video en el punto de tiempo calculado
                self.media_player.set_time(numero_de_frame)
        except:
            pass
    
    def borrar_segmentos(self):
        """Permite borrar los segmentos ejecuntando un visualizador opencv"""
        try:
            estado_video_anterior = True if self.playing_video else False
            if self.playing_video:
                self.tomar_snapshot()
                self.pause_video()
            elif self._pausing_video:
                self.tomar_snapshot()

            #lanzar vizualizer en modo 1 (borrador)
            self.visualizador.motrar_roi(1)
            self.visualizador.mostrarImagen(f"{self._path_temp + self._snapshot}.png")
        except:
            print("No fue posible lanzar el segmentador")
    
    def seleccionar_personaje(self):
        """Permite seleccionar el personaje sobre el cual se vaz a realizar la inferencia"""
        try:
            estado_video_anterior = True if self.playing_video else False
            if self.playing_video:
                self.tomar_snapshot()
                self.pause_video()
            elif self._pausing_video:
                self.tomar_snapshot()
                
            
            #lanzar vizualizer en modo 2 (personaje)
            self.visualizador.motrar_roi(2)
            self.visualizador.mostrarImagen(f"{self._path_temp + self._snapshot}.png")

            # Si estaba reproduciendo al cerrar va a volver a reproducir
            if estado_video_anterior:
                self.play_video()
                


        except:
            print("No fue posible lanzar el segmentador")

    def tomar_snapshot(self):
        """Tomar foto para hacer ediciones"""
        p = self.media_player
        if p and p.get_media():
            file_name = f"{self._path_temp + self._snapshot}.png" # Solamente PNG
            if p.video_take_snapshot(0, file_name, 0, 0):
                self.showerror(file_name)

        
            
            



class VideoProgressBar(tk.Scale):
    def __init__(self, master,command, **kwargs):
        kwargs["showvalue"] = False
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
            self.after(300, self._desactivarClicked)
    
    
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

    inBox_inicio = Spinbox(frame_to_barra,from_=0, to=100)
    inBox_inicio.pack()

    inBox_Actual = Spinbox(frame_to_barra, from_ = 0, to=100)
    inBox_Actual.pack()

    inBox_fin = Spinbox(frame_to_barra, from_=1, to=100)
    inBox_fin.pack()

    

    
    #reproductor = MediaPlayer("sources/Martin Miller.mp4", display, frame_to_barra, spinInicio=inBox_inicio, spinFinal=inBox_fin, spinActual=inBox_Actual, mainVideo=False)
    reproductor = MediaPlayer("sources/feliz-2.mp4", display, frame_to_barra, spinInicio=inBox_inicio, spinFinal=inBox_fin, spinActual=inBox_Actual, mainVideo=False)
    #reproductor = MediaPlayer("sources/feliz-2.mp4", display, frame_to_barra)
    #reproductor = MediaPlayer("sources/feliz_3.mp4", display, frame_to_barra)
    #reproductor = MediaPlayer("sources/pexels.mp4", display, frame_to_barra)
    
    #opencv = visualizador_video2()
    boton_borrador = Button(frame_to_barra, text="Borrador", command=reproductor.tomar_snapshot)
    boton_borrador.pack(side='right')

    frame_root.mainloop()

    


