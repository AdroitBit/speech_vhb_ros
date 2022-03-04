import os
from pocketsphinx import LiveSpeech
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import pyttsx3
from playsound import playsound
from ament_index_python.packages import get_package_share_directory



##########################
# this node will listen to the microphone and publish the recognized words to the topic
# and also subscribe to other topic which will be to do text to speech stuff with your speaker
##########################



class PocketSphinx(Node):
    def __init__(self):
        super().__init__('pocketsphinx_speech_pub_node')
        self.topic_recog='/speech_recognition/output'
        self.pub_recognizer = self.create_publisher(String, self.topic_recog, 10)
        #self.pub_recognizer_timer = self.create_timer(
        #    timer_period_sec=0.1,
        #    self.recognition_timer_callback
        #)
    def publish(self,msg):
        _msg=String()
        _msg.data=str(msg)
        self.pub_recognizer.publish(_msg)
    def start_recognition(self):
        for phrase in LiveSpeech():
            self.publish(phrase)
            self.get_logger().info(f'Publishing "{phrase}" to {self.topic_recog}')
            break

def main(args=None):
    rclpy.init(args=args)
    node=PocketSphinx()
    try:
        while True:
            node.start_recognition()
    except KeyboardInterrupt as e:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()