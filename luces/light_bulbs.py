from lifxlan import *
import ConfigParser
import time
import paho.mqtt.client as mqtt
import os
from subprocess import call

num_lights = None
lifx = LifxLAN(verbose = False)
config = ConfigParser.RawConfigParser()

devices = lifx.get_lights()
print("\n {} luces encontradas \n".format(len(devices)))
for d in devices:
        print d.mac_addr, d.port, d.service, d.source_id, d.ip_addr

bombilla1 = 'd0:73:d5:10:7b:0e'
bombilla2 = 'd0:73:d5:10:7f:33'
#devices = {}
#devices[bombilla1] = Light(bombilla1, 1, 56700, 542952283, "192.168.0.102")
#devices[bombilla2] = Light(bombilla2, 1, 56700, 542952283, "192.168.0.103")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("acho/lights/#")

def turn_light_on(lights):
	for l in lights:
		d = [x for x in devices if x.mac_addr == l][0]
		d.set_power("on");
    
def turn_light_off(lights):
	for l in lights:
		d = [x for x in devices if x.mac_addr == l][0]
		d.set_power("off")
		
topics = {"acho/lights/on/all":  { "command": turn_light_on, "params": [bombilla1, bombilla2], "text": "encendiendo luces" },
		  "acho/lights/off/all": { "command": turn_light_off, "params": [bombilla1, bombilla2],  "text": "apagando luces" },
  		  "acho/lights/on/1": 	 { "command": turn_light_on, "params": [bombilla1], "text" : "encendiendo luz uno" },
  		  "acho/lights/on/2": 	 { "command": turn_light_on, "params": [bombilla2], "text" : "encendiendo luz dos" },
		  "acho/lights/off/1": 	 { "command": turn_light_off, "params": [bombilla1], "text" : "apagando  luz uno" }
		  "acho/lights/off/2": 	 { "command": turn_light_off, "params": [bombilla2], "text" : "apagando luz dos" }
		  "acho/lights/brightnessup" :  
		 
		  }

def on_message(client, userdata, msg):
	print "topic", msg.topic
	if msg.topic in topics:
		t = topics[msg.topic]
		client.publish("acho/tts", t["text"])
		t["command"](t["params"]) 	
    
    #elif (msg.topic == "acho/bombillas/unpocobrillo1"):
        #client.publish("acho/tts", "encendiendo bombilla 1")
        #control_percentual_vble_B(bombilla1)
    #elif (msg.topic == "acho/bombillas/unpocobrillo2"):
        #client.publish("acho/tts", "encendiendo bombilla 2")
        #control_percentual_vble_B(bombilla2)
    #elif (msg.topic == "acho/bombillas/unpocobrillo"):
        #client.publish("acho/tts", "encendiendo bombillas")
        #control_percentual_vble_B(bombilla1)
        #control_percentual_vble_B(bombilla2)
    #elif (msg.topic == "acho/bombillas/brillo1"):
        #client.publish("acho/tts", "encendiendo bombilla 1")
        #control_percentual_total_B(bombilla1)
    #elif (msg.topic == "acho/bombillas/brillo2"):
        #client.publish("acho/tts", "encendiendo bombilla 2")
        #control_percentual_total_B(bombilla2)
    #elif (msg.topic == "acho/bombillas/brillo"):
        #client.publish("acho/tts", "encendiendo bombillas")
        #control_percentual_total_B(bombilla1)
        #control_percentual_total_B(bombilla2)
    #elif (msg.topic == "acho/bombillas/unpococolor1"):
        #client.publish("acho/tts", "encendiendo bombilla 1")
        #control_percentual_vble_K(bombilla1)
    #elif (msg.topic == "acho/bombillas/unpococolor2"):
        #discover()
        #client.publish("acho/tts", "encendiendo bombilla 2")
        #control_percentual_vble_K(bombilla2)
    #elif (msg.topic == "acho/bombillas/unpococolor"):
        #client.publish("acho/bombillas", "encendiendo bombillas")
        #control_percentual_vble_K(bombilla1)
        #control_percentual_vble_K(bombilla2)
    #elif (msg.topic == "acho/bombillas/color1"):
        #client.publish("acho/tts", "encendiendo bombilla 1")
        #control_percentual_total_K(bombilla1)
    #elif (msg.topic == "acho/bombillas/color2"):
        #client.publish("acho/tts", "encendiendo bombilla 2")
        #control_percentual_total_K(bombilla2)
    #elif (msg.topic == "acho/bombillas/color"):
        #client.publish("acho/tts", "encendiendo bombillas")
        #control_percentual_total_K(bombilla1)
        #control_percentual_total_K(bombilla2)


