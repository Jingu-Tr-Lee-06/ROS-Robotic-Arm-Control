import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class M_sub(Node):
    def __init__(self):
        # 1. 부모 클래스(Node) 초기화를 통해 노드 이름을 부여해야 합니다.
        super().__init__("massage_sub")

        # 2. 토픽 구독 (Subscription) 생성
        self.sub = self.create_subscription(String, "massage", self.sub_callback, 10)
        self.count = 0

    def sub_callback(self, msg: String):
        self.get_logger().info(msg.data) # DDS로부터 받은 Data 출력


def main(args=None):
    rclpy.init(args=args)  # rmw 활성화

    node = M_sub()  # 노드 생성

    try:
        rclpy.spin(node)  # 노드 실행
    except KeyboardInterrupt:
        # 이미 셧다운된 경우 print문으로 출력하는 것이 안전합니다.
        print("\nKeyboard Interrupt (SIGINT) - 노드를 종료합니다.")
    finally:
        node.destroy_node()  # 노드 소멸

        # 컨텍스트가 아직 열려있는 경우에만 shutdown 호출
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
