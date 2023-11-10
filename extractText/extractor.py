import cv2
import easyocr

import threading

reader = easyocr.Reader(["es"], gpu=False)
captura = cv2.VideoCapture("../sources/Dictionary/personas/2.mp4")


def analisiText(img):
    result = reader.readtext(img, paragraph=False)
    #return result
    print (result)
    return result



fotograma = 0
HILOS = []


    



while 1:

    _, imagen = captura.read()

    if not _:
        break
    else:
        fotograma += 1
        cv2.imshow("video", imagen)

        if fotograma % 180:
            pass

        
        #if cv2.waitKey(1) == 27:
        #    break
        if cv2.waitKey(9) == 9:
            #imagenes.append(fotograma)
            HILOS.append(threading.Thread(target=analisiText, args=(imagen,)))
        elif cv2.waitKey(1) == 27:
            break

captura.release()
cv2.destroyAllWindows()



for hilo in HILOS:
    print(hilo)
    hilo.start()
    hilo.join()




