#librerias
from tkinter import *
from tkinter import ttk

from funciones.reproductor import iniciar_video, visualizar


#----------------------------------------------------
#               Hiperparametros
#----------------------------------------------------


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
    
    #Iniciacion del video
    iniciar_video(ruta, lblVideo)

    


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
arbol.pack()




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
#----------------------------------------------------
cuadro_visualizador = Frame(cuadro_reproductor)
cuadro_visualizador.grid(row=0, column = 0)
cuadro_visualizador.config(bg="purple", width=520, height=580) 

lblVideo = Label(cuadro_visualizador)
lblVideo.pack()



if __name__ == "__main__":

    #visualizar(lblVideo)
    frame_root.mainloop()