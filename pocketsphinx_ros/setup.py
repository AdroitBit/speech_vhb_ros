from setuptools import setup
from ament_index_python.packages import get_package_share_directory
from glob import glob


package_name = 'pocketsphinx_ros'
setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/'+package_name+'/glados-pre-sound',glob('glados-pre-sound/*.wav')),
        ('share/' + package_name, glob('launch/*.launch.py'))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='veryhardbit',
    maintainer_email='yanothaic15@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'test = pocketsphinx_ros.test:main',
            'speech_recog_pub = pocketsphinx_ros.speech_recog_pub:main',
            'tts = pocketsphinx_ros.tts:main',
            'cmd_vel = pocketsphinx_ros.cmd_vel:main',
        ]
    }
)