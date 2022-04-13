import os
import re
import threading

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Empty
from ament_index_python.packages import get_package_share_directory
from speech_ros_interfaces.srv import SpeechRecog

pkg_dir=get_package_share_directory('speech_ros')

class VOSK_Recognizer():
    def __init__(self,wtf=False):#setup function
        from vosk import Model, KaldiRecognizer
        import speech_recognition as sr #use as a micrphone listener since This module doesn't have vosk yet

        self.model = Model(get_package_share_directory('pocketsphinx_ros')+'/model/en-us/en-us')
        self.recognizer = KaldiRecognizer(self.model)

        #create listener using speech_recognition
        listener=sr.Recognizer()
        print('Adjusting listener for ambient noise...')
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source,duration=1)
        listener.pause_threshold = 0.8
        print('Listener Adjusted')
        print(f'Energy threshold => {listener.energy_threshold}')
        self.listener=listener

    def sentence_mapping(self,s):
        config_path=pkg_dir+'/config/sentence-mapper'
        data=yaml.safe_load(open(config_path+'/vosk-GPSR.yaml').read())
        if data is None:
            return s
        for b,a in data.items():
            for ai in a:
                s=s.replace(ai,b)
        return s
    def listen(self):#return binary wav data
        rospy.loginfo('Listening...')
        with sr.Microphone() as source:
            audio = self.listener.listen(source)
        data=audio.get_wav_data(convert_rate=16000,convert_width=2)
        f=open('/tmp/speech.wav','wb')
        f.write(data)
        f.close()
        if self.record_input==True:
            path=pkg_dir+'/recorded-audios'
            self.save_audio(audio,path,self.record_ext)


        rospy.loginfo('Recognizing...')
        self.recognizer.AcceptWaveform(data)
        sentence=json.loads(self.recognizer.Result())['text']
        return sentence
#class Google_Recognizer():

        


class PocketSphinx_Recognizer():
    def __init__(self,wtf=False):#WIP likely to be removed
        from pocketsphinx import LiveSpeech
        model_path=get_package_share_directory('pocketsphinx_ros')+'/model'
        speech = LiveSpeech(
            verbose=False,
            sampling_rate=16000,
            buffer_size=2048,
            no_search=False,
            full_utt=False,
            hmm=os.path.join(model_path, 'en-us'),
            lm=os.path.join(model_path, 'en-us.lm.bin'),
            dic=os.path.join(model_path, 'KU_Robocup-en-us.dict')
        )
        for phrase in speech:
            #using in noetic branch
            #return map_phrase(str(phrase)) 
            return str(phrase)



class SpeechRecognizerNode(Node):
    def __init__(self):
        super().__init__('speech_recognizer_node')
        #self.srv_start= self.create_service(SpeechRecog, 'recognizer/start',self.srv_recog_callback)
        #self.sub_start=self.create_subscription(Empty, 'recognizer/foxy/start',self.sub_recog_callback,10)
        
        self.declare_parameter(
            namespace='',
            parameters=[
                ('recog_engine','vosk')
            ]
        )

        if str(self.get_parameter('recog_engine').value)=='vosk':
            self.recognizer=VOSK_Recognizer()
        self.recognizer_srv= self.create_service(SpeechRecog, '/<ns>/speech/speak',self.srv_recog_callback)
    def srv_recog_callback(self,req):
        rospy.loginfo('Recognizing...')

        return self.recognizer.listen()


def main(args=None):
    rclpy.init(args=args)
    node = SpeechRecognizerNode()
    print("Send request to .... for speech recognition activation.")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()