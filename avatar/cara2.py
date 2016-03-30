import paho.mqtt.client as mqtt
import pygame, sys, time
from pygame.locals import *
from time import *
import re

pygame.init()
windowSurface = pygame.display.set_mode((259, 271), 0, 32)
pygame.display.set_caption("Cara animada")

BACKGROUND = (255, 255, 255)

windowSurface.fill(BACKGROUND)
img=pygame.image.load('animate/face_normal.png')
windowSurface.blit(img,(0,0))
pygame.display.update()
sleep(0.2)

# Minimize window
#pygame.display.iconify()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("acho/tts/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  
    if(msg.topic=="acho/tts"):
	print "topic tts recibido"
	windowSurface = pygame.display.set_mode((259, 271), 0, 32)
	paragraph = str(msg.payload) 
	paragraph = re.sub('[!,;?]', '.', paragraph)
	lastImage = pygame.image.load('animate/face_normal.png')

	for sentence in paragraph.split("."):

		sleep(0.24)
		for word in sentence.split():
	
			timePerChar = 0.444/float(len(word))
			for char in word:

				#print char
				windowSurface.fill(BACKGROUND)

				if "m" in char.lower() or "b" in char.lower() or "p" in char.lower():
					img=pygame.image.load('animate/face_mbp.png')
				elif "e" in char.lower():
					img=pygame.image.load('animate/face_ee.png')
				elif "i" in char.lower():
					img=pygame.image.load('animate/face_i.png')
				elif "l" in char.lower() or "z" in char.lower():
					img=pygame.image.load('animate/face_l.png')
				elif "f" in char.lower() or "v" in char.lower():
					img=pygame.image.load('animate/face_fv.png')
				elif "g" in char.lower() or "j" in char.lower() or "ch" in char.lower():
					img=pygame.image.load('animate/face_gshch.png')
				elif "s" in char.lower() or "d" in char.lower() or "t" in char.lower() or "r" in char.lower() or "k" in char.lower() or "c" in char.lower():
					img=pygame.image.load('animate/face_sdtrck.png')
				elif "a" in char.lower():
					img=pygame.image.load('animate/face_a.png')
				elif "o" in char.lower():
					img=pygame.image.load('animate/face_o2.png')
				else:
					img = lastImage

				windowSurface.blit(img,(0,0))
				pygame.display.update()
				sleep(timePerChar)
				lastImage = img

			windowSurface.fill(BACKGROUND)
			img=pygame.image.load('animate/face_normal.png')
			lastImage = img
			windowSurface.blit(img,(0,0))
			pygame.display.update()
			sleep(0.04)

		windowSurface.fill(BACKGROUND)
		img=lastImage
		windowSurface.blit(img,(0,0))
		pygame.display.update()
		sleep(0.4)

	sleep(1)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
print "Connected to Mosquitto broker"

client.loop_forever()

