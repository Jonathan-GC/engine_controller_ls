
import cv2
import numpy as np

image = None
miArray = None

start = False
estado  = 0
estado1 = 0
p1, p2 = None, None
p3, p4 = None, None
list_puntos_difuminar = []
'''
def on_trackbar(value):
    pass

def on_mouse(event, x, y, flags, param):

    global start
    pt = (x, y)

    if event == cv2.EVENT_LBUTTONDOWN:
        start = True
    elif event == cv2.EVENT_LBUTTONUP:
        start = False
    elif start and event == cv2.EVENT_MOUSEMOVE:
        ventana = 'Drawing'
        grosor = cv2.getTrackbarPos('Grosor', ventana)

        
        
        cv2.circle(param, pt, grosor, (0, 0, 0), -1)
'''  
  

def on_mouse(event, x, y, flags, param):
    global estado, p3, p4, miArray
    if event == cv2.EVENT_LBUTTONDBLCLK:
        if estado == 0:
            p3 = (x,y)
            estado = 1
        elif estado == 1:
            p4 = (x,y)
            estado = 0
            miArray=cv2.rectangle(param, p3, p4, (0, 100, 0), -1)
        
            


if __name__ == "__main__":
    
    title = 'Drawing'
    image = cv2.imread("sources/temp/blob.png")
    
    cv2.namedWindow(title)
    #cv2.createTrackbar('Grosor', title, 5, 50, on_trackbar) 
    cv2.setMouseCallback(title, on_mouse, image)

    while(1):
        cv2.imshow(title, image)
        if cv2.waitKey(20) & 0xFF == 27:
            break
        
    cv2.destroyAllWindows()
    print((miArray==image).all())
    print(miArray == image)
#joder = cv2.imread("sources/temp/Captura1.png")
#cv2.imshow("JJJ", joder)
#cv2.waitKey()
#cv2.destroyAllWindows()


"""
import threading
import time

def hilo1():
    while True:
        print("Hilo 1 trabajando")
        time.sleep(1)

def hilo2():
    while True:
        print("Hilo 2 trabajando")
        time.sleep(1)

# Crear dos hilos
thread1 = threading.Thread(target=hilo1)
thread2 = threading.Thread(target=hilo2)

# Iniciar los hilos
thread1.start()
thread2.start()

# Esperar a que ambos hilos terminen (esto no se ejecutará ya que los hilos son infinitos)
thread1.join()
thread2.join()
"""
"""
from multiprocessing import Process
import os
import time


contador = 1

def funcion1():
    global contador
    while 1:
        print("Hilo 1 trabajando")
        contador+=1
        time.sleep(1)
        if contador > 15:
            break

        
def funcion2():
    global contador
    
    while 1:
        print("Hilo 2 trabajando")
        contador *=3
        print("Contador=",contador)
        time.sleep(1)
        if contador > 400:
            break


if __name__ == '__main__':
    p = Process(target=funcion1, args=())
    q = Process(target=funcion2, args=())
    
    p.start()
    q.start()
    
    
    p.join()
    q.join()



    print("Termino Todo")
    print("contador= ", contador)

"""
