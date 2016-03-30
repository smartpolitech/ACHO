import cv2
import numpy as np
from matplotlib import pyplot as plt

def media(img):  
    for i in range(205):
        suma = 0
        for j in range(255):
            suma = suma + img[i][j]
  
        suma = suma // 255
        for j in range(255):
            img[i][j] = suma
    return img

def calcula(img):
    num = 0
    while img[204-num][40] > 0 and num < 205:  
            num += 1      
    return int (round(num/2.05 ,0))

camera = cv2.VideoCapture(1)
retval, frame = camera.read()

frame = frame[0:205,165:420]   #480 640
cv2.imwrite("una.jpg", frame)

cargada = cv2.imread('una.jpg', cv2.IMREAD_GRAYSCALE)

nueva = media(cargada)


nueva = cv2.adaptiveThreshold(nueva,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
#ret,nueva = cv2.threshold(nueva,127,255,cv2.THRESH_BINARY)
cv2.imshow('img1',nueva)
print(calcula(nueva))


while True:
    if cv2.waitKey(1) & 0xFF == ord('y'):
            cv2.destroyAllWindows()
	    break

camera.release()
