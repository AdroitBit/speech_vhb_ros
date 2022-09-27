import os
import re
import threading
import time
import subprocess
import sys


import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from vhb_ros_interfaces.srv import SpeakCommand

def ros_ver():
    if "rospy" in sys.modules:
        return 1
    elif "rclpy" in sys.modules:
        return 2
    else:
        return 0
class pico2wave_Engine():
    def __init__(self):
        pass
    def perform(self,msg,wait_until_finished=True):
        #Can add '.' or ',' or '?' It will make the sentence tone more appropriately
        #But '.' need some spacing or It will speak 'dot'
        cmds=[]
        cmds.append(f'pico2wave -w /tmp/test.wav {repr(msg)}')
        #cmds.append(f'aplay /tmp/test.wav')
        cmds.append(f'mplayer -af scaletempo -speed 0.95 /tmp/test.wav')
        time.sleep(0.01)
        if wait_until_finished==True:
            os.system(' && '.join(cmds))
        else:
            #os.popen(' && '.join(cmds))
            subprocess.Popen(' && '.join(cmds),shell=True)
class SpeakerNode(Node):
    def __init__(self):
        self.init_node('speaker_node')
        self.srv=self.create_ros_srv('/speech/speak',SpeakCommand,self.srv_callback)
        self.tts_engine=pico2wave_Engine()
        self.log_info(f"Speaker node ready to be requested.")
    def srv_callback(self,req):
        self.log_info(f'speaking "{req.sentence}" with wait_for_success={req.wait_for_success}')
        try:
            self.tts_engine.perform(req.sentence,req.wait_for_success)
            return SpeakCommandResponse(True)
        except Exception as e:
            self.log_error(f'failed to speak "{req.sentence}"')
            self.log_error(e)
            return SpeakCommandResponse(False)
    def create_ros_srv(self,service_name,service_type,service_callback):
        try:
            return rospy.Service(service_name,service_type,service_callback)
        except:
            return self.create_service(service_name,service_type,service_callback)

    def log_info(self,msg):
        try:
            rospy.loginfo(msg)
        except:
            self.get_logger().info(msg)
    def log_error(self,msg):
        try:
            rospy.logerr(msg)
        except:
            self.get_logger().error(msg)
    def init_node(self,name):
        try:
            rospy.init_node(name)
        except:
            super().__init__(name)
    def spin(self):
        try:
            rospy.spin()
        except:
            rclpy.spin(self)
    def shutdown(self):
        try:
            rospy.shutdown()
        except:
            rclpy.shutdown()
def main():
    node=SpeakerNode()
    node.spin()
    node.shutdown()
if __name__ == '__main__':
    main()