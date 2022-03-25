#!/usr/bin/env python3
import os
import re
from pocketsphinx import LiveSpeech
import rospy
import rospkg
from speech_ros.srv import SpeechRecog,SpeechRecogResponse
from std_msgs.msg import Empty
from std_msgs.msg import String


rospack=rospkg.RosPack()
scripts_dir=rospack.get_path('speech_ros')+'/scripts'
model_path=rospack.get_path('speech_ros')+'/model'

def start_recog_callback(req):
    global scripts_dir
    rospy.loginfo(f'Received request.Starting speech recognition....')

    sentence=os.popen(f'python3 {scripts_dir}/recog_nodes/_pocketsphinx_recog_node.py').read()

    rospy.loginfo(f'Response to client with "{sentence}" , {len(sentence)}')
    return SpeechRecogResponse(sentence)



if __name__=='__main__':
    rospy.init_node('speech_recog_node')
    print("You can send request to recognizer/start for speech recognition start")
    s = rospy.Service('recognizer/start', SpeechRecog, start_recog_callback )
    rospy.spin()