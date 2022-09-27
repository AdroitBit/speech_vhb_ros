#!/usr/bin/env python

import rclpy
from ament_index_python.packages import get_package_share_directory
pkg_dir = get_package_share_directory('speech_vhb_ros')

from rclpy.node import Node
from std_msgs.msg import String
from speech_vhb_ros.msg import Speech


#from skuba_ahr_speechprocessing.Recognizer import Recognizer
import sys
import os
sys.path.append(pkg_dir)
from scripts.Recognizer import Recognizer
from skuba_ahr_msgs.srv import ListenCommand,ListenCommandResponse
import time
from pathlib import Path
dictionary_cfg=Path(pkg_dir+'/config/dictionary')
word_mapper_cfg=Path(pkg_dir+'/config/word-mapepr')

class ListenerNode():
    def __init__(self):
        rospy.init_node('listener_node')
        self.recognizer=Recognizer(
            node=self,
            dictionary_configs=[
                dictionary_cfg/'arena-objects.yaml',
                dictionary_cfg/'arena-furniture.yaml',
                #config_path/'carry-luggage.yaml',
                dictionary_cfg/'common.yaml',
                dictionary_cfg/'names.yaml',
                dictionary_cfg/'edible-std-objects.yaml'
            ],
            cmd_extraction=False,
            use_noisetorch=False
        )
        self.srv=rospy.Service('basil/speech/listen',ListenCommand,self.srv_callback)

        self.log_info(f"Listener node ready to be requested.")
    def srv_callback(self,req):
        time0=time.time()
        req_sentence=req.sentence.lower()
        self.log_info('Listening...')
        self.log_info(f'req.sentence="{req_sentence}"')
        self.log_info(f'req.timeout={req.timeout}')
        try:
            resp_sentence,is_success = self.recognizer.listen_command(
                sentence=req_sentence,
                timeout=None if req.timeout<0 else req.timeout
            )
            self.log_info(f'Result from listen_command')
            self.log_info(f'resp_sentence="{resp_sentence}"')
            self.log_info(f'is_success={is_success}')
            resp=ListenCommandResponse()
            resp.sentence=resp_sentence
            resp.success=is_success
            self.log_info(f'Response time : {time.time()-time0}')
            return resp
        except Exception as e:
            self.log_error(e)
            resp=ListenCommandResponse()
            resp.sentence=''
            resp.success=False
            self.log_info(f'Response time : {time.time()-time0}')
            return resp

    def log_info(self,msg):
        rospy.loginfo(msg)
    def log_error(self,msg):
        rospy.logerr(msg)
    def log_warn(self,msg):
        rospy.logwarn(msg)
def main():
    node=ListenerNode()
    rospy.spin()
    if node.recognizer.use_noisetorch==True:
        os.popen('noisetorch -u')
        print('noisetorch killed')
if __name__ == '__main__':
    main()