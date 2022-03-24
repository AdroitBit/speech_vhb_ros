# pocketsphinx-ros2
The pocketsphinx kinda not working well in ROS noetic because the ros noetic use multithread for service and client.

And LiveSpeech() only work in main thread.

Kinda workaround here.But I managed it to work.


## Dependencies
- Just consider it like foxy version's dependencies.


## Installation
```
source /opt/ros/noetic/setup.bash
mkdir -p ~/ros_noetic_thing/pocketsphinx_ws/src
cd ~/ros_noetic_thing/pocketsphinx_ws/src
git clone -b noetic-devel https://github.com/VeryHardBit/pocketsphinx-ros2
cd ..
catkin_make
```

## Launch 




## Nodes
- pocketsphinx_speech_srv_node (speech_recog_srv.py)
    - create service name `speech_recog_output`
    - to run `$ rosrun pocketsphinx_ros speech_recog_srv`
    - to test `$ rosservice call /speech_recog_output pocketsphinx_ros_interfaces/srv/SpeechRecog {}`

- pocketsphinx_tts_srv_node (tts_srv.py)
    - slightly different foxy version.


## Running (for speech recognition)

```
$ source /opt/ros/noetic/setup.bash && \
  source ~/ros_noetic_thing/pocketsphinx_ws/devel/setup.bash && \
  rosrun pocketsphinx_ros speech_recog_node.py
```

## Running (for tts)
```
$ source /opt/ros/noetic/setup.bash && \
  source ~/ros_noetic_thing/pocketsphinx_ws/devel/setup.bash && \
  rosrun pocketsphinx_ros tts_node.py
```

## State testing
```
$ source /opt/ros/noetic/setup.bash && \
  source ~/ros_noetic_thing/pocketsphinx_ws/devel/setup.bash && \
  rosrun state_test test_cli.py
```


## testing
[robot come here]

Hello,What would you like to drink?

[Drink name]

Ok,I will be back with your drink.

Here is your drink.

[Thank you]

You're welcome.
