#!/usr/bin/env python3

import rospy
from pocketsphinx_ros.srv import SpeechRecog,SpeechRecogResponse
from std_msgs.msg import Empty
from std_msgs.msg import String
from pocketsphinx import LiveSpeech
import os
import re

scripts_dir=os.path.dirname(__file__)

def start_recog_callback(req):
    global scripts_dir
    rospy.loginfo(f'Received request.Starting speech recognition.... : {req.keywords}')

    sentence=os.popen(f'python3 {scripts_dir}/_speech_recog_node.py').read()
    rospy.loginfo(f'Response to client with "{sentence}" , {len(sentence)}')
    return SpeechRecogResponse(sentence)



if __name__=='__main__':
    rospy.init_node('speech_recog_node')
    print("You can send request to recognizer/start for speech recognition start")
    s = rospy.Service('recognizer/start', SpeechRecog, start_recog_callback )
    rospy.spin()