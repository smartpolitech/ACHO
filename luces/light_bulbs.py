from lifxlan import Light, LifxLAN
import time
# import os
# from subprocess import call

lifx = LifxLAN()


#Conocemos la MAC, asignamos segun la MAC
                    ####### LIGHT DATA ######
# bulbTV ---> 'd0:73:d5:10:7f:33'  #FUNCIONA
# bulbWin ---> 'D0:73:D5:2D:52:AF' #FUNCIONA
# OLDbulbWin ---> 'd0:73:d5:10:7b:0e' #NOFUNCIONA


class Luces:

    ###############################
    ###        VARIABLE         ###
    ###############################

    def __init__(self, _client):

        self.client = _client
        self.index = 0
        self.bulbWin = None
        self.bulbTV = None
        self.stateBulbWin = False
        self.stateBulbTV = False

    # Detect devices available and store them on a list
        self.devices = lifx.get_devices()
    # Obtain the number of devices store
        self.num_lights = len(self.devices)

        print (" ======================== LIGHTS =========================")
        print
        print
        print ("Number of lights found: " + self.num_lights.__str__())
        print
        print

    #Asignacion de dispositivos

        while self.index < self.num_lights:
            bulbAux = self.devices[self.index]
            nameSplit = bulbAux.mac_addr.split(":")
            if nameSplit[5] == "33":
                print ("MAC termina en 33. Bombilla TV")
                self.bulbTV = bulbAux

                print ("                    TIPO DE BULBTV: ")
                print ("                    " + str(type.__str__(self.bulbTV)))
                print
                print

            elif nameSplit[5] == "af":
                print ("MAC temina en AF. Bombilla WIN")
                self.bulbWin = bulbAux

                print ("                    TIPO DE BULBWIN: ")
                print ("                    " + str(type.__str__(self.bulbWin)))
                print
                print

        # old bulb ---> NOT WORKS
            elif nameSplit[5] == "0e":
                print ("MAC termina en 0e. Bombilla Win")
                self.bulbWin = bulbAux

                print ("                    TIPO DE BULBWIN: ")
                print ("                    " + str(type.__str__(self.bulbWin)))
                print
                print

            self.index += 1



    # Como no tiene memoria, apagamos y guardamos el estado apagado
        if self.bulbTV is not None:
            self.bulbTV.set_power(False)
            self.stateBulbTV = False
            print (" ======= BULB TV =======")
            if self.stateBulbTV:
                print ("STATE: ON")
            else:
                print ("STATE: OFF")
            print ("MAC: " + self.bulbTV.mac_addr)
            print ("IP:  " + self.bulbTV.ip_addr)
            print

        if self.bulbWin is not None:
            self.bulbWin.set_power(False)
            self.stateBulbWin = False
            print (" ======= BULB WIN =======")
            if self.stateBulbWin:
                print ("STATE: ON")
            else:
                print ("STATE: OFF")
            print ("MAC: " + self.bulbWin.mac_addr)
            print ("IP:  " + self.bulbWin.ip_addr)
            print

        time.sleep(2)

    #############################
    #          TOPICS           #
    #############################
        #
        #
        #
        # Cambiar la llamada a metodos por self.metodo()
        self.topics = {"acho/lights/on/all": {"command": self.bulb_all_on, "text": "encendiendo luces"},
                       "acho/lights/off/all": {"command": self.bulb_all_off, "text": "apagando luces"},
                       "acho/lights/on/tv": {"command": self.bulb_tv_on, "text": "encendiendo luz TV"},
                       "acho/lights/on/win": {"command": self.bulb_win_on, "text": "encendiendo luz ventana"},
                       "acho/lights/off/tv": {"command": self.bulb_tv_off, "text": "apagando luz TV"},
                       "acho/lights/off/win": {"command": self.bulb_win_off, "text": "apagando luz ventana"},
                       "acho/lights/brightnessdown/tv": {"command": self.less_bright_bulbTV, "text": "bajando brillo en luz TV"},
                       "acho/lights/brightnessup/tv": {"command": self.more_bright_bulbTV, "text": "subiendo brillo TV"},
                       "acho/lights/brightnessdown/win": {"command": self.less_bright_bulbWin, "text": "bajando brillo ventana"},
                       "acho/lights/brightnessup/win": {"command": self.more_bright_bulbWin, "text": "subiendo brillo ventana"},
                       "acho/lights/brightnessdown/all": {"command": self.less_bright_all, "text": "bajando brillo luces"},
                       "acho/lights/brightnessup/all": {"command": self.more_bright_all, "text": "subiendo brillo luces"}}

    # #PARA PUBLICAR
    # self.topics_publicar = {
    #     "acho/lights/BulbTV/power": {"command": get_state_bulbTV(), "text": ""},
    #     "acho/lights/BulbWin/power": {"command": get_state_bulbWin(), "text": ""}
    # }

