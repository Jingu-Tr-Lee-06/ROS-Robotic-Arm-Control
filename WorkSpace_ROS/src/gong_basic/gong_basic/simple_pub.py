import rclpy
from rclpy.node import Node



def timer_callback():
    print("첫번째 프로그램입니다.")


def main(args=None):
    rclpy.init(args=args) #rmw 활성화
    node = Node("massage_pub") #노드 이름

    #timer 생성
    node.create_timer(1.0, timer_callback) #1초마다 timer_callback 함수 호출

    try:
        rclpy.spin(node) #노드 실행
    except KeyboardInterrupt:
        node.get_logger().info("Keyboard Interrupt (SIGINT)") #Ctrl+C 입력 시 종료
    finally:
        node.destroy_node() #노드 종료


if __name__ == '__main__':
    main()

