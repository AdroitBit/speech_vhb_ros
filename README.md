# speech-ros2
Text to speech and Speech Recognition in ROS.<br>
Give the ability to speak and understand speech to the Robot.


### Dependencies
- [pocketsphinx](https://pypi.org/project/pocketsphinx/)
- espeak
- festival
- pico2wave
- aplay


### Installation
```
mkdir -p ~/speech_ws/src
cd ~/speech_ws/src
git clone -b noetic-devel https://github.com/VeryHardBit/speech-ros2
cd ..
catkin_make
```

### Launch
listener_speaker.launch
  - run speech_recog_node and tts_node
  - arguments
    - tts_type
      - default : pico2wave
      - the value can be pico2wave,festival,espeak
    - recog_engine
      - default : pocketsphinx
    - dict
      - default : cmudict-en-us.dict
      - the value can also be `KU_Robocup-en-us.dict`,`movement-en-us.dict` observe in folder named model in speech_ros package
  - examples
```
$ roslaunch speech_ros listener_speaker.launch

$ roslaunch speech_ros listener_speaker.launch tts_type:=espeak

$ roslaunch speech_ros listener_speaker.launch dict:=KU_Robocup-en-us.dict
```



### Nodes
- speech_recog_node (recog_node.py)
    - create service name `speech_recog_output`
    - use pocketsphinx engine for speech recognition

- tts_node (tts_node.py)
    - create service `tts_input`
    - use pico2wave,espeak,festival engine.This can be chosen in roslaunch



`speech_ros_cli` package is the example of how to write client for these nodes

in `speech_ros` package there is model folder which is speech_recog_node using. You can modify the model there. Such as KU_Robocup-en-us.dict just to make model more specific to drink and greeting.