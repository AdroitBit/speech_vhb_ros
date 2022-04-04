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
from pocketsphinx import AudioFile,Pocketsphinx,Decoder,DefaultConfig,LiveSpeech
import os
import signal
import time

rospack=rospkg.RosPack()
    

class Recognizer_Node:
    def __init__(self):
        rospy.init_node('speech_recog_node')
        rospy.logwarn('Setting up')
        self.srv=rospy.Service('recognizer/start', SpeechRecog, self.start_recog_callback)



        self._sentence=''

        self._switch_recog_on=False
    def loop(self):
        rate=rospy.Rate(30)
        while True:#Use loop because I can't use LiveSpeech() in service
            if self._switch_recog_on==True:
                try:
                    rospy.loginfo(f'Activating listener')
                    self._sentence=self.listen()
                except sr.WaitTimeoutError as e:
                    rospy.loginfo(f'Timeout : {e}')
                self._switch_recog_on=False
            rate.sleep()

            
    def start_recog_callback(self,req):
        rospy.loginfo(f'Received request.Starting speech recognition....')

        self._switch_recog_on=True
        rate=rospy.Rate(10)
        while self._switch_recog_on==True:
            rate.sleep()

        rospy.loginfo(f'Response to client with "{self._sentence}" , {len(self._sentence)}')
        return SpeechRecogResponse(self._sentence)

    def listen(self):
        for phrase in LiveSpeech():
            if phrase is None:
                return 'null'
            else:
                return self.sentence_mapping(str(phrase))
        return 'null'
    def sentence_mapping(self,s):
        config_path=rospack.get_path('speech_ros')+'/config/sentence-mapper'
        data=yaml.safe_load(open(config_path+'/sphinx-GPSR.yaml').read())
        for b,a in data.items():
            for ai in a:
                s=s.replace(ai,b)
        return s
    

if __name__=='__main__':
    rospy.init_node('speech_recog_node')
    r_node=Recognizer_Node()
    r_node.loop()
    #rospy.spin()