#
# PERSIANA
#

#from skyfield.api import load 
from astral import Astral 
import paho.mqtt.client as mqtt
import os, _thread, time
from datetime import datetime, timedelta
from pytz import timezone
import pytz
from subprocess import call

ARDUINO = "192.168.0.106"
tiempo = 0
posicion_persiana = 0
isSubiendo = False
esDeDia = False
esDeNoche = False

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
    client.publish('acho/tts', '        Parando persiana')
    call(["curl", "http://root:opticalflow@" +ARDUINO + "/arduino/command/blindstop"])


# Secc es un numero del 1 al 5, 1 es 1/5 y el 5 el recorrido entero

def bajar_persiana_por_seccion(secc):
    client.publish('acho/tts', '        Buenas noches, bajando persiana')
    call(["curl", "http://root:opticalflow@" + ARDUINO + "/arduino/command/blinddown"])
    print("Bajando persiana a tramos.")
    time.sleep(secc*4)
    parar_persiana()
	
def subir_persiana_por_seccion(secc):
    client.publish('acho/tts', 'Buenos dias')
    call(["curl", "http://root:opticalflow@" + ARDUINO + "/arduino/command/blindup"])
    print("Subiendo persiana a tramos.")
    time.sleep(secc*4)
    parar_persiana()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("acho/blind/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    print (msg.topic)

    if(msg.topic == "acho/blind/up"):
        client.publish('acho/tts', '        Subiendo persiana')
        call(["curl", "http://root:opticalflow@" + ARDUINO + "/arduino/command/blindup"])
        initTiempo(True)		

    if(msg.topic == "acho/blind/down"):
        client.publish('acho/tts', '        Bajando persiana')
        call(["curl", "http://root:opticalflow@" + ARDUINO + "/arduino/command/blinddown"]) 
        initTiempo(False)		

    if(msg.topic == "acho/blind/stop"):
        client.publish('acho/tts', '        Parando persiana')
        finTiempo()
        call(["curl", "http://root:opticalflow@" +ARDUINO + "/arduino/command/blindstop"])    
	
    if(msg.topic == "acho/blind/up/few"):
        client.publish('acho/tts', '        Subiendo un poco la persiana')
        subir_persiana_por_seccion(1)
	
    if(msg.topic == "acho/blind/down/few"):
        client.publish('acho/tts', '        Bajando un poco la persiana')
        bajar_persiana_por_seccion(1)


def blindController():
    global esDeDia
    global esDeNoche
    print ("\nEntering lind controller")
    
    
    while True:
        print ("Checking sunset at ", str(datetime.now().replace(tzinfo=pytz.UTC)))
        
        city_name = 'Madrid'
        a = Astral()
        a.solar_depression = 'civil'
        city = a[city_name]
        sun = city.sun(date=datetime.today(), local=True)
        
        print ("\nPuesta del sol: " + str(sun['sunset'].replace(tzinfo=pytz.UTC)))
        print ("Amanecer: " + str(sun['sunrise'].replace(tzinfo=pytz.UTC)) + "\n")

        print ("Hora UTC: " + str(datetime.now().replace(tzinfo=pytz.UTC)) + "\n")

        if ((datetime.now().replace(tzinfo=pytz.UTC) > sun['sunset'].replace(tzinfo=pytz.UTC)) and (esDeNoche != True)):
            print ("Buenas noches, bajando persiana\n")
            client.publish('acho/tts', '        Buenas noches, bajando persiana')
            call(["curl", "http://root:opticalflow@" + ARDUINO + "/arduino/command/blinddown"])  
            esDeNoche = True 
        
        if (datetime.today().weekday() >= 0 and datetime.today().weekday() < 5 and 
        datetime.now().replace(tzinfo=pytz.UTC) > sun['sunrise'].replace(tzinfo=pytz.UTC) and 
        datetime.now().replace(tzinfo=pytz.UTC) < sun['sunset'].replace(tzinfo=pytz.UTC) and (esDeDia != True)):
            print ("        Buenos dias, subiendo persiana\n")
            client.publish('acho/tts', 'Buenos dias')
            call(["curl", "http://root:opticalflow@" + ARDUINO + "/arduino/command/blindup"])    
            esDeDia = True

        time.sleep(300)
            
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("salareuniones.local", 1883, 60)
print ("Connected to Mosquitto broker")

try:
   _thread.start_new_thread(client.loop_forever, ()) 
   _thread.start_new_thread(blindController, ())
except:
   print ("Error: unable to start thread")

while True:
    time.sleep(0.1)
    pass
