#librerias
from tkinter import *
from tkinter import ttk

from PIL import Image
from PIL import ImageTk
import cv2
import numpy as np
import imutils
from tkinter import filedialog

def iniciar():
    global cap
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    visualizar()

def visualizar():

    global cap
    
    #cap = cv2.VideoCapture("sources/feliz-2.mp4")
    
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=300)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualizar)
        else:
            lblVideo.image = ""
            cap.release()

def finalizar():
    global cap
    cap.release()

def elegir_visualizar_video():
    global cap
    if cap is not None:
        lblVideo.image = ""
        cap.release()
        cap = None
    video_path = filedialog.askopenfilename(filetypes = [
        ("all video format", ".mp4"),
        ("all video format", ".avi")])
    if len(video_path) > 0:
        #lblInfoVideoPath.configure(text=video_path)
        cap = cv2.VideoCapture(video_path)
        visualizar()
    else:
        #lblInfoVideoPath.configure(text="Aún no se ha seleccionado un video")
        pass


cap = None
#Correr la ventana Principal
#Ventana principal
frame_root = Tk()

#Configuraciones de la ventana
frame_root.title("Sistema de Mineria TecnoBot")
frame_root.geometry("1250x1000")

lblVideo = Label(frame_root)
lblVideo.grid(column=0, row=0)
lblVideo.pack()


elegir_visualizar_video()
frame_root.mainloop()