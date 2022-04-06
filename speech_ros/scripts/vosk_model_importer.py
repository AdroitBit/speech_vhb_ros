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
from tkinter import Tk
from tkinter.filedialog import askopenfilename
rospack = rospkg.RosPack()

model_path=rospack.get_path('speech_ros')+'/models'

print("You have to downloaded model from https://alphacephei.com/vosk/models to this device.")
print("This is for importing that model to this ROS package.")

print('Select the vosk model (.zip file)')
root=Tk()
url=askopenfilename(
    title='Select the vosk model (.zip file)',
    initialdir='~/Downloads',
    filetypes=(
        ('zip files', '*.zip'),
    ))
print('File selected : '+url)
root.destroy()


import os
models_o=os.listdir(model_path)
import zipfile
with zipfile.ZipFile(url, 'r') as zip_ref:
    zip_ref.extractall(model_path)

models_n=os.listdir(model_path)

try:
    model_name=list(set(models_n)-set(models_o))[0]
    print("The import model's name is "+model_name)
    print(f'Run this for testing the model : $ roslaunch speech_ros listener_speaker.launch recog_engine:=vosk vosk.model_name:={model_name}')
except IndexError as e:
    print('Cannot find the name of the downloaded model....')