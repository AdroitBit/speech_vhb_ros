#!/usr/bin/env python3

import rospy
from pocketsphinx_ros.srv import SpeechRecog,SpeechRecogResponse
from std_msgs.msg import Empty
from std_msgs.msg import String
from pocketsphinx import LiveSpeech
import os
import re
def map_phrase(s):
    s=re.sub("want a one","water",s)
    s=re.sub('why that is',"water please",s)
    s=re.sub('wanda',"water",s)
    s=re.sub('one of these','water please',s)
    s=re.sub('what the us','water please',s)
    s=re.sub('watch the new','water please',s)
    s=re.sub('what a', 'water', s)
    s=re.sub('what a reason', 'water please', s)
    s=re.sub('comair','come here',s)
    s=re.sub('calm yeah why','come here why',s)
    s=re.sub('i\'m year','come here',s)
    s=re.sub('let a couple of','like a cup of',s)
    s=re.sub('i would let it out on what the','i would like the cup of water',s)
    s=re.sub('i had a couple want to','give me the cup of water',s)
    s=re.sub('command','come here',s)
    s=re.sub('oh man','come here',s)
    s=re.sub('one of','come here',s)
    return s

def start_recog_callback(req):
    rospy.loginfo('Received request.Starting speech recognition....')

    f_start=open('/tmp/pocketsphinx_ros_starter.txt','w')
    f_start.write('EEEEEEEEEE')
    f_start.close()

    rate=rospy.Rate(10)
    while os.path.exists("/tmp/pocketsphinx_ros_comm.txt")==False:
        rate.sleep()

    sentence=open("/tmp/pocketsphinx_ros_comm.txt","r").read()
    sentence=map_phrase(sentence)
    os.remove("/tmp/pocketsphinx_ros_comm.txt")

    
    rospy.loginfo(f'Response to client with "{sentence}"')
    return SpeechRecogResponse(sentence)



if __name__=='__main__':
    rospy.init_node('pocketsphinx_speech_srv_node')
    print("Test")
    s = rospy.Service('recognizer/start', SpeechRecog, start_recog_callback )
    rospy.spin()