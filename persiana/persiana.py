#
# PERSIANA
#

import paho.mqtt.client as mqtt
import os, thread, time, datetime, ephem
from subprocess import call

ARDUINO = "192.168.0.101"
tiempo = 0;
posicion_persiana = 0
isSubiendo = False;

def moduloInferior(num, divisor):
    return num - (num%divisor)

def moduloSuperior(num, divisor):
    return (num+5) - (num%divisor)

def calculaTiempoSeccion():
    global posicion_persiana
    global isSubiendo
    if isSubiendo:
        return moduloSuperior(posicion_persiana,5)-posicion_persiana
    return posicion_persiana - moduloInferior(posicion_persiana,5)
		
def initTiempo(estadoSubiendo):
    global isSubiendo
    global tiempo
    global posicion_persiana
    isSubiendo = estadoSubiendo
    tiempo = time.time()

def finTiempo():
    global isSubiendo
    global tiempo
    global posicion_persiana
    if isSubiendo:
	    posicion_persiana+=time.time()-tiempo
    else:
	    posicion_persiana-=time.time()-tiempo
    #Comprobaciones finales
    if posicion_persiana > 25:
        posicion_persiana = 25
    if posicion_persiana < 0:
        posicion_persiana = 0

def parar_persiana():
    client.publish('acho/tts', 'Parando persiana')
    call(["curl", "http://root:opticalflow@" +ARDUINO + "/arduino/command/blindstop"])

def bajar_persiana_por_seccion(secc):
    global posicion_persiana
    initTiempo(False)
    call(["curl", "http://root:opticalflow@" + ARDUINO + "/arduino/command/blinddown"])
    print("Bajando persiana a tramos.")
    time.sleep(calculaTiempoSeccion())
    #Restamos al tiempo acumulado de la persiana el tiempo dedicado para la bajada ejecutada 
    finTiempo()
    parar_persiana()
	
def subir_persiana_por_seccion(secc):
    global posicion_persiana
    initTiempo(True)
    call(["curl", "http://root:opticalflow@" + ARDUINO + "/arduino/command/blindup"])
    print("Subiendo persiana a tramos.")
    time.sleep(calculaTiempoSeccion())
    #Sumamos al tiempo acumulado de la persiana el tiempo dedicado para la subida ejecutada 
    finTiempo()
    parar_persiana()

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
        client.publish('acho/tts', 'Subiendo persiana')
        call(["curl", "http://root:opticalflow@" + ARDUINO + "/arduino/command/blindup"])
        initTiempo(True)		

    if(msg.topic=="acho/blind/down"):
        client.publish('acho/tts', 'Bajando persiana')
        call(["curl", "http://root:opticalflow@" + ARDUINO + "/arduino/command/blinddown"]) 
        initTiempo(False)		

    if(msg.topic=="acho/blind/stop"):
        client.publish('acho/tts', 'Parando persiana')
        finTiempo()
        call(["curl", "http://root:opticalflow@" +ARDUINO + "/arduino/command/blindstop"])    
	
    if(msg.topic=="acho/blind/up/few"):
        client.publish('acho/tts', 'Subiendo un poco la persiana')
        subir_persiana_por_seccion(1)
	
    if(msg.topic == "acho/blind/down/few"):
        client.publish('acho/tts', 'Bajando un poco la persiana')
        bajar_persiana_por_seccion(1)


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
