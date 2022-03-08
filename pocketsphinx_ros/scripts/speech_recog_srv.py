#!/usr/bin/env python3

import rospy
from pocketsphinx_ros.srv import SpeechRecog,SpeechRecogResponse
from std_msgs.msg import Empty
from std_msgs.msg import String
from pocketsphinx import LiveSpeech
import os


def start_recog_callback(req):
    rospy.loginfo('Received request.Starting speech recognition....')

    f_start=open('/tmp/pocketsphinx_ros_starter.txt','w')
    f_start.write('EEEEEEEEEE')
    f_start.close()

    rate=rospy.Rate(10)
    while os.path.exists("/tmp/pocketsphinx_ros_comm.txt")==False:
        rate.sleep()

    sentence=open("/tmp/pocketsphinx_ros_comm.txt","r").read()
    os.remove("/tmp/pocketsphinx_ros_comm.txt")
    
    rospy.loginfo(f'Response to client with "{sentence}"')
    return SpeechRecogResponse(sentence)



if __name__=='__main__':
    rospy.init_node('pocketsphinx_speech_srv_node')
    print("Test")
    s = rospy.Service('recognizer/start', SpeechRecog, start_recog_callback )
    rospy.spin()