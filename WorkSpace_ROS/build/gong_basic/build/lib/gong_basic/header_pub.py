import rclpy
from rclpy.node import Node
from std_msgs.msg import Header


class Header_pub(Node):

    def __init__(self):
        super().__init__('header_pub')

        self.pub = self.create_publisher(Header, 'header', 10)

        # 1.0 -> 0.1로 변경 (1초에 10번 호출)
        self.create_timer(0.1, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        msg = Header()
        msg.frame_id = f'time test {self.count}'
        msg.stamp = self.get_clock().now().to_msg()

        self.get_logger().info(
            f'Published Frame ID: {msg.frame_id}, Stamp: {msg.stamp.sec}.{msg.stamp.nanosec}'
        )

        self.pub.publish(msg)
        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = Header_pub()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('\nKeyboard Interrupt (SIGINT) - 퍼블리셔를 종료합니다.')
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()