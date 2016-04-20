import paho.mqtt.client as mqtt
import pygame, sys, time
import random
from pygame.locals import *
from time import *
import re

BACKGROUND = (255, 255, 255)

def hide():
	global ishide
	ishide = True
	pygame.display.iconify()
	return

def show():
	pygame.display.quit()
	pygame.display.init()
	windowSurface = pygame.display.set_mode((259, 271), 0, 32)
	pygame.display.set_caption("avatar")

	windowSurface.fill(BACKGROUND)
	img=pygame.image.load('animate/face_normal_random.png')
	windowSurface.blit(img,(0,0))
	pygame.display.update()
	return

def Timer():
	tfinish = time()
	if ((tfinish - tstart >= 20.0)): 
		hide()	
	return

show()
sleep(0.2)
global tstart
tstart = time()
global ishide
ishide = False

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("acho/tts/#")
    client.subscribe("acho/avatar/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  
    if(msg.topic=="acho/avatar/show"):
	show()

    if(msg.topic=="acho/avatar/hide"):
	hide()

    if(msg.topic=="acho/tts"):
	print "topic tts recibido"

	if(ishide):
		show()

	windowSurface = pygame.display.set_mode((259, 271), 0, 32)
	paragraph = str(msg.payload) 
	paragraph = re.sub('[!,;?]', '.', paragraph)
	lastImage = pygame.image.load('animate/face_normal.png')

	for sentence in paragraph.split("."):

		sleep(0.24)
		for word in sentence.split():
	
			timePerChar = 0.444/float(len(word))
			for char in word:

				rand = random.randrange(2)
				windowSurface.fill(BACKGROUND)

				if "m" in char.lower() or "b" in char.lower() or "p" in char.lower():
					if rand:
						img=pygame.image.load('animate/face_mbp.png')
					else:
						img=pygame.image.load('animate/face_mbp_random.png')
				elif "e" in char.lower():
					if rand:
						img=pygame.image.load('animate/face_ee.png')
					else:
						img=pygame.image.load('animate/face_ee_random.png')
				elif "i" in char.lower():
					if rand:
						img=pygame.image.load('animate/face_i.png')
					else:
						img=pygame.image.load('animate/face_i_random.png')
				elif "l" in char.lower() or "z" in char.lower():
					if rand:
						img=pygame.image.load('animate/face_lz.png')
					else:
						img=pygame.image.load('animate/face_lz_random.png')
				elif "f" in char.lower() or "v" in char.lower():
					if rand:
						img=pygame.image.load('animate/face_fv.png')
					else:
						img=pygame.image.load('animate/face_fv_random.png')
				elif "g" in char.lower() or "j" in char.lower() or "ch" in char.lower():
					if rand:
						img=pygame.image.load('animate/face_gjch.png')
					else:
						img=pygame.image.load('animate/face_gjch_random.png')
				elif "s" in char.lower() or "d" in char.lower() or "t" in char.lower() or "r" in char.lower() or "k" in char.lower() or "c" in char.lower():
					if rand:
						img=pygame.image.load('animate/face_sdtrck.png')
					else:
						img=pygame.image.load('animate/face_sdtrck_random.png')
				elif "a" in char.lower():
					if rand:
						img=pygame.image.load('animate/face_a.png')
					else:
						img=pygame.image.load('animate/face_a_random.png')
				elif "o" in char.lower():
					if rand:
						img=pygame.image.load('animate/face_oo.png')
					else:
						img=pygame.image.load('animate/face_oo_random.png')
				else:
					img = lastImage

				windowSurface.blit(img,(0,0))
				pygame.display.update()
				sleep(timePerChar)
				lastImage = img

			windowSurface.fill(BACKGROUND)
			img=pygame.image.load('animate/face_normal_random.png')
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
	global tstart
	tstart = time()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
print "Connected to Mosquitto broker"

while True:
	Timer()
	client.loop()   

