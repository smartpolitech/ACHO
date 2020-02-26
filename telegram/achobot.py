'''Bot de Telegram que permanece a la espera de que alguien le envie un comando (texto o un audio) por Telegram. Una vez lo recibe:
    - si es texto lo envia al NLP para que procese el texto en busca de lo que se desea hacer.
    - si es audio (.wav) lo envia al ASR para que obtenga el texto y este sea enviado al NLP de la misma forma.
'''

import telebot            # Librería de la API del bot.
from telebot import types  # Tipos para la API del bot.
import time, sys
import paho.mqtt.client as mqtt
#import requests
import urllib
import urllib.request
import shutil
import tempfile
import os

DEBUG = True
cid = 0

print("[✓] Iniciando bot...")

##################         MQTT         ###################

client = mqtt.Client()
try:
    client.connect("salareuniones.local", 1883, 60)
except:
    print("[!] No se puede conectar con el broker: \n\n ", sys.exc_info()[0])
    sys.exit()
print("[✓] Conexion con el broker MQTT con éxito.")

TOKEN = "205601802:AAHkJYiNdXXG1p5XPOWqq5l_L334H-VJHzc"
bot = telebot.TeleBot(TOKEN)
print("[✓] Conexion del bot con Telegram con éxito.")


##################    Metodos del Bot    ###################
def funpersiana(cid):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
    markup.row('subir','parar', 'bajar')
    markup.row('subir seccion','bajar seccion')
    markup.row('retroceder')
    bot.send_message(cid, "Elije que deseas hacer, o retroceder para volver atras", None, None, markup)

def funbombilla(cid):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
    markup.row('encender','apagar')
    markup.row('retroceder')
    bot.send_message(cid, "Elije que deseas hacer, o retroceder para volver atras", None, None, markup)

def funtelevision(cid):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
    markup.row('power')
    markup.row('retroceder')
    bot.send_message(cid, "Elije que deseas hacer, o retroceder para volver atras", None, None, markup)


def retroceder(cid):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
    markup.row('persiana')
    markup.row('bombilla')
    markup.row('television')
    bot.send_message(cid, "Elije que deseas hacer", None, None, markup)

def publish(topic):
	client.reconnect()
	client.publish(topic, "")
#estos topics se usaban para saber si el comando recibido por texto era valido o no,pero ahora se envia el texto directamente al NPL y este ya dira si es valido o no.
topics = {"persiana":  { "command": funpersiana, "params": "cid", "text": "" },
		  "bombilla":  { "command": funbombilla, "params": "cid",  "text": "" },
  		  "television":{ "command": funtelevision, "params": "cid", "text" : "" },
  		  "retroceder":{ "command": retroceder, "params": "cid", "text" : "" },
		  "subir seccion": { "command": publish, "params": "subir seccion persiana","text":"" },
		  "subir": 	   { "command": publish, "params": "subir persiana", "text" : "" },
		  "bajar seccion":{"command":publish, "params":"bajar seccion persiana","text":"" },
		  "bajar": 	   { "command": publish, "params": "bajar persiana", "text" : "" },
  		  "parar": 	   { "command": publish, "params": "parar persiana", "text" : "" },
		  "power": 	   { "command": publish, "params": "encender television", "text" : "" },
		  "encender":  { "command": publish, "params": "encender luces", "text" : "" },
		  "apagar":    { "command": publish, "params": "apagar luces", "text" : "" }
		  }

def dateStringFromTimestamp(t):
    return str(time.strftime("%Y%m%d%H%M%S", time.localtime(float(t))))

def listener(messages):
    global cid
    for m in messages:
        if m.content_type == 'text':
            if m.text != "/start":
                if m.text in topics:
                    cid = m.chat.id
                    print("[✓] Detectado comando de Texto: " + m.text)
                    t = topics[m.text]
                    if t["params"] == "cid":
                        t["command"](cid)
                    else:
                        client.reconnect()
                        client.publish("acho/nlp", t["params"])
                        print("[✓] Enviando comando de Texto al NPL.", t["params"])
                        #enviamos al tts (pasa el texto a voz y la reproduce) el comando
                        client.reconnect()
                        client.publish("acho/tts", t["params"])
                        if DEBUG: print("[✓] Enviando comando de Texto al TTS.", t["params"])

                else:
                    #si el comando NO es un comando bien-conocido (los de las estructura topic), entonces se lo pasamos al NPL directamente
                    client.reconnect()
                    client.publish("acho/nlp", m.text)
                    print("[✓] Enviando comando de Texto al NLP.", m.text)
                    #enviamos al tts (pasa el texto a voz y la reproduce) el comando
                    client.reconnect()
                    client.publish("acho/tts", str(m.text + " recibido desde Telegram."))
                    if DEBUG: print("[✓] Enviando comando de Texto al TTS.", m.text)

        elif m.content_type == 'voice':
            print("[✓] Detectado mensaje de voz.")
            #obtenemos el timestamp para ponerlo en el nombre del archivo de audio
            d = dateStringFromTimestamp(m.date)
            #creamos la ruta del archivo de audio, la cual estara en una carpeta en el directorio de este script
            file_path = "audios/" + d + "_voice.oga"
            #creamos la url para obtener el audio de los servidores de Telegram
            file_info = bot.get_file(m.voice.file_id)
            url = "https://api.telegram.org/file/bot{0}/{1}".format(TOKEN, file_info.file_path)

            #conectamos con la URL pidiendo el audio
            if DEBUG: print("URL del audio ---------->  " + str(url))
            #obtenemos la respuesta de la URL
            response = urllib.request.urlopen(url)
            if DEBUG: print("respuesta de URL ---------->  " + str(response))
            #Obtenemos los datos (bytes) de la respuesta de la URL
            audioFile = response.read()
            #y los escribimos en el archivo de audio que abrimos al principio
            with open(file_path, 'wb') as outfile:
                outfile.write(audioFile)

            #tranformamos el formato del archivo de .oga a .wav
            file_path_out = file_path[:-4]+".wav"
            command = "ffmpeg -loglevel quiet -i "+os.getcwd()+"/"+file_path+" "+os.getcwd()+"/"+file_path_out
            os.system(command)
            if DEBUG: print("[✓] Publicando audio en el topic MQTT...")
            if DEBUG: print("Ruta del archivo de audio ->> ",os.getcwd()+"/"+file_path_out)
            #y publicamos en el topic mqtt "acho/asr/wavfile" de "salareuniones.local" la ruta del archivo de audio.
            client.reconnect()
            client.publish("acho/asr/wavfile",os.getcwd()+"/"+file_path_out)
            print("[✓] Audio enviado a ACHO correctamente.")
            bot.send_message(cid, "He recibido tu audio. Enseguida lo escucho ;)", None, None, None)


			

@bot.message_handler(commands=['start'])
def command_start(m):
    global cid
    cid = m.chat.id
    bot.send_message(cid, "¡Hola! Mi nombre es ACHO.", None, None, None)
    retroceder(cid)
    print("[✓] Bot iniciando NUEVA conversacion por Telegram.")


#bot.notifyOnMessage(self.handle)
bot.set_update_listener(listener)

print("[✓] Bot configurado con éxito.")





##################          MAIN          ###################

print("[✓] Bot Iniciado.\n")
while True:
    time.sleep(10)
    print(".", end="")
    try:
        bot.polling(none_stop=True)
    except:
        if DEBUG:
            print("##################################################################################################")
            print()
            print("[!] Error Inesperado :(  -> ", sys.exc_info()[0])
            print()
            print("##################################################################################################")

