# speech-ros2



## Dependencies
- Just consider it like foxy version's dependencies.


## Installation
```
mkdir -p ~/ros_noetic_thing/speech_ws/src
cd ~/ros_noetic_thing/speech_ws/src
git clone -b noetic-devel https://github.com/VeryHardBit/speech-ros2
cd ..
catkin_make
```

## Launch
listener_speaker.launch
  - run speech_recog_node and tts_node
  - arguments
    - tts_type
      - default : pico2wave
      - can either be pico2wave,festival,espeak
    - recog_engine
      - default : pocketsphinx
  - examples
```
$ roslaunch speech_ros listener_speaker.launch

$ roslaunch speech_ros listener_speaker.launch tts_type:=espeak
```



## Nodes
- speech_recog_node (recog_node.py)
    - create service name `speech_recog_output`
    - use pocketsphinx engine for speech recognition

- tts_node (tts_node.py)
    - create service `tts_input`
    - use pico2wave,espeak,festival engine.This can be chosen in roslaunch



`speech_ros_cli` package is the example of how to write client for these nodes