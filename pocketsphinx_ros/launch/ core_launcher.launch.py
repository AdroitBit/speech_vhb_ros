#launch speech recognition node,launch tts node

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    #return LaunchDescription([
    #    launch.actions.DeclareLaunchArgument(
    #        'node_prefix',
    #        default_value=[launch.substitutions.EnvironmentVariable('USER'), '_'],
    #        description='Prefix for node names'),
    #    launch_ros.actions.Node(
    #        package='demo_nodes_cpp', executable='talker', output='screen',
    #        name=[launch.substitutions.LaunchConfiguration('node_prefix'), 'talker']),
    #])
    ld=LaunchDescription()
    speech_recog_node=Node(
        package='pocketsphinx_ros',
        executable='speech_recog_pub'
    )

    tts_node=Node(
        package='pocketsphinx_ros',
        executable='tts'
    )

    ld.add_action(speech_recog_node)
    ld.add_action(tts_node)

    return ld