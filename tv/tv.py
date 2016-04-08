# -*- coding: utf-8 -*-
#
# TELEVISION
#

import paho.mqtt.client as mqtt
import os
from subprocess import call

arduino = "root:opticalflow@192.168.0.101"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("acho/tv/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    if(msg.topic=="acho/tv/power"):
	call(["curl", arduino+"/arduino/command/power"])
	client.publish("acho/tts", "Apagando la television")
        print "topic power recibido"
    
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
print "Connected to Mosquitto broker"

client.loop_forever()