##################################################
#                GET PARAMETERS                  #
##################################################

    def get_color(self, light):
        index = 0
        while index < self.num_lights:
            if light.mac_addr == self.devices[index].mac_addr:
                return light.get_color()[0]
            index += 1

    def get_intensity(self, light):
        index = 0
        while index < self.num_lights:
            if light.mac_addr == self.devices[index].mac_addr:
                return light.get_color()[1]
            index += 1

    def get_brightness(self, light):
        index = 0
        while index < self.num_lights:
            if light.mac_addr == self.devices[index].mac_addr:
                return light.get_color()[2]
            index += 1

    def get_warm(self, light):
        index = 0
        while index < self.num_lights:
            if light.mac_addr == self.devices[index].mac_addr:
                return light.get_color()[3]
            index += 1

    def get_state_bulbTV(self):
        if self.bulbTV is not None:
            return self.stateBulbTV

    def get_state_bulbWin(self):
        if self.bulbWin is not None:
            return self.stateBulbWin


##################################################
#                SET PARAMETERS                  #
##################################################

    def set_color(self, light, new_color):
        index = 0
        while index < self.num_lights:
            if light.mac_addr == self.devices[index].mac_addr:
                light.set_color()[0] = new_color
            index += 1

    def set_intensity(self, light, new_intensity):
        index = 0
        while index < self.num_lights:
            if light.mac_addr == self.devices[index].mac_addr:
                light.get_color()[1] = new_intensity
            index += 1

    def set_brightness(self, light, new_bright):
        index = 0
        while index < self.num_lights:
            if light.mac_addr == self.devices[index].mac_addr:
                light.get_color()[2] = new_bright

            index += 1

    def set_warm(self, light, new_warm):
        index = 0
        while index < self.num_lights:
            if light.mac_addr == self.devices[index].mac_addr:
                light.get_color()[3] = new_warm
            index += 1

    def set_state_bulbTV(self, new_state):

        self.stateBulbTV = new_state
        ret = self.client.publish("acho/lights/bulbTV/power", new_state)

    def set_state_bulbWin(self, new_state):

        self.stateBulbWin = new_state
        ret = self.client.publish("acho/lights/bulbTV/power", new_state)


##################################################
#                 MODIFY LIGHTS                  #
##################################################

#             SUM AND REST QUANTITY

    '''
        Modify the color of the light with the given quantity
        Gets this value into bulb.get_color()[0]
    RED   ---> 0 or 360  ---> 0 or 65280   
    GREEN --->      120  --->      21760
    BLUE  --->      240  --->      43520  
    '''

    def modify_color(self, light, quantity):
        index = 0
        while index < self.num_lights:
            if light.mac_addr == self.devices[index].mac_addr:
                light.get_color()[0] = light.get_color()[0] + quantity
            index += 1

    '''
        Modify the intensity of the color
        Gets this value into bulb.get_color()[1] 
    MIN --->     0
    MAX ---> 60292  
    '''

    def modify_intensity(self, light, quantity):
        index = 0
        while index < self.num_lights:
            if light.mac_addr == self.devices[index].mac_addr:
                light.get_color()[1] = light.get_color()[1] + quantity
            index += 1

    '''
        Modify the brightness of the bulb with the given quantity
        Gets this parameter into bulb.get_color()[2]
    MIN --->  1966 --->   1%
    MAX ---> 65535 ---> 100%
    '''

    def modify_brightness(self, light, quantity, less):
        index = 0
        while index < self.num_lights:
            if light.mac_addr == self.devices[index].mac_addr:
                colorArray = list(light.get_color())
                if less is True:
                    bright = colorArray[2]
                    total = bright - quantity
                    colorArray[2] = total
                    light.set_color(colorArray)

                if less is False:
                    bright = colorArray[2]
                    total = bright + quantity
                    colorArray[2] = total
                    light.set_color(colorArray)

                if light.mac_addr == self.bulbTV.mac_addr:
                    ret = self.client.publish("acho/lights/bulbTV/brightness", total)
                else:
                    ret = self.client.publish("acho/lights/bulbWin/brightness", total)

            index += 1

    '''
        Modify from cold light to warm light with the given quantity
        Gets this value into bulb.get_color()[3]
    MIN --->    2700 K ---> Warmest Light
    MAX --->    6500 K ---> Coolest light
    '''

    def modify_warm(self, light, quantity):
        index = 0
        while index < self.num_lights:
            if light.mac_addr == self.devices[index].mac_addr:
                light.get_color()[3] = light.get_color()[3] + quantity
            index += 1


