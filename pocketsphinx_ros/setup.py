from setuptools import setup

package_name = 'pocketsphinx_ros'

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
    maintainer_email='yanothaic15@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'test = pocketsphinx_ros.test:main',
            'listen_and_publish = pocketsphinx_ros.listen_and_publish:main',
            'launcher = pocketsphinx_ros.launcher:main',
        ],
    },
)
