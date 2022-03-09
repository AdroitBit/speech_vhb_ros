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
    speak("Speeh setup")
    speak("Ready for commands")
    while True:
        listen_for('come','come here','good')
        

        speak('I am coming Weeeeeeeee')
        time.sleep(2)

        speak('What would you like to drink?')
        #I would like (coke,water,sprite)
        drink_name=listen_for('coke','water','sprite','cola','beer')
        speak(f'Ok,I will be back with the cup of {drink_name}.')
        speak('E E EE E E EE E E')
        time.sleep(2)



        speak('Here is your drink.')
        listen_for('thank')
        speak('You are welcome.')
        time.sleep(1)
        speak('I\'m getting back to origin position.')
        speak('Weeeeeeeeee')