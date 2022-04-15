import os
import re
import rclpy
import threading

from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Empty
from ament_index_python.packages import get_package_share_directory
from speech_ros_interfaces.srv import TTS


class pico2wave_Engine():
    def __init__(self):
        pass
    def perform(self,msg):
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
                os.system(f'aplay /tmp/test.wav')
    def perform_async(self,msg):
        cmds=[]
        ss=re.split('(\.|\,|\?)', msg)
        for s in ss:
            if s=='.':
                cmds.append("sleep 0.2")
            elif s==',':
                cmds.append("sleep 0.1")
            elif s=='?':
                cmds.append("sleep 0.3")
            else:
                cmds.append(f'pico2wave -w /tmp/test.wav "{s}"')
                cmds.append(f'aplay /tmp/test.wav')
        os.popen('&&'.join(cmds))
class espeak_Engine():
    def __init__(self):
        pass
    def perform(self,msg):
        os.system(f'espeak "{msg}"')
class festival_Engine():
    def __init__(self):
        pass
    def perform(self,msg):
        os.system(f'echo "{msg}" | festival --tts')
class glados_Engine():#WIP 
    def __init__(self):
        pass
    def perform(self,msg):
        msg=msg.strip().strip('.')
        for extension in [".wav",".mp3"]:
            dir=get_package_share_directory('speech_ros')+'/glados-pre-sound/'
            fn=msg.lower()+".wav"
            if os.path.exists(dir+fn):
                playsound(dir+fn)


class TextToSpeechNode(Node):
    def __init__(self):
        super().__init__('text_to_speech_node')
        self.declare_parameters(
            namespace='',
            parameters=[
                ('tts_engine','pico2wave')
            ]
        )
        ns_prefix=self.get_namespace()
        self.srv_name=ns_prefix+'/speech/speak'
        self.tts_srv=self.create_service(TTS, self.srv_name, self.tts_callback)
        
        tts_engine=str(self.get_parameter('tts_engine').value)
        if tts_engine=='pico2wave':
            self.engine=pico2wave_Engine()
        elif tts_engine=='espeak':
            self.engine=espeak_Engine()
        elif tts_engine=='festival':
            self.engine=festival_Engine()
        elif tts_engine=='glados':
            self.engine=glados_Engine()
    def tts_callback(self,req,resp):
        msg,wait_for_success=req.sentence,req.wait_for_success
        self.get_logger().info(f'speaking "{msg}"')
        try:
            if wait_for_success==False:
                self.engine.perform_async(msg)
            if wait_for_success==True:
                self.engine.perform(msg)
            resp.success=True
            return resp

        except Exception as e:
            self.get_logger().error(f'failed to speak "{msg}"')
            self.get_logger().error(e)
            resp.success=False
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