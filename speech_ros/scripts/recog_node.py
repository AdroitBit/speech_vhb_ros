#!/usr/bin/env python3

#Just kill me the code is so messy.I'm litterally combine pyaudio and pocketsphinx which is hard af
import os
import re
import rospy
import rospkg
from speech_ros.srv import SpeechRecog,SpeechRecogResponse
from std_msgs.msg import Empty
from std_msgs.msg import String


import speech_recognition as sr
from pocketsphinx import AudioFile,Pocketsphinx,Decoder,DefaultConfig
import os
import signal


rospack=rospkg.RosPack()
scripts_dir=rospack.get_path('speech_ros')+'/scripts'
model_path=rospack.get_path('speech_ros')+'/model'
r=sr.Recognizer()

def start_recog_callback(req):
    global scripts_dir
    global model_path
    rospy.loginfo(f'Received request.Starting speech recognition....')

    #Recording (save to .raw file)
    with sr.Microphone() as source:
        audio=r.listen(source,phrase_time_limit=10)
    audio=audio.get_raw_data(convert_rate=16000,convert_width=2)
    f=open('/tmp/speech.raw','wb')
    f.write(audio)

    #Detecting
    config = {
        'verbose': False,
        'audio_file': '/tmp/speech.raw',
        'buffer_size': 2048,
        'no_search': False,
        'full_utt': False,
        'hmm': os.path.join(model_path, 'en-us'),
        'lm': os.path.join(model_path, 'en-us.lm.bin'),
        #'dict': os.path.join(model_path, 'cmudict-en-us.dict')
        'dic': os.path.join(model_path, 'drink-en-us.dict')
    }
    audio=AudioFile(**config)
    for phrase in audio:
        pass
    sentence=str(phrase)



    #sentence=os.popen(f'python3 {scripts_dir}/_pocketsphinx_recog.py').read()

    rospy.loginfo(f'Response to client with "{sentence}" , {len(sentence)}')
    return SpeechRecogResponse(sentence)



if __name__=='__main__':
    rospy.init_node('speech_recog_node')
    rospy.logwarn('Adjusting to ambient noise for 5 seconds...')
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=5)
    rospy.logwarn('Adjusted')

    print("You can send request to recognizer/start for speech recognition start")
    s = rospy.Service('recognizer/start', SpeechRecog, start_recog_callback )
    rospy.spin()