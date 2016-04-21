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

    if(msg.topic=="acho/asr/power"):
	call(["curl", arduino+"/arduino/command/power"])
	client.publish("acho/tts", "Usando voz")
        print "topic power recibido"
    

# obtain audio from the microphone
r = sr.Recognizer()

file_path = d + '_voice.ogg'
self.bot.downloadFile(message['voice']['file_id'], file_path)
os.system('ffmpeg -y -i ' + file_path + ' audio.wav')
with sr.WavFile("audio.wav") as source:
    print("   Say something to Acho!")
    audio = r.record(source)

# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
	transcription = r.recognize_google(audio, language="es-ES", key=GOOGLE_SPEECH_KEY)
	print("Transcription: " + transcription)
	self.sendmail("recuerda", transcription)

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
	
except sr.RequestError as e::
		print("Could not understand audio")
    
def handle_audio(self, message):
	d = dateStringFromTimestamp(message['date'])
	r = sr.Recognizer()
    
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
print "Connected to Mosquitto broker"

client.loop_forever()
