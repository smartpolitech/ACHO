#!/usr/bin/env python27
# NOTE: this example requires PyAudio because it uses the Microphone class
import os
from gtts import gTTS
from pydub import AudioSegment
import speech_recognition as sr
from subprocess import call

try:
  while True:
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
	print("   Habla en ingles! \n")
	audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
	# for testing purposes, we're just using the default API key
	# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
	# instead of `r.recognize_google(audio)`
	respuesta = r.recognize_google(audio)
	print("    Google Speech Recognition DICE QUE HAS DICHO \n \n" + respuesta + "\n")
	if "up" in respuesta:
	  tts= gTTS(text='Subiendo la persiana', lang='es')
	  tts.save("prueba.mp3")
	  song = AudioSegment.from_mp3("prueba.mp3")
	  song.export("final.wav", format ="wav")
	  os.system("aplay final.wav")
	  call(["curl", "http://root:opticalflow@158.49.247.178/arduino/command/blindup"])    
	if "down" in respuesta:
	  tts= gTTS(text='Bajando la persiana', lang='es')
	  tts.save("prueba.mp3")
	  song = AudioSegment.from_mp3("prueba.mp3")
	  song.export("final.wav", format ="wav")
	  os.system("aplay final.wav")
	  call(["curl", "http://root:opticalflow@158.49.247.178/arduino/command/blinddown"])    
	if "stop" in respuesta:
	  tts= gTTS(text='parando la persiana', lang='es')
	  tts.save("prueba.mp3")
	  song = AudioSegment.from_mp3("prueba.mp3")
	  song.export("final.wav", format ="wav")
	  os.system("aplay final.wav")
	  call(["curl", "http://root:opticalflow@158.49.247.178/arduino/command/blindstop"])    
	if "power" in respuesta:
	  tts= gTTS(text='Bienvenido a la sala', lang='es')
	  tts.save("prueba.mp3")
	  song = AudioSegment.from_mp3("prueba.mp3")
	  song.export("final.wav", format ="wav")
	  os.system("aplay final.wav")
	  call(["curl", "http://root:opticalflow@158.49.247.178/arduino/command/power"])    
	if "one" in respuesta:
	  call(["curl", "http://root:opticalflow@158.49.247.178/arduino/command/one"])    
	if "exit" in respuesta:
	  tts= gTTS(text='Hasta luego!', lang='es')
	  tts.save("prueba.mp3")
	  song = AudioSegment.from_mp3("prueba.mp3")
	  song.export("final.wav", format ="wav")
	  os.system("aplay final.wav")
	  call(["curl", "http://root:opticalflow@158.49.247.178/arduino/command/exit"])    
	
    except sr.UnknownValueError:
	print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
	print("Could not request results from Google Speech Recognition service; {0}".format(e))
      
except KeyboardInterrupt:
  pass