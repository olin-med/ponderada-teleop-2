import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TeleopTurtleBot(Node):
    def __init__(self):
        super().__init__('teleop_turtlebot')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10
        )
        self.subscription  # prevent unused variable warning

    def cmd_vel_callback(self, msg):
        self.publisher_.publish(msg)
        self.get_logger().info(f'Received velocity command: linear={msg.linear.x}, angular={msg.angular.z}')

def main(args=None):
    rclpy.init(args=args)
    teleop_turtlebot = TeleopTurtleBot()
    rclpy.spin(teleop_turtlebot)
    teleop_turtlebot.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
