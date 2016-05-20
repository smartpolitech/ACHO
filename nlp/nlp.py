#Natural Language Processor for ACHO

import nltk, time
import paho.mqtt.client as mqtt

def parse(text):
	print text
	tokens = nltk.word_tokenize(text)
	print "tokens ", tokens
	#tagged = nltk.pos_tag(tokens)
	#print "tagged", tagged
	return tokens

#coms = {"persiana": {"subir":"acho/blind/up","bajar":"acho/blind/down","parar":"acho/blind/stop"},
#	"luces": {"encender":"acho/lights/on/all","apagar":"acho/lights/off/all"},
#	"television": {"encender":"acho/tv/power","apagar":"acho/tv/power"}
#	}

coms = {"subir": 			{"persiana":"acho/blind/up"},
		"bajar": 			{"persiana":"acho/blind/down"},
		"parar": 			{"persiana":"acho/blind/stop"},
		"encender": 		{"luz": {"uno":"acho/lights/on/1", "dos":"acho/lights/on/2"}, "luces":"acho/lights/on/all", "television":"acho/tv/power"},
		"apagar":			{"luz": {"uno":"acho/lights/off/1", "dos":"acho/lights/off/2"}, "luces":"acho/lights/off/all", "television":"acho/tv/power"},
		"subir seccion": 	{"persiana": "acho/blind/up/few"},
		"bajar seccion": 	{"persiana": "acho/blind/down/few"},
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
	print "hola"
	if(msg.topic=="acho/nlp"):
		print "topic nlp recibido"
		par = parse(msg.payload)
	acs={}     

	for p in par:
		if p in coms or p in acs:
			if p in coms.keys():
				acs = coms[p]
			elif p in acs.keys():	
				acs = acs[p]
				action=True
		
	if action:
		print "publicar topico", acs
		client.publish(acs, "")
                
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)

print "Connected to Mosquitto broker"

while True:
	try:
		client.loop_forever()
	except:
		time.sleep(5)
	
