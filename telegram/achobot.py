# -*- coding: utf-8 -*-
import telebot  # Librería de la API del bot.
from telebot import types  # Tipos para la API del bot.
import time  # Librería para hacer que el programa que controla el bot no se acabe.

#TOKEN = '186444357:AAFEmRGWuU6dj493QkS99gRPHdxGdEQaGeU'
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
    markup.row('encender', 'apagar')
    markup.row('retroceder')
    bot.send_message(cid, "Elija la opcion que desea, o retroceder para volver atras", None, None, markup)


def retroceder(cid):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False)
    markup.row('persiana')
    markup.row('bombilla')
    markup.row('television')
    bot.send_message(cid, "Elija la opcion que desea", None, None, markup)




def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            cid = m.chat.id
            print "[" + str(cid) + "]: " + m.text

            if m.text.find("persiana") != -1:
                funpersiana(cid)

            elif m.text.find("bombilla") != -1:
                funbombilla(cid)

            elif m.text.find("television") != -1:
                funtelevision(cid)

            elif m.text.find("retroceder") != -1:
                retroceder(cid)
            elif m.text.find("subir")  != -1:
                print "Curl subir la persiana"

            elif m.text.find("bajar")  != -1:
                print "curl bajar la persiana"

            elif m.text.find("parar")  != -1:
                print "curl parar la persiana"

            elif m.text.find("encender")  != -1:
                print "curl encender tele"

            elif m.text.find("apagar")  != -1:
                print "curl apagar tele"


bot.set_update_listener(listener)

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    retroceder(cid)

print "polling.."

bot.polling(none_stop=True)
