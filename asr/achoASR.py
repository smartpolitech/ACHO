import speech_recognition as sr

import paho.mqtt.client as mqtt
import os
from subprocess import call

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("acho/asr/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    if(msg.topic=="acho/asr/wavfile"):
        print "topic power recibido"
	# obtain audio from the microphone
	r = sr.Recognizer()
	with sr.WavFile(msg.payload) as source:
	    audio = r.record(source)
	# recognize speech using Google Speech Recognition
	try:
		transcription = r.recognize_google(audio, language="es-ES")
		print("Transcription: " + transcription)
		client.publish("acho/nlp",transcription)
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not understand audio")
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
print "Connected to Mosquitto broker"

client.loop_forever()
