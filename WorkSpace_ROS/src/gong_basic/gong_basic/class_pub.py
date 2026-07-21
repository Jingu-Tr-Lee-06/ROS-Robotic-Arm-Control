import rclpy
from rclpy.node import Node

class M_pub(Node):
    def __init__(self):
        super().__init__("massage_pub") #노드 이름
        #timer 생성
        self.create_timer(1.0, self.timer_callback) #1초마다 timer_callback 함수 호출
        self.count = 0

        
    def timer_callback(self):
        self.get_logger().info("첫번째 프로그램입니다. %d" % self.count)
        self.count += 1


def main(args=None):
    rclpy.init(args=args) #rmw 활성화

    node = M_pub() #노드 생성

    try:
        rclpy.spin(node) #노드 실행
    except KeyboardInterrupt:
        node.get_logger().info("Keyboard Interrupt (SIGINT)") #Ctrl+C 입력 시 종료
    finally:
        node.destroy_node() #노드 종료


if __name__ == '__main__':
    main()

