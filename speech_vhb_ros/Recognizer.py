import os
import re
import threading
from multiprocessing import Process
import time
import pyaudio
from vosk import Model, KaldiRecognizer
import speech_recognition as sr
import json
import yaml
import wave
import subprocess
from pathlib import Path
import numpy
#numpy.random.bit_generator = numpy.random._bit_generator
#numpy.random.BitGenerator = numpy.random.bit_generator.BitGenerator


import pandas as pd

import rospkg
rospack=rospkg.RosPack()
pkg_dir=rospack.get_path('skuba_ahr_speechprocessing')
import sys
sys.path.append(pkg_dir)
from scripts.SentenceManager import CommandExtractor
from scripts.SentenceManager import WordMapper

#from skuba_ahr_speechprocessing.SentenceManager import CommandExtractor
#from skuba_ahr_speechprocessing.SentenceManager import WordMapper


class Recognizer():
    def log_info(self,*a):
        if self.node is not None:
            self.node.log_info(*a)
        else:
            print(*a)
    def log_warn(self,*a):
        if self.node is not None:
            self.node.log_warn(*a)
        else:
            print(*a)
    def __init__(self,node=None,
            dictionary_configs=None,
            cmd_extraction=False,
            use_noisetorch=False):
        self.node=node
        self.dictionary_configs=dictionary_configs
        self.cmd_extraction=cmd_extraction

        #VOSK Recognizer
        #Download more vosk model from https://alphacephei.com/vosk/models
        #Extract and move model in ai-models folder in package
        #model_path=str(Path.home()/'Downloads/vosk-model-en-us-0.22-lgraph') #WER 7.82
        model_path=pkg_dir+'/ai-models/vosk-model-en-us-0.22-lgraph'
        self.log_info(f'VOSK_Recognizer initialized with model_path={model_path}')
        self.vosk_model = Model(model_path)
        self.log_info(f'VOSK_Recognizer setup done')
        
        self.use_noisetorch=use_noisetorch
        if self.use_noisetorch==True:
            self.log_info('Starting NoiseTorch')#starting with no gui
            subprocess.Popen('noisetorch -i',shell=True)


        self.log_info('Starting CommandExtractor')#starting command extractor to help listener
        self.cmd_extractor=CommandExtractor()
        self.cmd_extractor.load_model(datasets_path=pkg_dir+'/ai-models/command extractor/')

        self.log_info('Starting WordMapper')#starting word mapper to improve accuracy for certain environment
        self.word_mapper=WordMapper()

        #Create listener using speech_recognition(just in case)
        self.listener=sr.Recognizer()
        self.log_info('Adjusting listener for ambient noise,Please be quiet...')
        with sr.Microphone() as source:
            self.listener.adjust_for_ambient_noise(source,duration=1)
        self.listener.pause_threshold = 0.8
        self.log_info('Listener Adjusted')
        self.log_info(f'Energy threshold => {self.listener.energy_threshold}')
    def refresh_recognizer(self):
        freq=22000#default : 16000
        detect=[]
        noise=[]
        for config_path in self.dictionary_configs:
            config=yaml.safe_load(open(config_path))
            detect+=config['detect']
            noise+=config['noise']
        detect=list(set(detect))
        noise=list(set(noise))

        detect=" ".join(detect)
        noise=" ".join(noise)
        #self.log_info(f"Recognizer limited word to {detect}")

        limiter_vosk=json.dumps([detect,noise])
        self.vosk_rec=KaldiRecognizer(self.vosk_model,freq,limiter_vosk)
        
        self.vosk_rec.SetWords(True)
        self.vosk_rec.SetPartialWords(True)
        cap=pyaudio.PyAudio()
        self._stream=cap.open(format=pyaudio.paInt16,channels=1,rate=freq,input=True,frames_per_buffer=1024)
        self._stream.start_stream()
    def feed_live_audio(self):
        #self.vosk_rec.AcceptWaveform(self._stream.read(1024*10))
        self.vosk_rec.AcceptWaveform(self._stream.read(1024*4))
    def feed_wave_audio(self,data):
        self.vosk_rec.AcceptWaveform(data)
    def decoded_sentence(self):
        try:
            sentence_o=json.loads(self.vosk_rec.PartialResult())['partial']
            sentence=self.word_mapper.map(sentence_o)
            self.log_info(f'heard "{sentence}"')
            self.log_info(f'original heard "{sentence_o}"')
            return sentence
        except KeyError as e:
            self.log_warn(f'{e}')
            return ''
    def listen_command(self,sentence='',timeout=None):#listen for command only
        #sentence = "tomohawk please help me carry this luggage"
        #cmd="carry luggage"
        #listen until Hear the word "carry" and "luggage"

        #If sentence = "please help me carry this luggage;clean the room up"
        #sentence = ["please help me carry this luggage","clean the room up"]
        #cmds = ["carry luggage","clean up"]
        #hear the "carry" and "luggage" stop there and return "carry luggage".
        #hear the "clean" and "up" stop there and return "clean up".
        #same go with "yes" and "no"
        

        if self.cmd_extraction==True:
            cmds=[self.cmd_extractor.extract(s) for s in sentence.split(';')]
        else:
            cmds=[s for s in sentence.split(';')]
        
        self.log_warn(f'req.sentence is extracted into {cmds}')
        self.refresh_recognizer()
        time0=time.time()
        while True:
            self.log_info("Listening")
            self.feed_live_audio()
            self.log_info('Feed listen audio to vosk...')
            sentence=self.decoded_sentence()#This sentence var have nothing to do with upper one.

            for cmd in cmds:
                if all(word in sentence for word in cmd.split()):
                    self.log_info(f"Process time : {time.time()-time0:.2f}s")
                    return cmd,True
            if timeout is not None and time.time()-time0>timeout:
                return sentence,False
        return '',False

    def _run_test(self,dir_loc,audio_fn,sentence,command):
        audio_loc=os.path.join(dir_loc,audio_fn)
        self.log_info(f'Running test on file')
        self.log_info(f'audio_loc={audio_loc}')
        self.log_info(f'sentence={sentence}')
        self.log_info(f'command={command}')
        self.log_info(' ')

        wf=wave.open(audio_loc,'rb')
        freq=wf.getframerate()
        self.refresh_recognizer()

        sentence=''
        while True:
            data=wf.readframes(1024)
            if len(data)==0:
                break
            self.feed_wave_audio(data)
            sentence=self.decoded_sentence()
            if all(word in sentence for word in command.split()):
                return sentence,True
        return sentence,False

    def run_test(self,excel_file):
        excel_file=os.path.realpath(excel_file)
        dir_loc=os.path.dirname(excel_file)
        df=pd.read_excel(excel_file).fillna('')

        ndf=pd.DataFrame(columns=['heard sentence','success'])
        list_heard_sentence=[]
        list_success=[]
        for audio_fn,sentence,command in zip(df['filename'],df['sentence'],df['command']):
            heard_sentence,success=self._run_test(dir_loc,audio_fn,sentence,command)
            list_heard_sentence.append(heard_sentence)
            list_success.append(success)
        df['heard sentence']=list_heard_sentence
        df['success']=list_success
        df.to_excel(excel_file,index=False)

        self.log_info(f'Test result saved to {excel_file}')
        self.log_info(f'Success rate: {list_success.count(True)/len(list_success)*100:.2f}%')
        self.log_info(f'Fail rate: {list_success.count(False)/len(list_success)*100:.2f}')