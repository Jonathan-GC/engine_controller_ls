from tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
from tkinter import filedialog
import numpy as np
"""
    def elegir_video():
        # Especificar los tipos de archivos, para elegir solo a las imágenes
        path_video = filedialog.askopenfilename(filetypes = [
        ("video", ".mp4"),
        ("image", ".avi")
        ])

        if len(path_video) > 0:
            global video
            # Leer el video de entrada 
            cap = cv2.VideoCapture(path_video)
            if cap.isOpened():
                _, image = cap.read()
                image= imutils.resize(image, height=380)
                # Para visualizar la imagen de entrada en la GUI
                imageToShow= imutils.resize(image, width=500)
                imageToShow = cv2.cvtColor(imageToShow, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(imageToShow )
                img = ImageTk.PhotoImage(image=im)
                lblInputImage.configure(image=img)
                lblInputImage.image = img
                # Label IMAGEN DE ENTRADA
                lblInfo1 = Label(root, text="IMAGEN DE ENTRADA:")
                lblInfo1.grid(column=0, row=1, padx=5, pady=5)
                # Al momento que leemos la imagen de entrada, vaciamos
                # la iamgen de salida y se limpia la selección de los
                # radiobutton
                lblOutputImage.image = ""
                selected.set(0)
                


    def deteccion_color():
        global image
        if selected.get() == 1:
            # Rojo
            rangoBajo1 = np.array([0, 140, 90], np.uint8)
            rangoAlto1 = np.array([8, 255, 255], np.uint8)
            rangoBajo2 = np.array([160, 140, 90], np.uint8)
            rangoAlto2 = np.array([180, 255, 255], np.uint8)
        if selected.get() == 2:
            # Amarillo
            rangoBajo = np.array([10, 98, 0], np.uint8)
            rangoAlto = np.array([25, 255, 255], np.uint8)
        if selected.get() == 3:
            # Azul celeste
            rangoBajo = np.array([88, 104, 121], np.uint8)
            rangoAlto = np.array([99, 255, 243], np.uint8)
            
        imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        imageGray = cv2.cvtColor(imageGray, cv2.COLOR_GRAY2BGR)
        imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        if selected.get() == 1:
            # Detectamos el color rojo
            maskRojo1 = cv2.inRange(imageHSV, rangoBajo1, rangoAlto1)
            maskRojo2 = cv2.inRange(imageHSV, rangoBajo2, rangoAlto2)
            mask = cv2.add(maskRojo1, maskRojo2)
        else:
            # Detección para el color Amarillo y Azul celeste
            mask = cv2.inRange(imageHSV, rangoBajo, rangoAlto)
        mask = cv2.medianBlur(mask, 7)
        colorDetected = cv2.bitwise_and(image, image, mask=mask)
        # Fondo en grises
        invMask = cv2.bitwise_not(mask)
        bgGray = cv2.bitwise_and(imageGray, imageGray, mask=invMask)
        # Sumamos bgGray y colorDetected
        finalImage = cv2.add(bgGray, colorDetected)
        imageToShowOutput = cv2.cvtColor(finalImage, cv2.COLOR_BGR2RGB)
        # Para visualizar la imagen en lblOutputImage en la GUI
        im = Image.fromarray(imageToShowOutput)
        img = ImageTk.PhotoImage(image=im)
        lblOutputImage.configure(image=img)
        lblOutputImage.image = img
        # Label IMAGEN DE SALIDA
        lblInfo3 = Label(root, text="IMAGEN DE SALIDA:", font="bold")
        lblInfo3.grid(column=1, row=0, padx=5, pady=5)


    # Creamos la ventana principal
    root = Tk()

    # Label donde se presentará la imagen de entrada
    lblInputImage = Label(root)
    lblInputImage.grid(column=0, row=2)

    # Label donde se presentará la imagen de salida
    lblOutputImage = Label(root)
    lblOutputImage.grid(column=1, row=1, rowspan=6)

    # Label ¿Qué color te gustaría resaltar?
    lblInfo2 = Label(root, text="¿Qué color te gustaría resaltar?", width=25)
    lblInfo2.grid(column=0, row=3, padx=5, pady=5)

    # Creamos los radio buttons y la ubicación que estos ocuparán
    #selected = IntVar()
    #rad1 = Radiobutton(root, text='Rojo', width=25,value=1, variable=selected, command= deteccion_color)
    #rad2 = Radiobutton(root, text='Amarillo',width=25, value=2, variable=selected, command= deteccion_color)
    #rad3 = Radiobutton(root, text='Azul celeste',width=25, value=3, variable=selected, command= deteccion_color)
    #rad1.grid(column=0, row=4)
    #rad2.grid(column=0, row=5)
    #rad3.grid(column=0, row=6)

    # Creamos el botón para elegir la imagen de entrada
    btn = Button(root, text="Elegir Video", width=25, command=elegir_video)
    btn.grid(column=0, row=0, padx=5, pady=5)
    root.mainloop()
"""


def iniciar():
    global cap
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    visualizar()

def visualizar():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=480)
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
        lblInfoVideoPath.configure(text=video_path)
        cap = cv2.VideoCapture(video_path)
        visualizar()
    else:
        lblInfoVideoPath.configure(text="Aún no se ha seleccionado un video")


cap = None
root = Tk()

visualizador = Frame(root)
visualizador.grid(column=0, row=0, rowspan=2)

botones_de_control = Frame(root)
botones_de_control.grid(column=0, row=2, rowspan=2)

btnVisualizar = Button(visualizador, text="Elegir y visualizar video", command=elegir_visualizar_video)
btnVisualizar.grid(column=0, row=0, padx=5, pady=5, columnspan=2)

lblInfo1 = Label(visualizador, text="Video de entrada:")
lblInfo1.grid(column=0, row=1)
lblInfoVideoPath = Label(visualizador, text="Aún no se ha seleccionado un video")
lblInfoVideoPath.grid(column=1, row=1)
lblVideo = Label(visualizador)
lblVideo.grid(column=0, row=2, columnspan=2)

btn_pausar = Button(botones_de_control, text="pausar")
btn_pausar.grid(column=0, row=0, padx=5, pady=5, columnspan=1)

btn_detener = Button(botones_de_control, text="detener")
btn_detener.grid(column=1, row=0, padx=5, pady=5, columnspan=2)


root.mainloop()