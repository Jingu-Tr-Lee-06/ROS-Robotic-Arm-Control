# import rclpy
# from rclpy.node import Node
# # String 대신 geometry_msgs.msg의 Twist를 import합니다.
# from geometry_msgs.msg import Twist


# class Move_turtle(Node):
#     def __init__(self):
#         super().__init__("move_turtle")  # 노드 이름 (원하시는 이름으로 설정)
#         # timer 생성 (1초마다 timer_callback 함수 호출)
#         self.create_timer(1.0, self.timer_callback)
#         # 토픽 생성 (geometry_msgs/msg/Twist 타입)
#         self.pub = self.create_publisher(Twist, "turtle1/cmd_vel", 10)
#         self.count = 0.0

#     def timer_callback(self):
#         msg = Twist()  # Twist 메시지 객체 생성
#         msg.linear.x = 0.0 + self.count  # 직진 속도 증가
#         msg.angular.z = 1.0  # 회전 속도 설정
#         self.pub.publish(msg)  # turtle1/cmd_vel 토픽으로 메시지 발행
#         self.count += 0.1


# def main(args=None):
#     rclpy.init(args=args)

#     node = Move_turtle()  # 퍼블리셔 노드 생성

#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         print("\nKeyboard Interrupt (SIGINT) - 퍼블리셔를 종료합니다.")
#     finally:
#         node.destroy_node()
#         if rclpy.ok():
#             rclpy.shutdown()


# if __name__ == "__main__":
#     main()

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math  # 코사인 함수와 pi를 사용하기 위해 import

class MoveTurtleGeometric(Node):
    def __init__(self):
        super().__init__("move_turtle_geometric")
        
        # 주기를 짧게 설정하여 (0.01초) 움직임을 아주 매끄럽게 만듭니다.
        self.timer_period = 0.01  # seconds
        self.create_timer(self.timer_period, self.timer_callback)
        
        self.pub = self.create_publisher(Twist, "turtle1/cmd_vel", 10)
        
        # 시간 경과를 기록하기 위한 변수
        self.time_counter = 0.0

    def timer_callback(self):
        msg = Twist()
        
        # 1. 직진 속도 (Linear Velocity): 고정값
        # 너무 빠르면 화면 밖으로 금방 나가므로 적당히 설정합니다.
        msg.linear.x = 2.5
        
        # 2. 각속도 (Angular Velocity): 코사인 함수 적용
        # 시간이 지남에 따라 회전 속도가 +와 -를 오가며 기하학적 패턴을 만듭니다.
        # 아래 식의 숫자를 바꾸면 패턴의 모양이 바뀝니다.
        # 기본값: math.cos(self.time_counter * (주기 조절)) * (최대 각속도 조절)
        # 0.5: 패턴의 반복 횟수 조절, 4.0: 회전 반경의 변화폭 조절
        frequency_factor = 0.5
        amplitude_factor = 4.0
        
        msg.angular.z = math.cos(self.time_counter * frequency_factor) * amplitude_factor
        
        # 메시지 발행
        self.pub.publish(msg)
        
        # 시간 변수 업데이트
        self.time_counter += self.timer_period


def main(args=None):
    rclpy.init(args=args)
    
    # 노드 생성
    node = MoveTurtleGeometric()
    
    # turtlesim 화면의 배경색을 바꾸거나 펜 설정을 바꾸면 더 기하학적인 느낌을 줄 수 있습니다.
    # (이 노드에서는 구현하지 않았지만, 필요시 서비스(SetPen)를 호출하여 구현 가능합니다.)

    print("turtlesim 기하학적 문양 그리기 노드 시작...")
    print("패턴을 그리며 움직입니다. (종료: Ctrl+C)")

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt - 노드를 종료합니다.")
    finally:
        # 종료 시 노드 파괴 및 ROS 통신 종료
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()