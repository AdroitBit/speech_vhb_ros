import os
from pocketsphinx import LiveSpeech
import rclpy
from rclpy.node import Node
from std_msgs.msg import String



class PocketSphinx(Node):
    def __init__(self):
        super().__init__('pocketsphinx_ros_node')
        self.pub_recognizer=self.create_publisher(String, '/speech_recognition/output', 10)
        self.sub_tts=self.create_subscription(String, '/speech_tts/input', self.tts_callback, 10)
    def publish(self,msg):
        _msg=String()
        _msg.data=str(msg)
        self.pub_recognizer.publish(_msg)
    def start_recognition(self):
        for phrase in LiveSpeech():
            self.publish(phrase)
            self.get_logger().info(f'Publishing "{phrase}"')
            break
    def tts_callback(self,msg):
        self.get_logger().info(f'speaking "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    node=PocketSphinx()
    try:
        while True:
            node.start_recognition()
    except KeyboardInterrupt as e:
        node.destroy_node()
        rclpy.shutdown()

if __name__=='__main__':
    main()