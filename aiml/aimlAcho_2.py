import sys
sys.path.insert(0, "PyAIML")

import aiml
#import os

import nltk, time
import paho.mqtt.client as mqtt

def parse(text):
    print text
    tokens = nltk.word_tokenize(text)
    print "tokens ", tokens
    #tagged = nltk.pos_tag(tokens)
    #print "tagged", tagged
    return tokens



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("acho/nlp/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
"""
    if(msg.topic=="acho/nlp"):
        print "topic nlp recibido"
        par = parse(msg.payload)
        print par
        for p in par:
            print "p", p
            if p in coms.keys():
                acs = coms[p]
                print "acs", acs
                for p2 in par:
                    if p2 in acs.keys():
                        print "accion",acs[p2]
                        client.publish(acs[p2],"")
"""                
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


# The Kernel object is the public interface to
# the AIML interpreter.
kernel = aiml.Kernel()

# Use the 'learn' method to load the contents
# of an AIML file into the Kernel.
kernel.learn("inicial.xml")


kernel.respond("LOAD AIML B")

# Loop forever, reading user input from the command
# line and printing responses.
#while True: 
#	print kernel.respond(raw_input("HABLAME...> "))
print kernel.respond(msg.payload)
