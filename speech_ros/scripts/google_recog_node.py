#!/usr/bin/env python3

#Just kill me the code is so messy.I'm litterally combine pyaudio and pocketsphinx which is hard af
import os
import re
import yaml
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

rospack=rospkg.RosPack()
    

class Recognizer_Node:
    def __init__(self):
        rospy.init_node('speech_recog_node')
        rospy.logwarn('Setting up')
        self.srv=rospy.Service('recognizer/start', SpeechRecog, self.start_recog_callback )
        #It named recognizer but It's only good at listening.
        #adjust ambient noise for listener
        self._listener=sr.Recognizer()
        self._ready=False

        #self._listener.energy_threshold=2364
        #self._listener.pause_threshold = 0.8
        rospy.logwarn('Adjusting listener for ambient noise...')
        with sr.Microphone() as source:
            self._listener.adjust_for_ambient_noise(source,duration=1)
        self._listener.pause_threshold = 1.0
        rospy.logwarn('Listener Adjusted')
        rospy.loginfo(f'Energy threshold => {self._listener.energy_threshold}')
        #self._listener.dynamic_energy_threshold = True
        #self._listener.dynamic_energy_adjustment_damping = 0.15
        #self._listener.dynamic_energy_adjustment_ratio = 1.5
        #self._listener.pause_threshold = 0.8
        #energy_threshold=>1300

        self._ready=True

            
    def start_recog_callback(self,req):
        rate=rospy.Rate(30)
        while self._ready==False:
            rate.sleep()
        rospy.loginfo(f'Received request.Starting speech recognition....')

        with sr.Microphone() as source:
            audio = self._listener.listen(source,timeout=10,phrase_time_limit=17)
        
        rospy.loginfo(f'Decoding....')

        try:
            sentence=self._listener.recognize_google(audio)
        except sr.UnknownValueError:
            sentence='null'
        except sr.RequestError as e:
            sentence='null'
        sentence_o=sentence.lower()
        sentence=self.sentence_mapping(sentence_o)
        rospy.loginfo(f'Response to client with "{sentence}" , {sentence_o}')
        return SpeechRecogResponse(sentence)
    def sentence_mapping(self,s):
        config_path=rospack.get_path('speech_ros')+'/config/sentence-mapper'
        data=yaml.load(open(config_path+'/google-GPSR.yaml').read())
        for b,a in data.items():
            for ai in a:
                s=s.replace(ai,b)
        return s

if __name__=='__main__':
    rospy.init_node('speech_recog_node')
    r_node=Recognizer_Node()
    rospy.spin()