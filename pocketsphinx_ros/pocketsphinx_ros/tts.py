import os
from pocketsphinx import LiveSpeech
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import pyttsx3
from playsound import playsound
from ament_index_python.packages import get_package_share_directory



class PocketSphinx(Node):
    def __init__(self):
        super().__init__('pocketsphinx_tts_node')
        self.sub_tts=self.create_subscription(String, '/speech_tts/input', self.tts_callback, 10)
    def tts_callback(self,msg):
        msg=msg.data
        try:
            if msg[-1]=='.':
                msg=msg[:-1]
        except IndexError as e:
            pass
        for extension in [".wav",".mp3"]:
            dir=get_package_share_directory('pocketsphinx_ros')+'/glados-pre-sound/'
            fn=msg.lower()+".wav"
            if os.path.exists(dir+fn):
                playsound(dir+fn)
                self.get_logger().info(f'speaking "{msg}" from {extension}')
                return None
        #If file not found, use pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(msg)
        engine.runAndWait()
        self.get_logger().info(f'speaking "{msg}"')

def main(args=None):
    rclpy.init(args=args)
    node=PocketSphinx()
    print("Ready to speak")

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
if __name__=='__main__':
    main()