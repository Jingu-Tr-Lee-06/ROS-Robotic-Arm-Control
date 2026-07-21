import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/leeji/ROS-Robotic-Arm-Control/WorkSpace_ROS/install/gong_basic'
