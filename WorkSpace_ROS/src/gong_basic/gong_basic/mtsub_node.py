import rclpy
from rclpy.node import Node
from std_msgs.msg import Header, String


class MTSub(Node):

    def __init__(self):
        super().__init__('mtsub')

        # 1. message 토픽 구독 (String 타입)
        self.sub_msg = self.create_subscription(
            String, 'massage', self.msg_callback, 10
        )

        # 2. header(time) 토픽 구독 (Header 타입)
        self.sub_time = self.create_subscription(
            Header, 'header', self.time_callback, 10
        )

    def msg_callback(self, msg: String):
        self.get_logger().info(f'[mtsub] Recv Message: {msg.data}')

    def time_callback(self, msg: Header):
        self.get_logger().info(
            f'[mtsub] Recv Time Stamp: {msg.stamp.sec}.{msg.stamp.nanosec}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = MTSub()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('\nKeyboard Interrupt (SIGINT) - mtsub 노드를 종료합니다.')
    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()