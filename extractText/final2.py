#librerias
from struct import pack
from tkinter import *
from tkinter import ttk

import tkinter
from turtle import left, width, window_width
from idlelib.tooltip import Hovertip #para la informacion de los botones
from ttkwidgets import CheckboxTreeview
#from extractText.funciones import reproductor
#from torch import fill 

from funciones.reproductor import MediaPlayer

reproductor_video = None

#Funcion Global para seleccionar el objeto y ponerlo en 
# la vista general De Video
def item_selected(event):
    """
    Evento invocado cuando el contenido de una carpeta es abierto.
    """
    item_seleccionado = arbol.selection()
    item = arbol.item(item_seleccionado)
    print(item)
    
    #Extraer la ruta del archivo y si encuentra espacios unirlos
    ruta = ""
    for element in item["values"]:
        ruta += element + " "

    
    #Iniciacion del video
    global reproductor_video

    # Cerrar el video para que no se abra en multiples ventanas
    if reproductor_video is not None:
        reproductor_video.ClosePlayer()
    
    reproductor_video = MediaPlayer(ruta, frame_visualizer, frame_botones_procesar)
    reproductor_video.update_progres_video()
    


#Ventana principal
frame_root = Tk()

#Configuraciones de la ventana
frame_root.title("Sistema de Mineria TecnoBot")
frame_root.geometry("1080x720")
frame_root.config(bg='white')

#Crecion de 4 raices

#----------------------------------------------------
#                 Barra herramientas
#----------------------------------------------------
frame_tools_bar = Frame(frame_root)
frame_tools_bar.pack( fill='x', side='top')
frame_tools_bar.config(height=50)

#----------------------------------------------------
#                Barra herramientas
#----------------------------------------------------
#
#                 1. import/export 
#
#----------------------------------------------------
grupo_import_export = Frame(frame_tools_bar)
grupo_import_export.pack( anchor='center', side='left', padx=20)
#----------------------------------------------------
#                Barra herramientas
#----------------------------------------------------
#
#            1.1 import/export: Botones
#
#----------------------------------------------------
from funciones.seleccionar_directorios import *

img_boton = tkinter.PhotoImage(file="extractText/app_sources/icons/openFolder.png")
button_dir_in  = Button(grupo_import_export, image=img_boton,  command = lambda: abrir_directorio(arbol))
button_dir_in.config(width=35, height=35)
button_dir_in.pack(padx=5, side='left')
Hovertip(button_dir_in, text="Seleccionar el directorio fuente de videos", hover_delay=500)

img_boton2 = tkinter.PhotoImage(file="extractText/app_sources/icons/outPutFolder.png")
button_dir_out  = Button(grupo_import_export, image=img_boton2, text = "Directorio Entrada")
button_dir_out.config(width=35, height=35)
button_dir_out.pack(padx=5, side='right')
Hovertip(button_dir_out, text="Seleccionar el directorio de salida para los videos", hover_delay=500)
#----------------------------------------------------
#
#                 2. Tools Bar 
#
#----------------------------------------------------
grupo_tools_bar = Frame(frame_tools_bar)
grupo_tools_bar.pack( anchor='center', side='left', padx=20)
#----------------------------------------------------
#                Barra herramientas
#----------------------------------------------------
#
#            2.1 Tools Bar: eraser
#
#----------------------------------------------------
img_boton3 = tkinter.PhotoImage(file="extractText/app_sources/icons/eraser.png")
button_eraser = Button(grupo_tools_bar, image=img_boton3, text = "Directorio Entrada")
button_eraser.config(width=35, height=35)
button_eraser.pack(padx=5, side='left')
Hovertip(button_eraser, text="Elimina los segmentos de texto\nque no quiere que sean reconocidos dentro del video", hover_delay=500)

img_boton4 = tkinter.PhotoImage(file="extractText/app_sources/icons/SelectUser.png")
button_selec_user = Button(grupo_tools_bar, image=img_boton4, text = "Directorio Entrada")
button_selec_user.config(width=35, height=35)
button_selec_user.pack(padx=5, side='left')
Hovertip(button_selec_user, text="Selecciona el segmento de la persona que quiere reconocer", hover_delay=500)

