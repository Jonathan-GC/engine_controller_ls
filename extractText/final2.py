#librerias
from tkinter import *
from tkinter import ttk
import tkinter
from turtle import window_width


#Ventana principal
frame_root = Tk()

#Configuraciones de la ventana
frame_root.title("Sistema de Mineria TecnoBot")
frame_root.geometry("1080x720")
"""
frame_root.columnconfigure(0, weight=1)
frame_root.columnconfigure(1, weight=3)
frame_root.columnconfigure(2, weight=1)
frame_root.rowconfigure(0, weight=1, minsize=20)
frame_root.rowconfigure(1, weight=1)
frame_root.rowconfigure(2, weight=1)
frame_root.rowconfigure(3, weight=1)
"""
#Crecion de 4 raices

#Barra de herramientas
frame_tools_bar = Frame(frame_root)
frame_tools_bar.pack( fill='x', side='top')
frame_tools_bar.config(bg="blue", height=50)

#Arbol entrada
frame_Tree_in = Frame(frame_root)
frame_Tree_in.pack(side="left", anchor='n')
frame_Tree_in.config(bg="lightblue", width=200, height=480)


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


# Herramientas de video
frame_herrsamientas_de_video = Frame(frame_root)
frame_herrsamientas_de_video.place(x=200, y=531, width=680, height=200)
frame_herrsamientas_de_video.config(bg="red", width= 1200, height=190)
if __name__ == "__main__":
    
    frame_root.mainloop()