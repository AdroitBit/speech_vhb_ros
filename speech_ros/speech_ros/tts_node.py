import os
import re
import rclpy
import threading

from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Empty
from ament_index_python.packages import get_package_share_directory
from speech_ros_interfaces.srv import TTS



class TextToSpeechNode():
    def __init__(self):
        self.tts_srv=self.create_service(TTS, '/<ns>/speech/speak', self.tts_callback)
        self.declare_parameter(
            namespace='',
            parameters=[
                ('tts_engine','pico2wave')
            ]
        )
    def perform_tts(msg,tts_type='pico2wave'):
        if tts_type=='espeak':
            os.system(f'espeak "{msg}" -s70 -v en-us')
        elif tts_type=='pico2wave':#recommended
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
        elif tts_type=='festival':
            os.system(f'echo "{msg}" | festival --tts')
        elif tts_type=='glados':#Work in progress
            msg=msg.strip().strip('.')
            for extension in [".wav",".mp3"]:
                dir=get_package_share_directory('speech_ros')+'/glados-pre-sound/'
                fn=msg.lower()+".wav"
                if os.path.exists(dir+fn):
                    playsound(dir+fn)
    def tts_callback(self,req,resp):
        msg=req.sentence
        self.get_logger().info(f'speaking "{msg}"')
        self.perform_tts(msg,tts_type='pico2wave')
        resp.done_speaking=True
        return resp

def main(args=None):
    rclpy.init(args=args)
    node=TextToSpeechNode()
    print("Send request to .... for text to speech activation.")

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
if __name__=='__main__':
    main()