#!/usr/bin/env python3

#Not ros node pyaudio need tuning
import os
import re
import rospy
import rospkg
from speech_ros.srv import SpeechRecog,SpeechRecogResponse
from std_msgs.msg import Empty
from std_msgs.msg import String

import speech_recognition as sr
from pocketsphinx import AudioFile,Pocketsphinx,Decoder,DefaultConfig
import os
import signal
import time
import statistics

rospack=rospkg.RosPack()

def tune():
    r=sr.Recognizer()
    r.energy_threshold=2364
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=5)
    r.dynamic_energy_threshold=False
    d={
        'energy_threshold' : r.energy_threshold,
        'dynamic_energy_threshold' : r.dynamic_energy_threshold,
        'dynamic_energy_adjustment_damping' : r.dynamic_energy_adjustment_damping,
        #'dynamic_energy_adjustment_ratio' : r.dynamic_energy_adjustment_ratio,
        'pause_threshold' : r.pause_threshold,
    }
    for k,v in d.items():
        print(f'{k:<20} => {v:<20}')
    return d


if __name__=='__main__':
    tune_values=[]
    for nround in range(1,11):
        #rospy.loginfo(f'Tuning round {nround}')
        print(f'#### Tuning round {nround} ####')
        tune_values.append(tune())
    
    print(f'#### average Tuning result ####')
    tune_value={}
    for di in tune_values:
        for k,v in di.items():
            tune_value.setdefault(k,[])
            tune_value[k].append(v)
            
    for k,v in tune_value.items():
        tune_value[k]=statistics.mean(v)
        print(k,tune_value[k])
        
    print("##### Test the sound #####")

    with sr.Microphone() as source:
        audio=r.listen(source,timeout=10,phrase_time_limit=10)
    f=open('/tmp/speech.raw','wb')
    f.write(audio.get_raw_data(convert_rate=16000,convert_width=2))
    f.close()

    f=open('/tmp/speech.wav','wb')
    f.write(audio.get_wav_data(convert_rate=16000,convert_width=2))
    f.close()