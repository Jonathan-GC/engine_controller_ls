#librerias
from tkinter import *
from tkinter import ttk


#Funcion Global para seleccionar el objeto y ponerlo en la vista general
#De Video
def item_selected(event):
    """
    Evento invocado cuando el contenido de una carpeta es abierto.
    """
    item = arbol.selection()
    #PunteroArbol.item(selected_item)
    #iid = PunteroArbol.selection()[0]
    #self.load_subitems(iid)
    #print(iid)
    print(item)


#Ventana principal
frame_root = Tk()

#Configuraciones de la ventana
frame_root.title("Sistema de Mineria TecnoBot")
frame_root.geometry("1400x1000")

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
Tree_in = Frame(frame_root)
Tree_in.grid(row=1, column = 1)
Tree_in.config(bg="gray", width=900, height=900)  

#Arbol de salida
Tree_in = Frame(frame_root)
Tree_in.grid(row=1, column = 2)
Tree_in.config(bg="red", width=250, height=900)  



#----------------------------------------------------
#             botones barra herramientas
#----------------------------------------------------
from funciones.seleccionar_directorios import *

button_dir_in  = Button(tools_bar, text = "Directorio Entrada", command = lambda: abrir_directorio(arbol))
button_dir_in.grid(row=0, column=0, padx = 10, pady = 10)
button_dir_out = Button(tools_bar, text = "Directorio Salida", command = lambda: abrir_directorio(arbol))
button_dir_out.grid(row=0, column=1, padx = 10, pady = 10)





#Correr la ventana Principal
frame_root.mainloop()
