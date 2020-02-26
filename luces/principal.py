from light_bulbs import Luces
import ConfigParser
import paho.mqtt.client as mqtt
import time





    # elif (msg.topic == "acho/bombillas/unpocobrillo1"):
    # client.publish("acho/tts", "encendiendo bombilla 1")
    # control_percentual_vble_B(bombilla1)
    # elif (msg.topic == "acho/bombillas/unpocobrillo2"):
    # client.publish("acho/tts", "encendiendo bombilla 2")
    # control_percentual_vble_B(bombilla2)
    # elif (msg.topic == "acho/bombillas/unpocobrillo"):
    # client.publish("acho/tts", "encendiendo bombillas")
    # control_percentual_vble_B(bombilla1)
    # control_percentual_vble_B(bombilla2)
    # elif (msg.topic == "acho/bombillas/brillo1"):
    # client.publish("acho/tts", "encendiendo bombilla 1")
    # control_percentual_total_B(bombilla1)
    # elif (msg.topic == "acho/bombillas/brillo2"):
    # client.publish("acho/tts", "encendiendo bombilla 2")
    # control_percentual_total_B(bombilla2)
    # elif (msg.topic == "acho/bombillas/brillo"):
    # client.publish("acho/tts", "encendiendo bombillas")
    # control_percentual_total_B(bombilla1)
    # control_percentual_total_B(bombilla2)
    # elif (msg.topic == "acho/bombillas/unpococolor1"):
    # client.publish("acho/tts", "encendiendo bombilla 1")
    # control_percentual_vble_K(bombilla1)
    # elif (msg.topic == "acho/bombillas/unpococolor2"):
    # discover()
    # client.publish("acho/tts", "encendiendo bombilla 2")
    # control_percentual_vble_K(bombilla2)
    # elif (msg.topic == "acho/bombillas/unpococolor"):
    # client.publish("acho/bombillas", "encendiendo bombillas")
    # control_percentual_vble_K(bombilla1)
    # control_percentual_vble_K(bombilla2)
    # elif (msg.topic == "acho/bombillas/color1"):
    # client.publish("acho/tts", "encendiendo bombilla 1")
    # control_percentual_total_K(bombilla1)
    # elif (msg.topic == "acho/bombillas/color2"):
    # client.publish("acho/tts", "encendiendo bombilla 2")
    # control_percentual_total_K(bombilla2)
    # elif (msg.topic == "acho/bombillas/color"):
    # client.publish("acho/tts", "encendiendo bombillas")
    # control_percentual_total_K(bombilla1)
    # control_percentual_total_K(bombilla2)


if __name__ == "__main__":

    client = mqtt.Client()
    # client.on_connect = on__connect
    client.connect("192.168.0.110", 1883, 60)
    print("Connected...")
    client.subscribe("acho/lights/#")
    luces = Luces(client)
    client.on_message = luces.on__message



    client.loop_forever()
