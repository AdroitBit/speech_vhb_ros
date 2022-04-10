#!/usr/bin/env python3

#from vosk import Model, KaldiRecognizer, SetLogLevel
import vosk
import sys
import os
import wave
import speech_recognition as sr
import json

vosk.SetLogLevel(0)






#listen to microphone using speech_recognition


#Load VOSK model
print("Loading the vosk model")
model = vosk.Model("../models/vosk-model-en-us-0.22")
#model = Model("../models/vosk-model-small-en-us-0.15")

def listen():
    print("Listening")
    with sr.Microphone() as source:
        audio = listener.listen(source,timeout=10,phrase_time_limit=15)

    data=audio.get_wav_data(convert_rate=16000,convert_width=2)

    f=open('tmp.wav','wb')
    f.write(data)
    f.close()

    print("Vosk Recognizing")
    rec = vosk.KaldiRecognizer(model, 16000)
    rec.AcceptWaveform(data)
    text=json.loads(rec.Result())['text']
    print('Big vosk model think you say "{}"'.format(text))
    return text

def speak(msg):
    os.system('pico2wave -l en-US -w tmp.wav "{}"'.format(msg))
    os.system('aplay tmp.wav')



while True:
    speak(listen())