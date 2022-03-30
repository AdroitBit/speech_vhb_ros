#!/usr/bin/env python3

#Just kill me the code is so messy.I'm litterally combine pyaudio and pocketsphinx which is hard af
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


rospack=rospkg.RosPack()
scripts_dir=rospack.get_path('speech_ros')+'/scripts'
model_path=rospack.get_path('speech_ros')+'/model'
r=sr.Recognizer()

def start_recog_callback(req):
    global scripts_dir
    global model_path
    rospy.loginfo(f'Received request.Starting speech recognition....')
    
    #I don't want to call os.system.God damn it python
    if os.path.exists('/tmp/speech_recog_output.txt'):
        os.remove('/tmp/speech_recog_output.txt')
    os.system(f'python3 {scripts_dir}/_pocketsphinx_recog_pyaudio.py')
    sentence=open('/tmp/speech_recog_output.txt','r').read()
    #sentence=os.popen(f'python3 {scripts_dir}/_pocketsphinx_recog.py').read()

    rospy.loginfo(f'Response to client with "{sentence}" , {len(sentence)}')
    return SpeechRecogResponse(sentence)
class Recognizer:
    def __init__(self):
        self.srv=rospy.Service('recognizer/start', SpeechRecog, self.start_recog_callback)
    def start_recog_callback(self):
        global scripts_dir
        global model_path
        rospy.loginfo(f'Received request.Starting speech recognition....')
        
        #I don't want to call os.system.God damn it python
        if os.path.exists('/tmp/speech_recog_output.txt'):
            os.remove('/tmp/speech_recog_output.txt')
        os.system(f'python3 {scripts_dir}/_pocketsphinx_recog_pyaudio.py')
        sentence=open('/tmp/speech_recog_output.txt','r').read()
        #sentence=os.popen(f'python3 {scripts_dir}/_pocketsphinx_recog.py').read()

        rospy.loginfo(f'Response to client with "{sentence}" , {len(sentence)}')
        return SpeechRecogResponse(sentence)


switch_recog_on=False
if __name__=='__main__':
    rospy.init_node('speech_recog_node')

    print("You can send request to recognizer/start for speech recognition start")
    s = rospy.Service('recognizer/start', SpeechRecog, start_recog_callback )

    while True:

    rospy.spin()