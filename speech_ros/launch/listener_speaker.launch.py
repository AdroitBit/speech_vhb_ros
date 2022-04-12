from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.actions import DeclareLaunchArgument

def generate_launch_description():
    return LaunchDescription([
        #Node(
        #    package='turtlesim',
        #    namespace='turtlesim1',
        #    executable='turtlesim_node',
        #    name='sim'
        #),
        #Node(
        #    package='turtlesim',
        #    namespace='turtlesim2',
        #    executable='turtlesim_node',
        #    name='sim'
        #),
        #Node(
        #    package='turtlesim',
        #    executable='mimic',
        #    name='mimic',
        #    remappings=[
        #        ('/input/pose', '/turtlesim1/turtle1/pose'),
        #        ('/output/cmd_vel', '/turtlesim2/turtle1/cmd_vel'),
        #    ]
        #),
        DeclareLaunchArgument(name='namespace', default_value='GPSR'),
        DeclareLaunchArgument(name='recog_engine', default_value='vosk'),
        DeclareLaunchArgument(name='vosk_model', default_value='en-us'),
        Node(
            package='speech_ros',
            namespace='<ns>',
            executable='speech_recognizer_node'
        ),
        Node(
            package='speech_ros',
            namespace='<ns>',
            executable='tts_node'
        )
    ])