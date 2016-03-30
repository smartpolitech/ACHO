# -*- coding: utf-8 -*-
import telebot # Librería de la API del bot.
from telebot import types # Tipos para la API del bot.
import time # Librería para hacer que el programa que controla el bot no se acabe.
import paho.mqtt.publish as mqttClient

TOKEN = '205601802:AAHkJYiNdXXG1p5XPOWqq5l_L334H-VJHzc'

bot = telebot.TeleBot(TOKEN)

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            cid = m.chat.id
            print "[" + str(cid) + "]: " + m.text

bot.set_update_listener(listener)


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
   
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
    markup.row('/subir')
    markup.row('/baja')
    markup.row('/parar')
    bot.send_message(cid, "Bienvenido al acho bot",None,None,markup)


@bot.message_handler(commands=['subir'])
def command_start(m):
    cid = m.chat.id
    bot.send_message(cid, "Bienvenido al acho bot")
    mqttClient.single("acho/blind/up", "0")

@bot.message_handler(commands=['baja'])
def command_start(m):
    cid = m.chat.id
    bot.send_message(cid, "Bajando persiana")
    mqttClient.single("acho/blind/down", "0")

@bot.message_handler(commands=['parar'])
def command_start(m):
    cid = m.chat.id
    bot.send_message(cid, "Parando persiana")
    mqttClient.single("acho/blind/stop", "0")
    

bot.polling(none_stop=True)
