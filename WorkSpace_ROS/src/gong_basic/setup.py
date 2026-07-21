from setuptools import find_packages, setup
from glob import glob
import os
from setuptools import find_packages, setup

package_name = 'gong_basic'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob(os.path.join('launch', '*launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='leeji',
    maintainer_email='gidwjd2022@gmail.com',
    description='Kongju University ROS2 Basic Library',
    license='Apache 2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "simple_pub = gong_basic.simple_pub:main",
            "class_pub = gong_basic.class_pub:main",
            "class_sub = gong_basic.class_sub:main",
            "header_pub = gong_basic.header_pub:main",
            "header_sub = gong_basic.header_sub:main",
            "mtsub_node = gong_basic.mtsub_node:main",
            "move_turtle = gong_basic.move_turtle:main",
        ],
    },
)