img_boton5 = tkinter.PhotoImage(file="extractText/app_sources/icons/pointer.png")
button_pointer = Button(grupo_tools_bar, image=img_boton5, text = "Directorio Entrada")
button_pointer.config(width=35, height=35)
button_pointer.pack(padx=5, side='right')
Hovertip(button_selec_user, text="Usar el puntero", hover_delay=500)



#----------------------------------------------------
#                 Arbol de Entrada
#----------------------------------------------------
frame_Tree_in = Frame(frame_root)
frame_Tree_in.pack(side="left", anchor='n')
frame_Tree_in.config(width=200, height=480)

#from funciones.seleccionar_directorios import item_selected
arbol = CheckboxTreeview(frame_Tree_in)
#arbol = ttk.Treeview(frame_Tree_in)
arbol.bind("<<TreeviewSelect>>", item_selected)
arbol.pack(anchor='n',fill='both')



#Visualizador
frame_visualizer = Frame(frame_root)
frame_visualizer.pack(side="left", anchor='n')
frame_visualizer.config(bg="darkblue", width=680, height=480)


#Arbol Salida
frame_Tree_out = Frame(frame_root)
frame_Tree_out.pack(side="left", anchor='n', fill='y')
frame_Tree_out.config(bg="green", width=200)

#Frame Fragmentos
frame_Fragmentos = Frame(frame_root)
frame_Fragmentos.config(bg="purple")
frame_Fragmentos.place(x=0, y = 531, width=200, height=200)

#----------------------------------------------------
#               Herramientas de video
#----------------------------------------------------
#
#            1 Frame Control de Video
#
#----------------------------------------------------
frame_herrsamientas_de_video = Frame(frame_root)
frame_herrsamientas_de_video.place(x=200, y=531, width=680, height=200)
frame_herrsamientas_de_video.config(bg="red", width= 1200, height=190)
#----------------------------------------------------
#               Herramientas de video
#----------------------------------------------------
#----------------------------------------------------
#
#            1.1 Botones procesar
#
#----------------------------------------------------
frame_botones_procesar = Frame(frame_herrsamientas_de_video)
frame_botones_procesar.config(bg="blue")
frame_botones_procesar.pack(fill='x', anchor='center')


contenedorBotones = Frame(frame_botones_procesar)
contenedorBotones.config(bg="white")
contenedorBotones.pack(anchor='center', expand=True)

# Boton Proceso con texto
button_procesar_con_texto = Button(contenedorBotones, text="Procesar con texto")
button_procesar_con_texto.pack(padx=10, side='left', anchor='center', expand=False)

# Boton Proceso con texto
button_procesar_con_voz = Button(contenedorBotones, text="Procesar con voz")
button_procesar_con_voz.pack(padx=10, side='left', anchor='center', expand=False)

#----------------------------------------------------
#               Herramientas de video
#----------------------------------------------------
#----------------------------------------------------
#
#            1.2 Control de video
#
#----------------------------------------------------
frame_control_de_video = Frame(frame_herrsamientas_de_video)
frame_control_de_video.config(bg="white", height=180)
frame_control_de_video.pack(fill='x', anchor= 's')

#----------------------------------------------------
#
#            1.2.1 Control de posicion
#
#----------------------------------------------------
frame_control_de_posicion = Frame(frame_control_de_video)
frame_control_de_posicion.config(bg="white")
frame_control_de_posicion.pack(fill='x', anchor= 'n', padx=20)

#------------------------------------|
#     1.2.2  Frame insert inicio
# -----------------------------------|
frame_inicio = Frame(frame_control_de_posicion)
frame_inicio.config(bg="white", width=104)
frame_inicio.pack(side='left')

label_inicio = Label(frame_inicio, text="Fotograma Inicio",bg="white").pack()
inBox_inicio = Entry(frame_inicio).pack()

#------------------------------------|
#      1.2.3    Frame Actual
# -----------------------------------|
frame_actual = Frame(frame_control_de_posicion)
frame_actual.config(bg="white", width=104)
frame_actual.pack(side='left')

