
from PIL import Image
from PIL import ImageTk
import cv2
import numpy as np
import imutils


class Visualizador_Video:

    # Esta variable permite almacenar la ultima tarea 
    # y terminar los procesos he hilos de ejecución
    last_task = None
    #Roi Definido por dos puntos
    p1, p2 = None, None # Roi Persona
    p3, p4 = None, None # Roi Texto
    
    estado = 0
    estado1 = 0
    dimensiones = (480, 640)
    imagen_general = np.zeros(dimensiones, np.uint8)

    mostrar_ventana = False
    

    def __init__(self, etiquetaVideo, etiquetaRoiPersonaje, etiquetaRoiText, etiquetaBodyPoints ) -> None:
        self.etiquetaVideo = etiquetaVideo
        self.etiquetaRoiPersonaje = etiquetaRoiPersonaje
        self.etiquetaRoiText = etiquetaRoiText
        self.etiquetaBodyPoints = etiquetaBodyPoints

        #self.motrar_roi()
        


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
                    self.imagen_general=imagen

                    if self.mostrar_ventana:
                        # si el roi esta seleccionado dibujelo
                        if self.estado  > 1 and self.estado < 3:
                            cv2.rectangle(self.imagen_general, self.p1, self.p2, (255, 0, 0), 5)
                            imagen_persona = self.imagen_general[int(self.p1[1]) : int(self.p2[1]), int(self.p1[0]) : int(self.p2[0])]
                            imagen_persona = imutils.resize(imagen_persona, height=250)
                            imagen_persona = cv2.cvtColor(imagen_persona, cv2.COLOR_BGR2RGB)
                            im_persona = Image.fromarray(imagen_persona)
                            img_persona = ImageTk.PhotoImage(image=im_persona)
                            self.etiquetaRoiPersonaje.configure(image=img_persona)
                            self.etiquetaRoiPersonaje.image = img_persona
                        if self.estado  > 2 and self.estado < 5:
                            cv2.rectangle(self.imagen_general, self.p3, self.p4, (0, 255, 0), 5)
                            imagen_texto = self.imagen_general[int(self.p3[1]) : int(self.p4[1]), int(self.p3[0]) : int(self.p4[0])]
                            imagen_texto = imutils.resize(imagen_texto, height=250)
                            imagen_texto = cv2.cvtColor(imagen_texto, cv2.COLOR_BGR2RGB)
                            im_texto = Image.fromarray(imagen_texto)
                            img_texto = ImageTk.PhotoImage(image=im_texto)
                            self.etiquetaRoiText.configure(image=img_texto)
                            self.etiquetaRoiText.image = img_texto
                        cv2.imshow("Imagen", self.imagen_general)


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

    #Llamada a eventos del mouse
    def seleccionar_area(self, event, x, y, flags, param):
        # Ejemplos de acciones con algunos eventos del mouse
               
        if event == cv2.EVENT_LBUTTONDBLCLK:
            #cv2.putText(self.imagen_general, "Seleccionar", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2, cv2.LINE_AA) 
            
            if  flags == cv2.EVENT_FLAG_ALTKEY and  self.estado1 == 0:
                print("JOder1")
                self.p3 = (x, y)
                self.estado1 = 1
            elif flags == cv2.EVENT_FLAG_ALTKEY and self.estado1 == 1:
                print("JOder2")
                self.p4 = (x, y)
                self.estado1 = 2
            
            #Seleccionar primer punto
            elif self.estado == 0:
                self.p1 = (x, y)
                self.estado = 1
            #selecionar segundo punto
            elif self.estado == 1:
                self.p2 = (x, y)
                self.estado = 2
            


        if event == cv2.EVENT_RBUTTONUP:
            self.p1, self.p2 = None, None
            self.estado = 0
        elif flags == cv2.EVENT_FLAG_ALTKEY and event == cv2.EVENT_RBUTTONUP:
            self.p3, self.p4 = None, None
            

    def motrar_roi(self):
        
        #Activar la ventana de opencv
        self.mostrar_ventana = True
        cv2.namedWindow('Imagen')  
        #introducir los callBack del mouse
        cv2.setMouseCallback("Imagen", self.seleccionar_area)
        
        
        
        

    def quitar_ventana(self):
        self.mostrar_ventana = False
    
    


        

        

class visualizadorOpenCV:
    def __init__(self, ruta) -> None:
        self.ruta = ruta
        self.iniciar_video()

    def iniciar_video(self):
        cap = cv2.VideoCapture(self.ruta)
        ret, frame = cap.read()
        cv2.imshow("video", frame)
        cv2.waitKey()
        cv2.destroyAllWindows()



if __name__ == "__main__":
    visualizador = visualizadorOpenCV("sources/feliz_3.mp4")

