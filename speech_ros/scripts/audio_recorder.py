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
import statistics