def discover():
    global num_lights
    global lifx
    global config
    global devices

    print("\n {} luces encontradas \n".format(len(devices)))
    for d in devices:
        print(d)
        # i += 1
        # aux_mac = config.get('bombilla_{}'.format(i), 'mac')
        # if aux_mac != d.get_mac_addr():
        #     d.set_label("bombilla_{}".format(i))
        #     config.add_section('bombilla_{}'.format(i))
        #     config.set('bombilla_{}'.format(i), 'mac', d.get_mac_addr())
        #     with open('bulbs.cfg', 'wb') as configfile:
        #         config.write(configfile)



# FROM 0 to 65535
def modify_S(light, quantity):
    global num_lights
    global lifx
    global config
    global devices
    lifx = LifxLAN(num_lights)
    devices = lifx.get_lights()
    bombilla = devices[light]
    if bombilla.get_power() != 0:
        color = bombilla.get_color()
        color[1] = quantity
        bombilla.set_color(color)


# FROM 0 to 65535
def modify_B(light, quantity):
    global num_lights
    global lifx
    global config
    global devices
    lifx = LifxLAN(num_lights)
    devices = lifx.get_lights()
    for d in devices:
        if d.get_mac_addr() == light:
            bombilla = d
            break
    ogcolor = bombilla.get_color()
    if ogcolor[2] <= quantity:
        for i in range(ogcolor[2], quantity, 100):
            color = [ogcolor[0], ogcolor[1], i, ogcolor[3]]
            bombilla.set_color(color)
            print bombilla.get_color()
    elif ogcolor[2] > quantity:
        for i in range(ogcolor[2], quantity, -100):
            color = [ogcolor[0], ogcolor[1], i, ogcolor[3]]
            bombilla.set_color(color)
            print bombilla.get_color()


# FROM 2500 to 9000
def modify_K(light, quantity):
    global num_lights
    global lifx
    global config
    global devices
    lifx = LifxLAN(num_lights)
    devices = lifx.get_lights()
    for d in devices:
        if d.get_mac_addr() == light:
            bombilla = d
            break
    ogcolor = bombilla.get_color()
    if ogcolor[3] <= quantity:
        for i in range(ogcolor[3], quantity, 100):
            color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
            bombilla.set_color(color)
            print bombilla.get_color()
    elif ogcolor[3] > quantity:
        for i in range(ogcolor[3], quantity, -100):
            color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
            bombilla.set_color(color)
            print bombilla.get_color()


def control_percentual_vble_K(light):
    
    ogcolor = bombilla.get_color()
    quantity = ogcolor[3] * 0.1
    if ogcolor[3] <= quantity:
        for i in range(ogcolor[3], quantity, 100):
            color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
            bombilla.set_color(color)
            print bombilla.get_color()
    elif ogcolor[3] > quantity:
        for i in range(ogcolor[3], quantity, -100):
            color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
            bombilla.set_color(color)
            print bombilla.get_color()


def control_percentual_total_K(light):
    global num_lights
    global lifx
    global config
    global devices
    lifx = LifxLAN(num_lights)
    devices = lifx.get_lights()
    for d in devices:
        if d.get_mac_addr() == light:
            bombilla = d
            break
    ogcolor = bombilla.get_color()
    if ogcolor[3] <= 900:
        for i in range(ogcolor[3], 900, 100):
            color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
            bombilla.set_color(color)
            print bombilla.get_color()
    elif ogcolor[3] > 900:
        for i in range(ogcolor[3], 900, -100):
            color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
            bombilla.set_color(color)
            print bombilla.get_color()


def control_percentual_vble_B(light):
    global num_lights
    global lifx
    global config
    global devices
    lifx = LifxLAN(num_lights)
    devices = lifx.get_lights()
    for d in devices:
        if d.get_mac_addr() == light:
            bombilla = d
            break
    ogcolor = bombilla.get_color()
    quantity = ogcolor[2] * 0.1
    if ogcolor[2] <= quantity:
        for i in range(ogcolor[3], quantity, 100):
            color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
            bombilla.set_color(color)
            print bombilla.get_color()
    elif ogcolor[2] > quantity:
        for i in range(ogcolor[3], quantity, -100):
            color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
            bombilla.set_color(color)
            print bombilla.get_color()


def control_percentual_total_B(light):
    global num_lights
    global lifx
    global config
    global devices
    lifx = LifxLAN(num_lights)
    devices = lifx.get_lights()
    for d in devices:
        if d.get_mac_addr() == light:
            bombilla = d
            
    ogcolor = bombilla.get_color()
    if ogcolor[2] <= 3650:
        for i in range(ogcolor[3], 3650, 100):
            color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
            bombilla.set_color(color)
            print bombilla.get_color()
    elif ogcolor[2] > 3650:
        for i in range(ogcolor[3], 3650, -100):
            color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
            bombilla.set_color(color)
            print bombilla.get_color()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
print "Connected to Mosquitto broker"

client.loop_forever()
