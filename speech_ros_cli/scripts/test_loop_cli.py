#!/usr/bin/env python3


import rospy
from speech_ros.srv import SpeechRecog,SpeechRecogResponse
from speech_ros.srv import TTS,TTSResponse
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
    try:
        tts = rospy.ServiceProxy('tts_input', TTS)
        resp=tts(msg)
        return resp.done_speaking
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)


if __name__=='__main__':
    rospy.init_node('speech_cli_node')
    print('Ready')
    while True:
        # input('Waiting for enter')
        msg=listen()
        print(msg)
        speak(msg)