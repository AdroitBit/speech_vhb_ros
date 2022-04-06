import os
import re
import wget
import rospy
import rospkg
from speech_ros.srv import SpeechRecog,SpeechRecogResponse
from std_msgs.msg import Empty
from std_msgs.msg import String

import speech_recognition as sr
from vosk import Model,KaldiRecognizer
import os
import signal
import time
import statistics
rospack = rospkg.RosPack()

model_path=rospack.get_path('speech_ros')+'/models'

print("Visit to https://alphacephei.com/vosk/models and copy the download link,paste here and hit ENTER.")
url=input("Url : ")


print('The downloaded model will be saved in '+model_path)
if input('Ready? [Y/N] : ').lower() in ["y",'yes']:
    pass
else:
    exit(0)

if os.path.exists(model_path+'/vosk-model.zip'):
    print('There is vosk-model.zip here....')
    if input('\tOverwrite? [Y/N] : ').lower() in ["y",'yes']:
        wget.download(url,model_path+'/vosk-model.zip')
    else:
        if input('\t\tThen Extract it? [Y/N] : ').lower() in ["y",'yes']:
            pass
        else:
            print('\t\t\tNo work to do...exit')
else:
    wget.download(url,model_path+'/vosk-model.zip')


import os
models_o=os.listdir(model_path)
import zipfile
with zipfile.ZipFile(model_path+'/vosk-model.zip', 'r') as zip_ref:
    zip_ref.extractall(model_path)

models_n=os.listdir(model_path)

try:
    model_name=list(set(models_n)-set(models_o))[0]
    print("The downloaded model's name is "+model_name)
    print('Run this for testing the model : $ roslaunch speech_ros listener_speaker.launch recog_engine:=vosk vosk.model_name:={model_name}')
except IndexError as e:
    print('Cannot find the name of the downloaded model....')