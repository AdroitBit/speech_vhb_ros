import os
from pocketsphinx import LiveSpeech
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import pyttsx3
from playsound import playsound
from ament_index_python.packages import get_package_share_directory
import re

from pocketsphinx_ros_interfaces.srv import SpeechRecog



##########################
# The service can be requested for returned speech
##########################



class PocketSphinx(Node):
    def __init__(self):
        super().__init__('pocketsphinx_speech_srv_node')
        self.srv = self.create_service(SpeechRecog, 'speech_recog_output',self.recog_callback)
    def recog_callback(self,req,resp):
        self.get_logger().info(f'Requested...')
        for phrase in LiveSpeech():
            #self.publish(phrase)
            #resp.sentence=str(phrase)
            resp.sentence=self.map_phrase(str(phrase))
            self.get_logger().info(f'Response to some client with "{phrase}"')
            break
        return resp



    def map_phrase(self,s):
        s=re.sub("want a one","water",s)
        s=re.sub('why that is',"water please",s)
        s=re.sub('wanda',"water",s)
        s=re.sub('one of these','water please',s)
        s=re.sub('what the us','water please',s)
        s=re.sub('watch the new','water please',s)
        s=re.sub('what a', 'water', s)
        s=re.sub('what a reason', 'water please', s)
        s=re.sub('comair','come here',s)
        s=re.sub('calm yeah why','come here why',s)
        s=re.sub('i\'m year','come here',s)
        s=re.sub('let a couple of','like a cup of',s)
        s=re.sub('i would let it out on what the','i would like the cup of water',s)
        s=re.sub('i had a couple want to','give me the cup of water',s)
        return s

def main(args=None):
    rclpy.init(args=args)
    node=PocketSphinx()
    print("Send request to speech_recog_output for speech recognition activation.")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()