##################################################
##################################################
#              METHODS DEFINITION                #
##################################################
##################################################

##################################################
#                    TURN ON                     #
##################################################

# Enciende la bombilla de la TV

    def bulb_tv_on(self):
        if self.bulbTV is not None:
            print ("Encendiendo luz cerca TV")
            self.bulbTV.set_power(True)
            self.stateBulbTV = True

            if self.stateBulbTV:
                ret = self.client.publish("acho/lights/BulbTV/power", True)
                print ("Encendida")
                print


# Enciende la bombilla de la ventana

    def bulb_win_on(self):
        if self.bulbWin is not None:
            print ("Encendiendo luz cerca ventana")
            self.bulbWin.set_power(True)
            self.stateBulbWin = True

            if self.stateBulbWin:
                ret = self.client.publish("acho/lights/BulbWin/power", True)
                print ("Encendida")
                print


    # Enciende todas las bombillas

    def bulb_all_on(self):
        print ("Encendiendo todas las luces")
        if self.bulbTV is not None:
            self.bulb_tv_on()
        if self.bulbWin is not None:
            self.bulb_win_on()


    ##################################################
    #                   TURN OFF                     #
    ##################################################

    # Apaga la bombilla de la TV

    def bulb_tv_off(self):
        print ("Apagando luz cerca TV")
        self.bulbTV.set_power(False)
        self.stateBulbTV = False

        if not self.stateBulbTV:
            ret = self.client.publish("acho/lights/BulbTV/power", False)
            print ("Apagada")
            print


    # Apaga la bombilla de la ventana

    def bulb_win_off(self):
        print ("Apagando luz cerca ventana")
        self.bulbWin.set_power(False)
        self.stateBulbWin = False

        if not self.stateBulbTV:
            ret = self.client.publish("acho/lights/BulbTV/power", False)
            print ("Apagada")
            print


    # Apaga todas las luces

    def bulb_all_off(self):
        print ("Apagando todas las luces")
        self.bulb_tv_off()
        self.bulb_win_off()


    # 20% LESS -- QUANTITY = -12400

    def less_bright_bulbTV(self):
        if self.bulbTV is not None:
            brillo = int(self.bulbTV.get_color()[2])
            total = brillo - 12400
            if total > 0:
                less = True
                self.modify_brightness(self.bulbTV, 12400, less)
            else:
                print ("Ha llegado al brillo minimo")

    # 20% MORE -- QUANTITY = +12400

    def more_bright_bulbTV(self):
        if self.bulbTV is not None:
            brillo = int(self.bulbTV.get_color()[2])
            total = brillo + 12400
            if total < 65535:
                less = False
                self.modify_brightness(self.bulbTV, 12400, less)
            else:
                print("Ha llegado al brillo maximo")


    # 20% LESS -- QUANTITY = -12400

    def less_bright_bulbWin(self):
        if self.bulbWin is not None:
            brillo = int(self.bulbWin.get_color()[2])
            total = brillo - 12400
            if total > 0:
                less = True
                self.modify_brightness(self.bulbWin, 12400, less)
            else:
                print ("Ha llegado al brillo minimo")

    # 20% MORE -- QUANTITY = +12400

    def more_bright_bulbWin(self):
        if self.bulbWin is not None:
            brillo = int(self.bulbWin.get_color()[2])
            total = brillo + 12400
            if total < 65535:
                less = False
                self.modify_brightness(self.bulbWin, 12400, less)
            else:
                print ("Ha llegado al brillo maximo")

    def less_bright_all(self):
        self.less_bright_bulbTV()
        self.less_bright_bulbWin()

    def more_bright_all(self):
        self.more_bright_bulbTV()
        self.more_bright_bulbWin()

#############################
#            MQTT           #
#############################
    def on__message(self, client, userdata, msg):
        print ("topic", msg.topic)
        if msg.topic in self.topics:
            t = self.topics[msg.topic]
            # client.publish("acho/tts", t["text"])
            print (t)
            t["command"]()




