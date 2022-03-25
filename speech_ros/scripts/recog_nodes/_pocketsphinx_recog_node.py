#!/usr/bin/env python3

#This file is not intended to be run directly through ROS.
#This file is helper for speech_recog_srv
#Because in ros noetic there is a problem
from pocketsphinx import LiveSpeech
import os
import signal
import rospkg

rospack = rospkg.RosPack()

def timeout_handler(signum, frame):
   raise TimeoutError("end of time")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(10)


model_path=rospack.get_path('speech_reos')+'/model'

try:
    speech=LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm=os.path.join(model_path, 'en-us'),
        lm=os.path.join(model_path, 'en-us.lm.bin'),
        dic=os.path.join(model_path, 'KU_Robocup-en-us.dict')
    )
    for phrase in speech:
        phrase=str(phrase)
        if len(phrase)==0 or phrase=='':
            phrase="null"
            print(phrase)
        else:
            print(phrase,end='')
        break
except TimeoutError as e:
    if str(e)=='end of time':
        print('null')