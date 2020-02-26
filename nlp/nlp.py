#Natural Language Processor for ACHO
# -*- coding: utf-8 -*-

import nltk, time
import paho.mqtt.client as mqtt

def parse(text):
	tokens = nltk.word_tokenize(text)
	newTokens=[]
	for word in tokens:
		newTokens.append(word.lower())
	return newTokens

coms = {"subir": 			{"persiana":"acho/blind/up", "poco":"acho/blind/up/few", "skype": "acho/linux-commands/skype", "firefox": "acho/linux-commands/firefox"},
		"bajar": 			{"persiana":"acho/blind/down", "poco": "acho/blind/down/few"},
		"parar": 			{"persiana":"acho/blind/stop"},
		"encender": 		{"luz": {"1":"acho/lights/on/tv", "2":"acho/lights/on/win", "tele": "acho/lights/on/tv", "ventana": "acho/lights/on/win"}, "luces":"acho/lights/on/all", "televisión":"acho/tv/power", "tele": "acho/tv/power"},
		"apagar":			{"luz": {"1":"acho/lights/off/tv", "2":"acho/lights/off/win", "tele": "acho/lights/off/tv", "ventana": "acho/lights/off/win"}, "luces":"acho/lights/off/all", "televisión":"acho/tv/power", "tele": "acho/tv/power"},
		"buscar":			{"google": "acho/linux-commands/google", "youtube": "acho/linux-commands/youtube", "wikipedia": "acho/linux-commands/wikipedia"},
		"hora":				{"acho/linux-commands/time"},
		"día":				{"acho/linux-commands/date"},
		"chiste":			{"acho/linux-commands/joke"},
		"radio":			{"cope": "acho/linux-commands/cope", "40": "acho/linux-commands/cuarenta", "máxima": "acho/linux-commands/maximaFM", "ser": "acho/linux-commands/ser"},
		"interesante":		{"acho/linux-commands/interesting"},
	}

words = {"subir": 		{'sube','súbeme','abrir','abre','ábreme','levantar','levanta','levántame'},
		 "bajar": 		{'baja', 'bájame', 'cerrar', 'cierra', 'ciérrame'},
		 "parar": 		{'para', 'párame', 'detener', 'detiene', 'detiéneme'},
		 "buscar": 		{'busca', 'búscame', 'encuentra', 'encuéntrame'},
		 "encender":	{'enciende','enciéndeme'},
		 "apagar":		{'apaga', 'apágame'}
		}

##############
## MenQTT
###########

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("acho/nlp/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	
	action=False
	
	if(msg.topic=="acho/nlp"):
		print ("topic nlp recibido")
		par = parse(msg.payload)
		print(par)
	acs={}     
	
	search = ''
	for p in par:
		for a in words.keys():
			if p in words[a]:
				p = a
		if p in coms or p in acs:
			if p in coms.keys():
				acs = coms[p]
				if type(acs) == set:
					for z in acs:
						acs = z
					action=True
			elif p in acs.keys():	
				acs = acs[p]
				if p in ['google','youtube', 'wikipedia']:
					search = msg.payload.lower().split(p+' ')[-1]
				action=True
				
	if action:
		print ("publicar topico", acs, search)
		client.publish(acs, search)
                
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("salareuniones.local", 1883, 60)

print ("Connected to Mosquitto broker")


while True:
	try:
		client.loop_forever()
	except:
		time.sleep(5)
	
