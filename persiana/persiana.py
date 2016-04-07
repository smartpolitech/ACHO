#
# PERSIANA
#

import paho.mqtt.client as mqtt
import os, thread, time, datetime, ephem
from subprocess import call

ARDUINO = "192.168.0.101"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("acho/blind/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    print msg.topic

    if(msg.topic=="acho/blind/up"):
        call(["curl", "http://root:opticalflow@" + ARDUINO + "/arduino/command/blindup"])    
	client.publish('acho/tts', 'Subiendo persiana')

    if(msg.topic=="acho/blind/down"):
        call(["curl", "http://root:opticalflow@" + ARDUINO + "/arduino/command/blinddown"])    
	client.publish('acho/tts', 'Bajando persiana')

    if(msg.topic=="acho/blind/stop"):
        call(["curl", "http://root:opticalflow@" +ARDUINO + "/arduino/command/blindstop"])    
	client.publish('acho/tts', 'Parando persiana')


def blindController():
    print "Entering lind controller"
    while True:
	print "Checking sunset at ", str(datetime.datetime.now())
        o=ephem.Observer()  
        o.lat='39.4'  
        o.long='-6.3'  
        s=ephem.Sun()  
        s.compute()  
        print ephem.localtime(o.next_rising(s)) , ephem.localtime(o.next_setting(s))
        chapar = datetime.datetime.now().replace(hour=21, minute = 30)
        if datetime.datetime.today() > ephem.localtime(o.next_setting(s)) or datetime.datetime.today() > chapar:
            print "Good night. lowering blids"
            call(["curl", "http://root:opticalflow@" + ARDUINO + "/arduino/command/blinddown"])    
        if datetime.datetime.today().weekday() >= 0 and datetime.datetime.today().weekday() < 5 and datetime.datetime.today() > ephem.localtime(o.next_rising(s)):
            print "Good morning. raising blinds"
            call(["curl", "http://root:opticalflow@" + ARDUINO + "/arduino/command/blindup"])    

        time.sleep(60*10)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
print "Connected to Mosquitto broker"

try:
   thread.start_new_thread( client.loop_forever, () )
   thread.start_new_thread( blindController, () )
except:
   print "Error: unable to start thread"

while True:
    time.sleep(0.1)
    pass
