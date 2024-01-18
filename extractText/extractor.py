import cv2
import easyocr

import threading

reader = easyocr.Reader(["es"], gpu=True)
#captura = cv2.VideoCapture("../sources/Dictionary/personas/2.mp4")
captura = cv2.VideoCapture("sources/Dictionary/personas/2.mp4")


#Roi Definido por dos puntos
p1, p2 = None, None
estado = 0

def seleccionar_area_de_texto(event, x, y, flags, param):
    global estado, p1, p2

    if event == cv2.EVENT_LBUTTONDBLCLK:
       #Seleccionar primer punto
        if estado == 0:
            p1 = (x, y)
            estado += 1
            print("Hola")
            
        #selecionar segundo punto
        elif estado == 1:
            p2 = (x, y)
            estado += 1
            print("Hola2")
    
    if event == cv2.EVENT_RBUTTONUP:
        
        p1, p2 = None, None
        estado = 0




def analisiText(img):
    result = reader.readtext(img, paragraph=False)
    #return result
    print (result)
    return result



fotograma = 0
HILOS = []


    
#introducir los callBack del mouse
cv2.namedWindow('video')
cv2.setMouseCallback("video", seleccionar_area_de_texto)


while 1:

    _, imagen = captura.read()

    if not _:
        break
    else:
        # si el roi esta seleccionado dibujelo
        if estado  > 1:
            cv2.rectangle(imagen, p1, p2, (255, 0, 0), 10)
        
        
        
        fotograma += 1
        cv2.imshow("video", imagen)

        if fotograma % 180:
            pass

        if cv2.waitKey(9) == 9:
            #Si hay puntos registre el fotograma
            if p1 != None and p2 !=None:
                #Capture el area de interes  
                imagen_area_interes = imagen[int(p1[1]) : int(p2[1]), int(p1[0]) : int(p2[0])]
                #Procese el texto
                HILOS.append(threading.Thread(target=analisiText, args=(imagen_area_interes,)))
        elif cv2.waitKey(1) == 27:
            break

captura.release()
cv2.destroyAllWindows()



for hilo in HILOS:
    print(hilo)
    hilo.start()
    hilo.join()




