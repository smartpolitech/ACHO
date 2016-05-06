# -*- coding: utf-8 -*-
import telebot  # Librería de la API del bot.
from telebot import types  # Tipos para la API del bot.
import time, sys  # Librería para hacer que el programa que controla el bot no se acabe.
import paho.mqtt.client as mqtt
#import requests
import urllib2
import urllib
import os

client = mqtt.Client()
client.connect("localhost", 1883, 60)
print "Connected to Mosquitto broker"

TOKEN = '205601802:AAHkJYiNdXXG1p5XPOWqq5l_L334H-VJHzc'

bot = telebot.TeleBot(TOKEN)

def funpersiana(cid):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
    markup.row('subir','parar', 'bajar')
    markup.row('subir seccion','bajar seccion')
    markup.row('retroceder')
    bot.send_message(cid, "Elija la opcion que desea, o retroceder para volver atras", None, None, markup)

def funbombilla(cid):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
    markup.row('encender','apagar')
    markup.row('retroceder')
    bot.send_message(cid, "Elija la opcion que desea, o retroceder para volver atras", None, None, markup)

def funtelevision(cid):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
    markup.row('power')
    markup.row('retroceder')
    bot.send_message(cid, "Elija la opcion que desea, o retroceder para volver atras", None, None, markup)


def retroceder(cid):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
    markup.row('persiana')
    markup.row('bombilla')
    markup.row('television')
    bot.send_message(cid, "Elija la opcion que desea", None, None, markup)

def publish(topic):
	client.reconnect()
	client.publish(topic, "")

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
	for m in messages:
		if m.content_type == 'text':
			cid = m.chat.id
			print "[" + str(cid) + "]: " + m.text
			t = topics[m.text]
			if t["params"] == "cid":
				t["command"](cid)
			else:
				#t["command"](t["params"])
				client.publish("acho/nlp", t["params"])
				print "sending to nlp", t["params"]
				
		elif m.content_type == 'voice':
			print "voice message"
			d = dateStringFromTimestamp(m.date)
			file_path = 'audios/' + d + '_voice.ogg'
			file_info = bot.get_file(m.voice.file_id)
			url = 'https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path)
			req = urllib2.Request(url)
			
			#da error al crear la url!!!!
			
			response = urllib2.urlopen(req)
			print response
			#TODO: check response
			audioFile = response.read()
			with open(file_path, 'w') as outfile:
				outfile.write(audioFile)
			file_path_out = file_path[:-4]+'.wav'
			command = "ffmpeg -loglevel quiet -i "+os.getcwd()+"/"+file_path+" "+os.getcwd()+"/"+file_path_out
			os.system(command)
			print "publishing", os.getcwd()+"/"+file_path_out
			client.publish('acho/asr/wavfile',os.getcwd()+"/"+file_path_out)
			
	
			

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    retroceder(cid)

print "polling.."

#bot.notifyOnMessage(self.handle)
bot.set_update_listener(listener)

while True:
	try:
		bot.polling(none_stop=False)
	except:
		print "Unexpected error:", sys.exc_info()[0]
    	time.sleep(10)

