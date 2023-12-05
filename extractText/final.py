#librerias
from tkinter import *
from tkinter import ttk

#from funciones.reproductor import iniciar_video, visualizar
from funciones.reproductor import Visualizador_Video

#----------------------------------------------------
#               Hiperparametros
#----------------------------------------------------

RUTA = "sources/emocionesVideo1.mp4"
#----------------------------------------------------

    
#Funcion Global para seleccionar el objeto y ponerlo en 
# la vista general De Video
def item_selected(event):
    """
    Evento invocado cuando el contenido de una carpeta es abierto.
    """
    item_seleccionado = arbol.selection()
    item = arbol.item(item_seleccionado)
    
    #Extraer la ruta del archivo
    ruta = item["values"][0]
    
    global RUTA
    RUTA = ruta
    #Iniciacion del video
    Visualizador_General.iniciar_video(ruta)
    #iniciar_video(ruta, lblVideo)

    


#Ventana principal
frame_root = Tk()

#Configuraciones de la ventana
frame_root.title("Sistema de Mineria TecnoBot")
frame_root.geometry("1250x1000")
frame_root.columnconfigure(0, weight=1)
frame_root.columnconfigure(1, weight=3)
frame_root.columnconfigure(2, weight=1)

#Crecion de 4 raices
tools_bar = Frame(frame_root)
tools_bar.grid(row=0, column = 0, sticky=S+N+E+W, columnspan=3)
tools_bar.config(bg="blue", height=50)


#Arbol1
Tree_in = Frame(frame_root)
Tree_in.grid(row=1, column = 0)
Tree_in.config(bg="lightblue", width=250, height=900)  

#treeview 
#from funciones.seleccionar_directorios import item_selected
arbol = ttk.Treeview(Tree_in)
arbol.bind("<<TreeviewSelect>>", item_selected)
arbol.pack(expand=True, fill='both')




#Visualizador
cuadro_reproductor = Frame(frame_root)
cuadro_reproductor.grid(row=1, column = 1)
cuadro_reproductor.config(bg="green", width=750, height=900)  
cuadro_reproductor['borderwidth'] = 5
cuadro_reproductor['relief'] = 'sunken'

#Arbol de salida
Tree_out = Frame(frame_root)
Tree_out.grid(row=1, column = 2)
Tree_out.config(bg="red", width=250, height=900)  



#----------------------------------------------------
#             botones barra herramientas
#----------------------------------------------------
from funciones.seleccionar_directorios import *

button_dir_in  = Button(tools_bar, text = "Directorio Entrada", command = lambda: abrir_directorio(arbol))
button_dir_in.grid(row=0, column=0, padx = 10, pady = 10)
button_dir_out = Button(tools_bar, text = "Directorio Salida", command = lambda: abrir_directorio(arbol))
button_dir_out.grid(row=0, column=1, padx = 10, pady = 10)


#----------------------------------------------------
#                   Reproductor
#----------------------------------------------------
#
#           1. Reproductor : Visualizador
#
#----------------------------------------------------
cuadro_visualizador = Frame(cuadro_reproductor)
cuadro_visualizador.grid(row=0, column = 0, sticky="nsew")
cuadro_visualizador.config(bg="purple", height=480) 

#----------------------------------------------------
#           1.2. Visualizador : Video Principal
#----------------------------------------------------
lblVideoPrincipal = Label(cuadro_visualizador)
lblVideoPrincipal.grid(row=0, column=0, columnspan=2, rowspan=3, sticky='nsew')

# Instanciamiento Objeto visualizador
Visualizador_General = Visualizador_Video(lblVideoPrincipal)

#----------------------------------------------------
#           1.2. Visualizador : Roi_Personaje
#----------------------------------------------------
roi_personaje = Frame(cuadro_visualizador)
roi_personaje.grid(row=0, column=2)
roi_personaje.config(bg="yellow", width=250, height=125) 


#----------------------------------------------------
#           1.3. Visualizador : Roi_Text
#----------------------------------------------------
roi_text = Frame(cuadro_visualizador)
roi_text.grid(row=1, column=2)
roi_text.config(bg="black", width=250, height=125) 


#----------------------------------------------------
#   1.4. Visualizador : Visualizer Puntos Corporales
#----------------------------------------------------
roi_body_puntos = Frame(cuadro_visualizador)
roi_body_puntos.grid(row=3, column=2)
roi_body_puntos.config(bg="blue", width=250, height=125) 

#----------------------------------------------------
#                   Reproductor
#----------------------------------------------------
#
#           2. Reproductor : CONTROLES
#
#----------------------------------------------------
cuadro_controles = Frame(cuadro_reproductor)
cuadro_controles.grid(row=1, column = 0, sticky='nsew')
cuadro_controles.config(bg="white", width=750, height=250)



lanzador = Button(cuadro_controles, text="ROI", command= Visualizador_General.motrar_roi)
lanzador.pack()
Cerrador = Button(cuadro_controles, text="X", command=Visualizador_General.quitar_ventana)
Cerrador.pack()


if __name__ == "__main__":
    
    frame_root.mainloop()