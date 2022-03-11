#!/usr/bin/env python3


import rospy
from pocketsphinx_ros.srv import SpeechRecog,SpeechRecogResponse
from pocketsphinx_ros.srv import TTS,TTSResponse
from std_msgs.msg import String
import time

def listen():
    rospy.wait_for_service('recognizer/start')
    try:
        start_recog = rospy.ServiceProxy('recognizer/start', SpeechRecog)
        resp=start_recog()
        return resp.sentence
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
def speak(msg):
    rospy.wait_for_service('tts_input')
    print(msg)
    try:
        tts = rospy.ServiceProxy('tts_input', TTS)
        resp=tts(msg)
        return resp.done_speaking
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def listen_for(*words):
    while True:
        sentence=listen()
        for w in words:
            if w in sentence:
                return w
        #rospy.loginfo(f'Hear "{sentence}" but don\'t have one on these {words}')


if __name__=='__main__':
    print('Ready')
    while True:
        w=listen_for('come','come here','good','tomohawk')
        speak(f'heard {w}')