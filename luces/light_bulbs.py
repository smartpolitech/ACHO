from lifxlan import *
import ConfigParser
import time
import paho.mqtt.client as mqtt
import os
from subprocess import call

num_lights = None
lifx = LifxLAN(num_lights)
config = ConfigParser.RawConfigParser()
devices = lifx.get_lights()
bombilla1 = 'd0:73:d5:10:7b:0e'
bombilla2 = 'd0:73:d5:10:7f:33'


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("acho/bombillas/#")


def on_message(client, userdata, msg):

    if (msg.topic == "acho/bombillas/enciende1"):
        discover()
        client.publish("acho/bombillas", "encendiendo bombilla 1")
        turn_light_on(bombilla1)
    elif (msg.topic == "acho/bombillas/enciende2"):
        discover()
        client.publish("acho/bombillas", "encendiendo bombilla 2")
        turn_light_on(bombilla2)
    elif (msg.topic == "acho/bombillas/enciende"):
        print "hola que ase"
        discover()
        client.publish("acho/bombillas", "encendiendo bombillas")
        turn_light_on(bombilla1)
        turn_light_on(bombilla2)
    elif (msg.topic == "acho/bombillas/apaga1"):
        print "topic recibido"
        discover()
        client.publish("acho/bombillas", "encendiendo bombilla 1")
        turn_light_off(bombilla1)
    elif (msg.topic == "acho/bombillas/apaga2"):
        discover()
        client.publish("acho/bombillas", "encendiendo bombilla 2")
        turn_light_off(bombilla2)
        print "topic recibido"
    elif (msg.topic == "acho/bombillas/apaga"):
        print "topic recibido"
        discover()
        client.publish("acho/bombillas", "encendiendo bombillas")
        turn_light_off(bombilla1)
        turn_light_off(bombilla2)
    elif (msg.topic == "acho/bombillas/unpocobrillo1"):
        discover()
        client.publish("acho/bombillas", "encendiendo bombilla 1")
        control_percentual_vble_B(bombilla1)
    elif (msg.topic == "acho/bombillas/unpocobrillo2"):
        discover()
        client.publish("acho/bombillas", "encendiendo bombilla 2")
        control_percentual_vble_B(bombilla2)
    elif (msg.topic == "acho/bombillas/unpocobrillo"):
        discover()
        client.publish("acho/bombillas", "encendiendo bombillas")
        control_percentual_vble_B(bombilla1)
        control_percentual_vble_B(bombilla2)
    elif (msg.topic == "acho/bombillas/brillo1"):
        discover()
        client.publish("acho/bombillas", "encendiendo bombilla 1")
        control_percentual_total_B(bombilla1)
    elif (msg.topic == "acho/bombillas/brillo2"):
        discover()
        client.publish("acho/bombillas", "encendiendo bombilla 2")
        control_percentual_total_B(bombilla2)
    elif (msg.topic == "acho/bombillas/brillo"):
        discover()
        client.publish("acho/bombillas", "encendiendo bombillas")
        control_percentual_total_B(bombilla1)
        control_percentual_total_B(bombilla2)
    elif (msg.topic == "acho/bombillas/unpococolor1"):
        discover()
        client.publish("acho/bombillas", "encendiendo bombilla 1")
        control_percentual_vble_K(bombilla1)
    elif (msg.topic == "acho/bombillas/unpococolor2"):
        discover()
        client.publish("acho/bombillas", "encendiendo bombilla 2")
        control_percentual_vble_K(bombilla2)
    elif (msg.topic == "acho/bombillas/unpococolor"):
        discover()
        client.publish("acho/bombillas", "encendiendo bombillas")
        control_percentual_vble_K(bombilla1)
        control_percentual_vble_K(bombilla2)
    elif (msg.topic == "acho/bombillas/color1"):
        discover()
        client.publish("acho/bombillas", "encendiendo bombilla 1")
        control_percentual_total_K(bombilla1)
    elif (msg.topic == "acho/bombillas/color2"):
        discover()
        client.publish("acho/bombillas", "encendiendo bombilla 2")
        control_percentual_total_K(bombilla2)
    elif (msg.topic == "acho/bombillas/color"):
        discover()
        client.publish("acho/bombillas", "encendiendo bombillas")
        control_percentual_total_K(bombilla1)
        control_percentual_total_K(bombilla2)


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


def turn_light_on(light):
    global num_lights
    global lifx
    global config
    global devices
    lifx = LifxLAN(num_lights)
    for d in devices:
        if d.get_mac_addr() == light:
            bombilla = d
            break
    bombilla.set_power("on")
    print (bombilla.get_color())


def turn_light_off(light):
    global num_lights
    global lifx
    global config
    global devices
    lifx = LifxLAN(num_lights)
    for d in devices:
        if d.get_mac_addr() == light:
            bombilla = d
            break
    bombilla.set_power("off")


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
            break
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
