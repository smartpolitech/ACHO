import cv2
from matplotlib import pyplot as plt
import paho.mqtt.client as mqtt

def recorte(img):
	height, width = img.shape
	porx = 25
	porx2 = 45 
	pory = 48
	x = (porx * width) / 100
	x2 = (porx2 * width) / 100
	y = (pory * height) / 100
	recorte = img.copy()[0:y, x:x2]
	return recorte

def mostrar(img, persiana, modificada, binarizada):
    plt.subplot(1,4,1), plt.imshow(img,        cmap = 'gray', interpolation = 'bicubic'), plt.xticks([]), plt.yticks([])	
    plt.subplot(1,4,2), plt.imshow(persiana,   cmap = 'gray', interpolation = 'bicubic'), plt.xticks([]), plt.yticks([])
    plt.subplot(1,4,3), plt.imshow(modificada, cmap = 'gray', interpolation = 'bicubic'), plt.xticks([]), plt.yticks([])
    plt.subplot(1,4,4), plt.imshow(binarizada, cmap = 'gray', interpolation = 'bicubic'), plt.xticks([]), plt.yticks([])
    plt.show()

def estirar(modificada, anchura, altura):  	
    for i in range(altura):
	acumulador = 0
        for j in range(anchura):
            acumulador = acumulador + modificada[i][j]  

        acumulador = acumulador // anchura

        for k in range(anchura):
            modificada[i][k] = acumulador

def calcula(imagen, altura):
    num = 0
    while imagen[altura-1-num][40] > 0 and num < altura:		
	num += 1		
    return (100-(int (round(num*100/altura, 0))))

def proceso():
	cap = cv2.VideoCapture("http://salareuniones-robolab.duckdns.org:8080/?action=stream")

	ret, img = cap.read()
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
	persiana = recorte(img)

	modificada = persiana.copy()
	altura, anchura = modificada.shape
	
	estirar(modificada, anchura, altura)		 

	binarizada = modificada.copy()
	(thresh, binarizada) = cv2.threshold(binarizada, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

	porcent = calcula(binarizada, altura)
	
	#print(porcent)
	#mostrar(img, persiana, modificada, binarizada)

	return porcent

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("acho/blindstate/#")


def on_message(client, userdata, msg):
	if msg.topic == "acho/blindstate/get":
		porcent = proceso()
		client.publish("acho/blindstate/now", str(porcent))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
print "Connected to Mosquitto broker"

while True:
    try:
        client.loop_forever()
    except:
        time.sleep(5)

