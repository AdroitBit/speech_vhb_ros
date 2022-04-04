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
import time

rospack=rospkg.RosPack()
    

class Recognizer_Node:
    def __init__(self):
        rospy.init_node('speech_recog_node')
        rospy.logwarn('Setting up')
        self.srv=rospy.Service('recognizer/start', SpeechRecog, self.start_recog_callback)
        #It named recognizer but It's only good at listening.
        #adjust ambient noise for listener
        self._listener=sr.Recognizer()

        #self._listener.energy_threshold=2364
        #self._listener.pause_threshold = 0.8
        rospy.logwarn('Adjusting listener for ambient noise...')
        with sr.Microphone() as source:
            self._listener.adjust_for_ambient_noise(source,duration=1)
        self._listener.pause_threshold = 1.0
        rospy.logwarn('Listener Adjusted')
        rospy.loginfo(f'Energy threshold => {self._listener.energy_threshold}')
        
        #self._listener.dynamic_energy_threshold = True
        #self._listener.dynamic_energy_adjustment_damping = 0.15
        #self._listener.dynamic_energy_adjustment_ratio = 1.5
        #self._listener.pause_threshold = 0.8
        #energy_threshold=>1300


        self._sentence=''

        self._switch_recog_on=False
    def loop(self):
        rate=rospy.Rate(30)
        while True:#Use loop because I can't use decoder in service . I need to use service for activation to this loop that can use decoder!
            if self._switch_recog_on==True:
                try:
                    rospy.loginfo(f'Activating listener')
                    self.listen()
                    rospy.loginfo(f'Activating Decoder')
                    self._sentence=self.decode_audio_file_to_text()
                except sr.WaitTimeoutError as e:
                    rospy.loginfo(f'Timeout : {e}')
                self._switch_recog_on=False
            rate.sleep()

            
    def start_recog_callback(self,req):
        rospy.loginfo(f'Received request.Starting speech recognition....')

        self._switch_recog_on=True
        rate=rospy.Rate(10)
        while self._switch_recog_on==True:
            rate.sleep()

        rospy.loginfo(f'Response to client with "{self._sentence}" , {len(self._sentence)}')
        return SpeechRecogResponse(self._sentence)
    def start_recog_callback2(self,req):
        rospy.loginfo(f'Received request.Starting speech recognition....')

        with sr.Microphone() as source:
            audio = self._listener.listen(source)
        raw_data=audio.get_raw_data(convert_rate=16000,convert_width=2)

        model_path=rospack.get_path('speech_ros')+'/model'
        config = Decoder.default_config()
        config.set_string("-hmm", f'{model_path}/en-us')  # set the path of the hidden Markov model (HMM) parameter files
        config.set_string("-lm", f'{model_path}/en-us.lm.bin')  # set the path to the language model parameter file
        config.set_string("-dict", f'{model_path}/GPSR-en-us.dict')  # set the path to the dictionary file
        config.set_string("-logfn", os.devnull)  # disable logging (logging causes unwanted output in terminal)
        decoder = Decoder(config)

        decoder.start_utt()
        decoder.process_raw(raw_data, False, True)
        decoder.end_utt()

        hypothesis = decoder.hyp()
        if hypothesis is not None:
            print('Best hypothesis: ', hypothesis.hypstr, " model score: ", hypothesis.best_score, " confidence: ", hypothesis.prob)
            sentence = hypothesis.hypstr
        else:
            sentence='null'

        rospy.loginfo(f'Response to client with "{self._sentence}" , {len(self._sentence)}')
        return SpeechRecogResponse(self._sentence)

    def listen(self):
        with sr.Microphone() as source:
            audio=self._listener.listen(source,timeout=10,phrase_time_limit=17)
        
        f=open('/tmp/speech.raw','wb')
        f.write(audio.get_raw_data(convert_rate=16000,convert_width=2))
        f.close()

        f=open('/tmp/speech.wav','wb')
        f.write(audio.get_wav_data(convert_rate=16000,convert_width=2))
        f.close()
        return audio

    def decode_audio_file_to_text(self):
        model_path=rospack.get_path('speech_ros')+'/model'
        config = {
            'verbose': False,
            'audio_file': '/tmp/speech.raw',
            'buffer_size': 2048,
            'no_search': False,
            'full_utt': False,
            'hmm': os.path.join(model_path, 'en-us'),
            'lm': os.path.join(model_path, 'en-us.lm.bin'),
            'dic': os.path.join(model_path, rospy.get_param('dict', 'cmudict-en-us.dict'))
        }
        #Need to use AudioFile Object because It has customiztion But doesn't in main thread for some reason
        fps=100
        audio=AudioFile(**config,frate=fps)
        for phrase in audio:
            print(phrase.seg())
            if phrase is None:
                return 'null'
            else:
                return str(phrase)
        return 'null'
    def sentence_mapping(self,s):
        config_path=rospack.get_path('speech_ros')+'/config/sentence-mapper'
        data=yaml.load(open(config_path+'/sphinx-GPSR.yaml').read())
        for b,a in data.items():
            for ai in a:
                s=s.replace(ai,b)
        return s
    

if __name__=='__main__':
    rospy.init_node('speech_recog_node')
    r_node=Recognizer_Node()
    r_node.loop()
    #rospy.spin()