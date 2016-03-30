#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, io, json, pyaudio, time, sys 
import paho.mqtt.publish as mqttClient

try:
    import apiai
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
    import apiai

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 6

CLIENT_ACCESS_TOKEN = 'c4c14424cdd5488f9183de8856cd83ea'
SUBSCRIPTION_KEY = 'c2a6c4eb-2961-4658-be52-fc75822d2fa7' 

def main():
    resampler = apiai.Resampler(source_samplerate=RATE)
    vad = apiai.VAD()
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN, SUBSCRIPTION_KEY)
    request = ai.voice_request()
    request.lang = 'es' # optional, default value equal 'en'

    def callback(in_data, frame_count, time_info, status):
        frames, data = resampler.resample(in_data, frame_count)
        state = vad.processFrame(frames)
        request.send(data)

        if (state == 1):
            return in_data, pyaudio.paContinue
        else:
            return in_data, pyaudio.paComplete

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS, 
                    rate=RATE, 
                    input=True,
                    output=False,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)

    stream.start_stream()

    print ("\n ACHO DI ALGO!!!!")

    try:
        while stream.is_active():
            time.sleep(0.5)
    except Exception:
        raise e
    except KeyboardInterrupt:
        pass

    stream.stop_stream()
    stream.close()
    p.terminate()
    
    response = request.getresponse()
    
    data=response.read()
    print data
    
    data1=data.replace('/n','')
    data1=data1.replace(' ','')
    data1=json.loads(data1)
    accion = data1["result"]["resolvedQuery"]
    
    
    #m1=data.find("resolvedQuery")
    #m2=data[m1:].find(":")
    ##print m1,m2
    #m1+=m2
    ##print m1,m2
    #m2=data[m1:].find('"')
    ##print m1,m2
    #m1+=m2+1
    ##print m1,m2
    #m3=data[m1:].find('"')
	
    ##print m1,m2,m3
    #accion=data[m1:m1+m3]
    
    if accion != '':
        print ("\n Usted ha dicho...\n")
	print accion
	mqttClient.single("acho/blind/up","1")
    else:
        print ("\n ¿COMORL? Repita acción porfavor \n")
        
    #print(data[m1:m1+m3])
    

if __name__ == '__main__':
    main()
