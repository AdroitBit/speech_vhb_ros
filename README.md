# pocketsphinx-ros2
Please read. I really put my soul into it.

This package also provided in noetic version. But It's quite tricky because It requires ros foxy version.

The reason is that pocketsphinx can't work with ROS noetic. Because of the noetic used multi-thread for service and client.

But pocketsphinx can't work in multi-thread.Due to signal module that they use.

But then ROS foxy working fine.No problem.That is the workaround for us.



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

#You still need foxy version tho.
source /opt/ros/foxy/setup.bash
mkdir -p ~/ros_foxy_thing/pocketsphinx_ws/src
cd ~/ros_foxy_thing/pocketsphinx_ws/src
git clone -b foxy-devel https://github.com/VeryHardBit/pocketsphinx-ros2
cd ..
colcon build
```




## Nodes
- pocketsphinx_speech_srv_node (speech_recog_srv.py)
    - create service name `speech_recog_output`
    - to run `$ rosrun pocketsphinx_ros speech_recog_srv`
    - to test `$ rosservice call /speech_recog_output pocketsphinx_ros_interfaces/srv/SpeechRecog {}`

- pocketsphinx_tts_srv_node (tts_srv.py)
    - slightly different foxy version.


## Running (for speech recognition)

```
#1st terminal
$ source /opt/ros/foxy/setup.bash && \
  source ~/ros_foxy_thing/pocketsphinx_ws/install/setup.bash && \
  ros2 run pocketsphinx_ros speech_recog_srv

#2nd terminal
$ source /opt/ros/noetic/setup.bash && \
  source ~/ros_noetic_thing/pocketsphinx_ws/devel/setup.bash && \
  rosrun pocketsphinx_ros speech_recog_srv.py
```
As mentioned in foxy version.

That foxy's node can be requested by creating the "file".

So That noetic's node will create that "file" whenever It's requested.

This is how it works step by step.
1. noetic node get requested by service name `recognizer/start`
2. noetic node will create the file "/tmp/pocketsphinx_ros_starter.txt"
3. foxy node always wait for that file.Meet that file.Then start speech recognition. Then send that output to other file "/tmp/pocketsphinx_ros_comm.txt"
4. noetic node always wait for "/tmp/pocketsphinx_ros_comm.txt"

## Running (for tts)
```
$ source /opt/ros/noetic/setup.bash && \
  source ~/ros_noetic_thing/pocketsphinx_ws/devel/setup.bash && \
  rosrun pocketsphinx_ros tts_srv.py
```


## testing
[robot come here]

Hello,What would you like to drink?

[Drink name]

Ok,I will be back with your drink.

Here is your drink.

[Thank you]

You're welcome.
