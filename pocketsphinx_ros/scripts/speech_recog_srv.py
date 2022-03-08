#!/usr/bin/env python3

import os
from pocketsphinx import LiveSpeech
from std_msgs.msg import String
import pyttsx3
import re
from playsound import playsound
from pocketsphinx_ros.srv import SpeechRecog,SpeechRecogResponse
import rospy

def recog_callback(req):
    rospy.loginfo("Requested...")
    for phrase in LiveSpeech():
        phrase=map_phrase(phrase)
        rospy.loginfo('Response to some client with "%s"', phrase)
        return SpeechRecogResponse(phrase)
def map_phrase(self,s):
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
    return s

if __name__ == "__main__":
    rospy.init_node('pocketsphinx_speech_srv_node')
    s = rospy.Service('speech_recog_output', SpeechRecog, recog_callback )
    print("Send request to speech_recog_output for speech recognition activation.")

    rospy.spin()