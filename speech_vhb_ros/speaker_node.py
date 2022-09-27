import os
import re
import threading
import time
import subprocess


import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from vhb_ros_interfaces.srv import SpeakCommand

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
        rospy.init_node('speaker_node')
        self.srv=rospy.Service('/speech/speak',SpeakCommand,self.srv_callback)
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

    def log_info(self,msg): 
        rospy.loginfo(msg)
    def log_error(self,msg):
        rospy.logerr(msg)
def main():
    node=SpeakerNode()
    rospy.spin()
if __name__ == '__main__':
    main()