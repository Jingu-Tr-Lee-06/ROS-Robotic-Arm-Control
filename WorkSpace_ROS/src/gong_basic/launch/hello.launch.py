from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # mpub (class_pub 실행 파일을 mpub 라는 이름으로 실행)
        Node(package='gong_basic', executable='class_pub', name='mpub'),
        # tpub (header_pub 실행 파일을 tpub 라는 이름으로 실행)
        Node(package='gong_basic', executable='header_pub', name='tpub'),
        # msub (class_sub 실행 파일을 msub 라는 이름으로 실행)
        Node(package='gong_basic', executable='class_sub', name='msub'),
        # m2sub (class_sub 실행 파일을 m2sub 라는 이름으로 실행)
        Node(package='gong_basic', executable='class_sub', name='m2sub'),
        # mtsub (다중 구독 노드 실행)
        Node(package='gong_basic', executable='mtsub_node', name='mtsub'),
    ])