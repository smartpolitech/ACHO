#
# TTS
#

import paho.mqtt.client as mqtt
import os, io, json, pyaudio, time, sys 
from gtts import gTTS
from subprocess import call
from pydub import AudioSegment

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
        tts = gTTS(text=msg.payload, lang='es')
        tts.save("prueba.mp3")
        song = AudioSegment.from_mp3("prueba.mp3")
        song.export("final.wav", format ="wav")
        os.system("aplay final.wav")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
print "Connected to Mosca broker"

client.loop_forever()