#
#
# # def discover():
# #     global self.num_lights
# #     global lifx
# #     global config
# #     global self.devices
# #
# #     print("\n {} luces encontradas \n".format(len(self.devices)))
# #     for d in self.devices:
# #         print(d)
# #         # i += 1
# #         # aux_mac = config.get('bombilla_{}'.format(i), 'mac')
# #         # if aux_mac != d.get_mac_addr():
# #         #     d.set_label("bombilla_{}".format(i))
# #         #     config.add_section('bombilla_{}'.format(i))
# #         #     config.set('bombilla_{}'.format(i), 'mac', d.get_mac_addr())
# #         #     with open('bulbs.cfg', 'wb') as configfile:
# #         #         config.write(configfile)
#
#
#
#
#
# # FROM 0 to 65535
# def modify_B(light, quantity):
#     global self.num_lights
#     global lifx
#     global config
#     global self.devices
#     lifx = LifxLAN(self.num_lights)
#     self.devices = lifx.get_lights()
#     for d in self.devices:
#         if d.get_mac_addr() == light:
#             bombilla = d
#             break
#     ogcolor = bombilla.get_color()
#     if ogcolor[2] <= quantity:
#         for i in range(ogcolor[2], quantity, 100):
#             color = [ogcolor[0], ogcolor[1], i, ogcolor[3]]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#     elif ogcolor[2] > quantity:
#         for i in range(ogcolor[2], quantity, -100):
#             color = [ogcolor[0], ogcolor[1], i, ogcolor[3]]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#
#
# # FROM 2500 to 9000
# def modify_K(light, quantity):
#     global self.num_lights
#     global lifx
#     global config
#     global self.devices
#     lifx = LifxLAN(self.num_lights)
#     self.devices = lifx.get_lights()
#     for d in self.devices:
#         if d.get_mac_addr() == light:
#             bombilla = d
#             break
#     ogcolor = bombilla.get_color()
#     if ogcolor[3] <= quantity:
#         for i in range(ogcolor[3], quantity, 100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#     elif ogcolor[3] > quantity:
#         for i in range(ogcolor[3], quantity, -100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#
#
# def control_percentual_vble_K(light):
#
#     ogcolor = bombilla.get_color()
#     quantity = ogcolor[3] * 0.1
#     if ogcolor[3] <= quantity:
#         for i in range(ogcolor[3], quantity, 100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#     elif ogcolor[3] > quantity:
#         for i in range(ogcolor[3], quantity, -100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#
#
# def control_percentual_total_K(light):
#     global self.num_lights
#     global lifx
#     global config
#     global self.devices
#     lifx = LifxLAN(self.num_lights)
#     self.devices = lifx.get_lights()
#     for d in self.devices:
#         if d.get_mac_addr() == light:
#             bombilla = d
#             break
#     ogcolor = bombilla.get_color()
#     if ogcolor[3] <= 900:
#         for i in range(ogcolor[3], 900, 100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#     elif ogcolor[3] > 900:
#         for i in range(ogcolor[3], 900, -100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#
#
# def control_percentual_vble_B(light):
#     global self.num_lights
#     global lifx
#     global config
#     global self.devices
#     lifx = LifxLAN(self.num_lights)
#     self.devices = lifx.get_lights()
#     for d in self.devices:
#         if d.get_mac_addr() == light:
#             bombilla = d
#             break
#     ogcolor = bombilla.get_color()
#     quantity = ogcolor[2] * 0.1
#     if ogcolor[2] <= quantity:
#         for i in range(ogcolor[3], quantity, 100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#     elif ogcolor[2] > quantity:
#         for i in range(ogcolor[3], quantity, -100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#
#
# def control_percentual_total_B(light):
#     global self.num_lights
#     global lifx
#     global config
#     global self.devices
#     lifx = LifxLAN(self.num_lights)
#     self.devices = lifx.get_lights()
#     for d in self.devices:
#         if d.get_mac_addr() == light:
#             bombilla = d
#
#     ogcolor = bombilla.get_color()
#     if ogcolor[2] <= 3650:
#         for i in range(ogcolor[3], 3650, 100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())
#     elif ogcolor[2] > 3650:
#         for i in range(ogcolor[3], 3650, -100):
#             color = [ogcolor[0], ogcolor[1], ogcolor[2], i]
#             bombilla.set_color(color)
#             print (bombilla.get_color())

#



