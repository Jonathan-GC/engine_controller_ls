import threading
from tkinter import *
import time

def funcion1():
    for i in range(5):
        print("Hola ", i)
        time.sleep(0.5)

def funcion2():
    for i in range(5):
        print("bienvenido ", i)
        time.sleep(2)

hilo1 = threading.Thread(target=funcion1)
hilo2 = threading.Thread(target=funcion2)



hilo1.start()
hilo2.start()

hilo1.join()
hilo2.join()

print("Adios")

"""
raiz = Tk()
but1 = Button(raiz, text="funcion1", command=funcion1)
but1.pack()
but2 = Button(raiz, text="funcion2", command=funcion2)
but2.pack()

raiz.mainloop()"""