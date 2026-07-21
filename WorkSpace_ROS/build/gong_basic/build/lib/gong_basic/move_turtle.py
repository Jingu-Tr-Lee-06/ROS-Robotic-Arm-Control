import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Move_turtle(Node):
    def __init__(self):
        super().__init__("massage_pub") #노드 이름
        #timer 생성
        self.create_timer(1.0, self.timer_callback) #1초마다 timer_callback 함수 호출
        self.pub = self.create_publisher(Twist, "turtle1/cmd_vel", 10) #토픽 생성
        self.count = 0

        
    def timer_callback(self):
        msg = Twist() #DDS에 보내는 객체 초기화
        msg.linear.x = 0.0 + self.count #Data를 입력
        msg.angular.z =1.0 #Data를 입력
        self.pub.publish(msg) #DDS로 보내는 기능 수행
        self.count += 0.1


def main(args=None):
    rclpy.init(args=args)

    node = M_pub()  # 퍼블리셔 노드 생성

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        # get_logger().info(...) 대신 print 사용!
        print("\nKeyboard Interrupt (SIGINT) - 퍼블리셔를 종료합니다.")
        
    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()

