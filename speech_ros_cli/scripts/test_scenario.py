#!/usr/bin/env python3


import rospy
from speech_ros.srv import SpeechRecog,SpeechRecogResponse
from speech_ros.srv import TTS,TTSResponse
from std_msgs.msg import String
import time
import random

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
    rospy.init_node('speech_cli_node')
    speak("I am ready for the command.")
    while True:
        drink_name=listen_for('water','cola','sprite','coke')

        speak(f'Please wait right there.I will be back with the bottle of {drink_name}')
        time.sleep(1)
        speak('Here is your drink.')
        listen_for('thank')
        speak('You are welcome.')