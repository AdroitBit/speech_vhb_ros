#!/usr/bin/env python3


import rospy
from std_msgs.msg import String
import time
import re
import os

def listen():
    rospy.wait_for_service('recognizer/start')
    try:
        start_recog = rospy.ServiceProxy('recognizer/start', SpeechRecog)
        resp=start_recog()
        return resp.sentence
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
def speak(msg,tts_type='pico2wave'):
    if tts_type=='espeak':
        os.system(f'espeak "{msg}" -s70 -v en-us')
    elif tts_type=='pico2wave':
        
        ss=re.split('(\.|\,|\?)', msg)
        for s in ss:
            if s=='.':
                time.sleep(0.2)
            elif s==',':
                time.sleep(0.1)
            elif s=='?':
                time.sleep(0.3)
            else:
                os.system(f'pico2wave -l en-US -w /tmp/test.wav "{s}"')
                playsound('/tmp/test.wav')
    elif tts_type=='festival':
        os.system(f'echo "{msg}" | festival --tts')
    else:
        msg=msg.strip().strip('.')
        for extension in [".wav",".mp3"]:
            dir=get_package_share_directory('pocketsphinx_ros')+'/glados-pre-sound/'
            fn=msg.lower()+".wav"
            if os.path.exists(dir+fn):
                playsound(dir+fn)

def listen_for(*words):
    while True:
        sentence=listen()
        for w in words:
            if w in sentence:
                return w
        #rospy.loginfo(f'Hear "{sentence}" but don\'t have one on these {words}')



if __name__=='__main__':
    speak("Speeh setup,Ready for commands")



    input("Waiting enter")
    speak('I\'m coming.Please wait there.')
    time.sleep(2)
    speak('Hello,What would you like to drink?')
    input("Waiting enter")
    speak('Ok,I will be back with your drink.')
    time.sleep(2)
    speak('Hear is your drink')
    input("Waiting enter")
    speak("You're welcome")