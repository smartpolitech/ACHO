# -*- coding: utf-8 -*-
import telebot  # Librería de la API del bot.
#from telebot import types  # Tipos para la API del bot.
import time, sys  # Librería para hacer que el programa que controla el bot no se acabe.
import paho.mqtt.client as mqtt
import requests

client = mqtt.Client()
client.connect("localhost", 1883, 60)
print "Connected to Mosquitto broker"

TOKEN = '205601802:AAHkJYiNdXXG1p5XPOWqq5l_L334H-VJHzc'

bot = telebot.TeleBot(TOKEN)

def funpersiana(cid):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
    markup.row('subir', 'parar', 'bajar')
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
		  "subir": 	   { "command": publish, "params": "acho/blind/up", "text" : "" },
		  "bajar": 	   { "command": publish, "params": "acho/blind/down", "text" : "" },
  		  "parar": 	   { "command": publish, "params": "acho/blind/stop", "text" : "" },
		  "power": 	   { "command": publish, "params": "acho/tv/power", "text" : "" },
		  "encender":  { "command": publish, "params": "acho/lights/on/all", "text" : "" },
		  "apagar":    { "command": publish, "params": "acho/lights/off/all", "text" : "" }
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
				t["command"](t["params"])
		elif m.content_type == 'voice':
			d = dateStringFromTimestamp(m.date)
			file_path = d + '_voice.ogg'
			print file_path, m.voice.file_id
			file_info = bot.get_file(m.voice.file_id)
			print file_info
			print 'https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path)
			
			#fich = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
			fich = os.system('''curl requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))''')
			
			#bot.downloadFile(m.voice.file_id, file_path)
			#print m.voice.file_info.file_path
			os.system('')
			print m.voice.file_id
			client.publish('/acho/asr/wavfile', 'audio.wav')


bot.set_update_listener(listener)

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    retroceder(cid)

print "polling.."

#bot.notifyOnMessage(self.handle)

while True:
	try:
		bot.polling(none_stop=False)
	except:
		print "Unexpected error:", sys.exc_info()[0]
    	time.sleep(10)
	
