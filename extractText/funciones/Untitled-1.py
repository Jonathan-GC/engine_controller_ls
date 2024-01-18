
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

"""from multiprocessing import Process, Pipe
import os
import time


contador = 0

def funcion1(tubo, contador):
    while 1:
        print("Hilo 1 trabajando")
        contador+=1
        time.sleep(0.2)
        tubo.send(contador)
        if contador > 15:
            break
    tubo.close()

        
def funcion2(tubo):
    contador = 0
    while 1:
        print("Hilo 2 trabajando")
        print("Contador=",contador*2)
        time.sleep(1)
        if contador >15:
            break
        contador = tubo.recv()
        
    tubo.close()


if __name__ == '__main__':
    
    tubo_praceso1, tubo_proceso2 = Pipe()
    p = Process(target=funcion1, args=(tubo_praceso1, contador,))
    q = Process(target=funcion2, args=(tubo_proceso2,))
    
    p.start()
    q.start()
    
    #print("contador al FINAL= ", tubo_proceso2.recv())
    p.join()
    q.join()



    print("Termino Todo")
  """

"""
from multiprocessing import Process, Lock

def f(l, i):
    l.acquire()
    try:
        print('hello world', i)
    finally:
        l.release()

if __name__ == '__main__':
    lock = Lock()

    for num in range(50):
        Process(target=f, args=(lock, num)).start()
"""


"""from multiprocessing import Process, Value, Array

def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

if __name__ == '__main__':
    num = Value('d', 0.0)
    arr = Array('i', range(10))

    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])
"""
'''
import multiprocessing

def worker(num):
    """worker function"""
    print('Worker', num)


if __name__ == '__main__':
    #jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        #jobs.append(p)
        p.start()
    #print(jobs)
'''
from multiprocessing import Process, log_to_stderr, get_logger
import time
from tkinter import Tk
from tkinter import ttk
import logging
import sys
import vlc


def item_selected(event):
    print("Joder")
    my_objeto = objeto()
    button_eraser.config(command=lambda:my_objeto.lanzador(2))
    button_marco.config(command=lambda:my_objeto.lanzador(1))
    my_objeto.start_player()

class objeto:

    def __init__(self) -> None:
        #self.start_player()
        pass
    
    def start_player(self):
        self.vlc_instance = vlc.Instance()
        

    def funcion1(self):
        contador = 0
        while 1:
            contador += 1
            print("Func1: ", contador, self.palabra)
            time.sleep(0.1)
            
            if contador > 80:
                break
        
        q = Process(target=self.funcion3)
        q.start()
        #q.join()
    
    def funcion2(self):
        contador = 0
        while 1:
            contador += 2
            print("Func2: ", contador)
            time.sleep(0.2)
            if contador > 120:
                break
    
    def funcion3(self):
        contador = 0
        while 1:
            contador += 2
            print("Func3: ", contador)
            time.sleep(0.02)
            if contador > 200:
                break
    
    def lanzador(self,mode):
        log_to_stderr(logging.DEBUG)
        logger = get_logger()
        logger.setLevel(logging.INFO)

        if mode == 1:
            self.p = Process(target=self.funcion1)
            self.p.start()
        elif mode == 2:
            self.p = Process(target=self.funcion2)
            self.p.start()
        
    def unir(self):
        self.p.join()
        print("Salio")

    def iniciar_multis(self):
        self.lanzador(2)
        self.lanzador(1)
        #my_objeto.unir()
"""
def iniciar_multis():
    my_objeto = objeto()
    my_objeto.lanzador(2)
    my_objeto.lanzador(1)
    #my_objeto.unir()
"""


#Ventana principal
frame_root = Tk()

#Configuraciones de la ventana
frame_root.title("Sistema de Mineria TecnoBot")
frame_root.geometry("1080x780")
frame_root.config(bg='white')

arbol = ttk.Treeview(frame_root)
arbol.bind("<<TreeviewSelect>>", item_selected)
arbol.pack(anchor='n',fill='both')
arbol.insert("", 'end', text="Elemento 1")
arbol.insert("", 'end', text="Elemento 2")
arbol.insert("", 'end', text="Elemento 21")
arbol.insert("", 'end', text="Elemento 22")
arbol.insert("", 'end', text="Elemento 3")


#button_eraser = ttk.Button(frame_root, text = "Borrador", command=lambda:my_objeto.lanzador(2))
button_eraser = ttk.Button(frame_root, text = "Borrador")
button_eraser.pack()
#button_marco = ttk.Button(frame_root, text = "marco", command=lambda:my_objeto.lanzador(1))
button_marco = ttk.Button(frame_root, text = "marco")
button_marco.pack()



if __name__ == '__main__':
    
    frame_root.mainloop()


    