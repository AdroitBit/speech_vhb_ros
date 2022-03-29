import speech_recognition as sr
from pocketsphinx import AudioFile,Pocketsphinx,Decoder,DefaultConfig
import os
import signal

import rospy
import rospkg
rospack = rospkg.RosPack()
#Record
r=sr.Recognizer()
with sr.Microphone() as source:
    print("Adjust ambient noise!")
    r.adjust_for_ambient_noise(source, duration=5)
    print("Say something!")
    audio=r.listen(source,phrase_time_limit=10)

    audio=audio.get_raw_data(convert_rate=16000,convert_width=2)

    f=open('/tmp/speech.raw','wb')
    f.write(audio)

#Detecting
model_path=rospack.get_path('speech_ros')+'/model'
#Way 1
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
audio = AudioFile(**config)
for phrase in audio:
    print(phrase)


#Way2
#config = {
#    'hmm': os.path.join(model_path, 'en-us'),
#    'lm': os.path.join(model_path, 'en-us.lm.bin'),
#    'dict': os.path.join(model_path, 'KU_Robocup-en-us.dict')
#}
#ps=Pocketsphinx(**config)
#ps.decode(
#    audio_file='/tmp/speech.raw',
#    buffer_size=2048,
#    no_search=False,
#    full_utt=False
#)
#print(ps.segments())
#print(ps.confidence())

#Way3 

#config=DefaultConfig()
#config.set_string('-hmm',os.path.join(model_path, 'en-us'))
#config.set_string('-lm',os.path.join(model_path, 'en-us.lm.bin'))
#config.set_string('-dict',os.path.join(model_path, 'KU_Robocup-en-us.dict'))
#decoder=Decoder(config)
#
#buf=bytearray(2048)
#f=open('/tmp/speech.raw','rb')
#decoder.start_utt()
#decoder.process_raw(audio,False,True)
#decoder.end_utt()
#
#hypothesis = decoder.hyp()
#print(hypothesis.hypstr)


#try:
#    print("Sphinx thinks you said '" + r.recognize_sphinx(audio) + "'")  
#
#    #print("Sphinx thinks you said '" + r.recognize_google(audio) + "'") 
#except sr.UnknownValueError:
#    print("Sphinx could not understand audio")  
#except sr.RequestError as e:
#    print("Sphinx error; {0}".format(e))