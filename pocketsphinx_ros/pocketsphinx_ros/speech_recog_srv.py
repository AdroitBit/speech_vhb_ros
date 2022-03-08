import os
from pocketsphinx import LiveSpeech
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Empty
import pyttsx3
from playsound import playsound
from ament_index_python.packages import get_package_share_directory
import re

from pocketsphinx_ros_interfaces.srv import SpeechRecog
import threading



##########################
# The service can be requested for returned speech
##########################
def map_phrase(s):
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

def perform_recog():
    for phrase in LiveSpeech():
        return map_phrase(str(phrase))

class PocketSphinx(Node):
    def __init__(self,wtf=False):
        print(wtf)
        super().__init__('pocketsphinx_speech_srv_node')
        self.srv_start= self.create_service(SpeechRecog, 'recognizer/start',self.srv_recog_callback)
        self.sub_start=self.create_subscription(Empty, 'recognizer/foxy/start',self.sub_recog_callback,10)#This can be only called by other ROS distro
        self.pub_output=self.create_publisher(String, 'recognizer/foxy/output', 10)
        self.timer_file=self.create_timer(1/10,self.file_callback)
        
    def srv_recog_callback(self,req,resp):
        self.get_logger().info(f'Recognizer triggered by Requested...')
        resp.sentence=perform_recog()
        self.get_logger().info(f'Response to client with "{resp.sentence}"')
        return resp
    def sub_recog_callback(self,data):
        self.get_logger().info(f'Recognizer triggered by Subscriber...')
        msg=String()
        msg.data=perform_recog()
        self.pub_output.publish(msg)
        self.get_logger().info(f'Response to subscriber with "{msg.data}"')
    def file_callback(self):
        if os.path.exists('/tmp/pocketsphinx_ros_starter.txt'):
            os.remove('/tmp/pocketsphinx_ros_starter.txt')
            self.get_logger().info('Recognizer triggered by File...')
            sentence=perform_recog()
            f_output=open("/tmp/pocketsphinx_ros_comm.txt","w")
            f_output.write(sentence)
            f_output.close()
            self.get_logger().info(f'Response to file request with "{sentence}"')
def main(args=None):
    rclpy.init(args=args)
    node=PocketSphinx()
    print("Send request to recognizer/start for speech recognition activation.")
    print("Or publish Empty to recognizer/foxy/start")

    rclpy.spin(node)


    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()