import cv2
import numpy as np
from matplotlib import pyplot as plt

def media(frame):   
    for i in range(420):
        suma = 0
        for j in range(610):
            suma = suma + frame[i][j]
   
        suma = suma // 610
        for j in range(610):
            frame[i][j] = suma
    return frame

def calcula(frame):
   
    num = 0
    while frame[419-num][40] > 0 and num < 420:       
            num += 1       
    return int (round(num/4.2 ,0))


def get_image():
 retval, im = camera.read()
 return im

camera = cv2.VideoCapture(1)
frame = get_image()

#cv2.imshow('img1',frame) 

print frame.shape[:2]

#frame = frame[0:420, 790:1400]

cv2.imshow('img1',frame) #display the captured image

cv2.adaptiveThreshold(media(frame),255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
print(calcula(frame)) 

while True:
	if cv2.waitKey(1) & 0xFF == ord('y'): #save on pressing 'y' 
	        cv2.destroyAllWindows()
 		break

camera.release()

    
