#!/usr/bin/env python3

#This file will print the output of the speech recognition result
#So ROS noetic node can read and get the result
from pocketsphinx import LiveSpeech
import os
import signal
import rospkg
rospack = rospkg.RosPack()
#pocketsphinx model path
model_path=rospack.get_path('speech_ros')+'/model'

def timeout_handler(signum, frame):
   raise TimeoutError("end of time")
def start_recog():
    global model_path
    try:
        speech=LiveSpeech(
            verbose=False,
            sampling_rate=16000,
            buffer_size=2048,
            no_search=False,
            full_utt=False,
            hmm=os.path.join(model_path, 'en-us'),
            lm=os.path.join(model_path, 'en-us.lm.bin'),
            #dic=os.path.join(model_path, 'KU_Robocup-en-us.dict')
            dic=os.path.join(model_path, 'movement-en-us.dict')
        )
        for phrase in speech:
            phrase=str(phrase)
            if len(phrase)==0 or phrase=='':
                return 'null'
            else:
                return phrase
    except TimeoutError as e:
        if str(e)=='end of time':
            return 'null'



signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(10)


#Here it's just print out the result
print(start_recog())