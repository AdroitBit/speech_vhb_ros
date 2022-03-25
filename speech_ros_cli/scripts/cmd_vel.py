import rospy
from geometry_msgs.msg import Twist

from speech_ros.srv import SpeechRecog,SpeechRecogResponse
import time



def listen():
    rospy.wait_for_service('recognizer/start')
    try:
        start_recog = rospy.ServiceProxy('recognizer/start', SpeechRecog)
        resp=start_recog()
        return resp.sentence
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

rospy.init_node('talker', anonymous=True)
pub_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
while not rospy.is_shutdown():
    o=Twist()
    o.linear.x=o.linear.y=o.linear.z=o.angular.x=o.angular.y=o.angular.z=0
    msg=listen()
    print(msg)
    if 'forward' in msg or 'go' in msg:
        o.linear.x+=0.1
    elif 'backward' in msg or 'retreat' in msg:
        o.linear.x-=0.1
    elif 'left' in msg:
        o.angular.z+=0.2
    elif 'right' in msg:
        o.angular.z-=0.2
    elif 'stop' in msg:
        o.linear.x=0
    pub_vel.publish(o)
    time.sleep(0.1)

