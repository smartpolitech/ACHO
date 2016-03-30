import cv2
import numpy as np
from matplotlib import pyplot as plt

def media(imagen):   
    for i in range(420):
        suma = 0
        for j in range(610):
            suma = suma + imagen[i][j]
   
        suma = suma // 610
        for j in range(610):
            imagen[i][j] = suma
    return imagen

def calcula(imagen):
   
    num = 0

    while imagen[419-num][40] > 0 and num < 420:       
            num += 1       
    return int (round(num/4.2 ,0))

cap =  cv2.VideoCapture(0)
    
ret, frame = cap.read()
frame = frame[0:420, 790:1400]

cv2.adaptiveThreshold(media(frame),255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
print(calcula(cap))