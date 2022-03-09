import os
from pocketsphinx import LiveSpeech
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import pyttsx3
from playsound import playsound
from ament_index_python.packages import get_package_share_directory

from pocketsphinx_ros_interfaces.srv import TTS

import re
import time


def perform_tts(msg,tts_type='pico2wave'):
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
                os.system(f'pico2wave -w /tmp/test.wav "{s}"')
                playsound(f'/tmp/test.wav')

        #os.system(f'pico2wave -l en-US -w /tmp/tts.wav "{msg}"')
        #playsound('/tmp/tts.wav')
    elif tts_type=='festival':
        os.system(f'echo "{msg}" | festival --tts')
    else:
        msg=msg.strip().strip('.')
        for extension in [".wav",".mp3"]:
            dir=get_package_share_directory('pocketsphinx_ros')+'/glados-pre-sound/'
            fn=msg.lower()+".wav"
            if os.path.exists(dir+fn):
                playsound(dir+fn)


class PocketSphinx(Node):
    def __init__(self):
        super().__init__('pocketsphinx_tts_node')
        self.srv=self.create_service(TTS, 'tts/input', self.tts_callback)
        self.done_speaking=True
    def tts_callback(self,req,resp):
        msg=req.sentence
        self.get_logger().info(f'speaking "{msg}"')
        perform_tts(msg)
        resp.done_speaking=True
        return resp

def main(args=None):
    rclpy.init(args=args)
    node=PocketSphinx()
    print("Send request to tts_input for text to speech activation.")

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
if __name__=='__main__':
    main()