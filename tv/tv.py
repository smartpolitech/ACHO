#
# TELEVISION
#

import paho.mqtt.client as mqtt
import os
from subprocess import call

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("acho/tv/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    if(msg.topic=="acho/tv/power"):
	call(["curl", "http://root:opticalflow@158.49.247.178/arduino/command/power"])
        print "topic power recibido"
    
    if(msg.topic=="acho/tv/uno"):
        call(["curl", "http://root:opticalflow@158.49.247.178/arduino/command/uno"])
        print "topic uno recibido"
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
print "Connected to Mosquitto broker"

client.loop_forever()
