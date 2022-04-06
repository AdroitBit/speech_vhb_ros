import os
import re
import yaml
import json
import pyaudio
import rospy
import rospkg

rospack = rospkg.RosPack()  
from speech_ros.srv import SpeechRecog,SpeechRecogResponse
from std_msgs.msg import Empty
from std_msgs.msg import String

import speech_recognition as sr
from vosk import Model,KaldiRecognizer
import os
import signal
import time
import statistics



def str2bool(s):
    if isinstance(s, bool):
        return s
    return s.lower() in ("true",) or bool(s)  
class Recognizer_Node:
    def __init__(self):
        rospy.init_node('speech_recog_node')
        self._ready=False
        rospy.logwarn('Setting up')
        self.srv=rospy.Service(rospy.get_param('recog_srv_name'), SpeechRecog, self.start_recog_callback )

        model_path=rospack.get_path('speech_ros')+'/models/'
        model_name=rospy.get_param('vosk_model_name')

        rospy.logwarn(f'Using model from {model_path}{model_name}')
        
        try:
            rospy.logwarn('Setting up Model object')
            self.model=Model(model_path+model_name)#Read the model
            rospy.logwarn('Setting up Recognizer')
            self.recognizer=KaldiRecognizer(self.model,16000)#Create the recognizer
        except Exception as e:
            if 'Failed to create a model' in str(e):
                if not os.path.exists(model_path):
                    print("Please run : $ rosrun speech_ros vosk_model_downloader.py")
                    print("It will setup and download the model for you.")
                elif not os.path.exists(model_path+model_name):
                    print('No model named '+model_name+' found in '+model_path)
                    print('Please check if parameter/argument is correct.')
                else:
                    rospy.logerr(e)
                    exit(1)
            else:
                rospy.logerr(e)
                exit(1)
        self.record_input=rospy.get_param('record_input','false')
        self.record_input=str2bool(self.record_input)
        self.record_ext=rospy.get_param('record_ext','.wav')
        self.record_ext=self.record_ext.lower()

        rospy.logwarn('Finish setting up')
        self._ready=True
            
    def start_recog_callback(self,req):
        rate=rospy.Rate(30)
        while self._ready==False:
            rate.sleep()
        rospy.loginfo(f'Received request.Starting speech recognition....')


        sentence_o=self.listen().lower()
        sentence=self.sentence_mapping(sentence_o)
        
        rospy.loginfo(f'Response to client with "{sentence}" , {sentence_o}')
        return SpeechRecogResponse(sentence)
    def sentence_mapping(self,s):
        config_path=rospack.get_path('speech_ros')+'/config/sentence-mapper'
        data=yaml.safe_load(open(config_path+'/vosk-GPSR.yaml').read())
        if data is None:
            return s
        for b,a in data.items():
            for ai in a:
                s=s.replace(ai,b)
        return s
    def save_audio(self,audio,path,ext):
        audios_fn = [int(f[0:-len(ext)]) for f in os.listdir(path) if f.endswith(ext)]

        audio_next_fn=1 if len(audios_fn)==0 else max(audios_fn)+1
        audio_next_fn=str(audio_next_fn).zfill(0)+ext

        path=path+'/'+audio_next_fn
        f=open(path,'wb')
        rospy.loginfo(f'Saving audio to {path}')
        if self.record_ext=='.wav':
            f.write(audio.get_wav_data(convert_rate=16000,convert_width=2))
            f.close()
        if self.record_ext=='.raw':
            f.write(audio.get_raw_data(convert_rate=16000,convert_width=2))
            f.close()
    def listen(self):
        cap=pyaudio.PyAudio()
        stream=cap.open(format=pyaudio.paInt16,channels=1,rate=16000,input=True,frames_per_buffer=1024)
        stream.start_stream()
        while True:
            data=stream.read(4096)
            if self.recognizer.AcceptWaveform(data):
               s=self.recognizer.Result()
               #print(type(s))
               stream.stop_stream()
               return json.loads(s)['text']

if __name__=='__main__':
    rospy.init_node('speech_recog_node')
    r_node=Recognizer_Node()
    rospy.spin()