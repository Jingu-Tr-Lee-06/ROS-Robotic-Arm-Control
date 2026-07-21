import rclpy
from rclpy.node import Node
from std_msgs.msg import Header


class HeaderSub(Node):

    def __init__(self):
        super().__init__('header_sub')

        # 'header' 토픽을 구독하도록 설정 (메시지 타입: Header)
        self.sub = self.create_subscription(
            Header, 'header', self.sub_callback, 10
        )

    def sub_callback(self, msg: Header):
        # Header 메시지 안의 frame_id와 stamp(초.나노초) 정보 출력
        self.get_logger().info(
            f'[header_sub] Frame ID: {msg.frame_id} | Stamp: {msg.stamp.sec}.{msg.stamp.nanosec}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = HeaderSub()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('\nKeyboard Interrupt (SIGINT) - 서브스크라이버를 종료합니다.')
    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()