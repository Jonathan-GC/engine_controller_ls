import easyocr
import cv2

Reader = easyocr.Reader(['es'], gpu=True)


cap = cv2.VideoCapture("sources/emocionesVideo1.mp4")


while 1:
    _, img = cap.read()

    if _ == False :
        break
    
    
    cv2.imshow("img", img)
    results = Reader.readtext(img)
    print(results)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

#result = Reader.readtext('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTMqpp6mrQydQ_NPbyUuB4X8ggSBh4knhqHSf7V0oRilf2Ivkqts-2F7zAxPWqMbuuB1aQ&usqp=CAU')
#print(result)