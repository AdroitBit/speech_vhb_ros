#!/usr/bin/env python3


import rospy
from pocketsphinx_ros.srv import SpeechRecog,SpeechRecogResponse
from pocketsphinx_ros.srv import TTS,TTSResponse
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
    print("I am ready for the command.")
    while True:
        w=listen_for('come','here','good','tomohawk','hi','hey')
        if 'come' in w:
            #speak('Hello, I am Tomohawk')
            speak('I am coming.')
            time.sleep(2)
        else:
            pass

        speak(random.choice([
            'What would you like to drink?',
            'Hello,What do you want to drink?'
        ]))
        #I would like (coke,water,sprite)
        drink_name=listen_for('coke','water','sprite','cola','apple juice')
        speak(f'Ok,I will be back with the cup of {drink_name}.')
        time.sleep(2)



        speak('Here is your drink.')
        listen_for('thank')
        speak('You are welcome.')
        time.sleep(1)
        speak('I\'m getting back to my origin position.')
        time.sleep(2)