from setuptools import setup

package_name = 'speech_vhb_ros'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='veryhardbit',
    maintainer_email='yanothaic8@gmaill.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_node = speech_vhb_ros.my_node:main',
            'speaker_node = speech_vhb_ros.speaker_node:main',
            'listener_node = speech_vhb_ros.listener_node:main',
        ],
    },
)