label_actual = Label(frame_actual, text="Fotograma Actual", bg="white").pack()
inBox_Actual = Entry(frame_actual, state='disabled').pack()

#------------------------------------|
#    1.2.4   Frame insert Fin
# -----------------------------------|
frame_fin = Frame(frame_control_de_posicion)
frame_fin.config(bg="white", width=104)
frame_fin.pack(side='left')

label_fin = Label(frame_fin, text="Fotograma Fin",bg="white").pack()
inBox_fin = Entry(frame_fin).pack()

#------------------------------------|
#       Boton Guardar Video
# -----------------------------------|
boton_guardar_video = Button(frame_control_de_posicion, text="Guardar")
boton_guardar_video.pack(side='left', padx=20, expand=True)

#----------------------------------------------------
#
#            1.3. Visores Post-Procesados
#
#----------------------------------------------------
frame_visores_Post_Procesados = Frame(frame_control_de_video)
frame_visores_Post_Procesados.config(bg="white")
frame_visores_Post_Procesados.pack(fill='x', anchor= 'n', padx=20, expand=1)

#------------------------------------|
#    1.3.1   visor mediapipe
# -----------------------------------|
frame_visor_mediaPipe = Frame(frame_visores_Post_Procesados)
frame_visor_mediaPipe.config(bg="grey", width=178, height=123)
frame_visor_mediaPipe.pack(anchor= 'n', padx=10, side='left')

#------------------------------------|
#    1.3.2   visor preview
# -----------------------------------|
frame_visor_preview = Frame(frame_visores_Post_Procesados)
frame_visor_preview.config(bg="grey", width=178, height=123)
frame_visor_preview.pack(anchor= 'n', padx=10, side='left')

#------------------------------------|

#    1.3.3   visor propiedades

# -----------------------------------|
frame_visor_propiedades = Frame(frame_visores_Post_Procesados)
frame_visor_propiedades.config(bg="white", width=300, height=123)
frame_visor_propiedades.pack(anchor= 'center', padx=1, side='left')

#------------------------------------|
#    1.3.3.1   campo nombre del Gesto
# -----------------------------------|
frame_campo_nombre_gesto = Frame(frame_visor_propiedades)
frame_campo_nombre_gesto.config(bg="white", width=389, height=16)
frame_campo_nombre_gesto.pack(anchor = 'center', padx=10, pady=5, expand=1)

etiqueta_nombre_gesto = Label(frame_campo_nombre_gesto, text="Nombre de\ngesto", bg="white").pack(padx=5, side='left')
inbox_nombre_gesto = Entry(frame_campo_nombre_gesto, state='disabled').pack(side='left')

#------------------------------------|
#    1.3.3.2   campo carpeta del Gesto
# -----------------------------------|
frame_campo_nombre_carpeta = Frame(frame_visor_propiedades)
frame_campo_nombre_carpeta.config(bg="white", width=389, height=16)
frame_campo_nombre_carpeta.pack(anchor = 'center', padx=10, pady=5, expand=1)

etiqueta_nombre_carpeta = Label(frame_campo_nombre_carpeta, text="Nombre de\ncarpeta", bg="white").pack(padx=5, side='left')
inbox_nombre_carpeta = Entry(frame_campo_nombre_carpeta, state='disabled').pack(side='left')

#------------------------------------|
#    1.3.3.3  campo nombre del Gesto
# -----------------------------------|
frame_campo_nombre_archivo = Frame(frame_visor_propiedades)
frame_campo_nombre_archivo.config(bg="white", width=389, height=16)
frame_campo_nombre_archivo.pack(anchor = 'center', padx=10, pady=5, expand=1)

etiqueta_nombre_archivo = Label(frame_campo_nombre_archivo, text="Nombre de\narchivo", bg="white").pack(padx=5, side='left')
inbox_nombre_archivo = Entry(frame_campo_nombre_archivo, state='disabled').pack(side='left')


if __name__ == "__main__":
    
    frame_root.mainloop()