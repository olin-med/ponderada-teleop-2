#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import cv2
import threading
import time
import signal
import os

app = Flask(__name__)
CORS(app)  # Adiciona suporte a CORS

class TeleopNode(Node):

    def __init__(self):
        super().__init__('teleop_node')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.linear_velocity = 0.2
        self.angular_velocity = 0.5
        self.current_linear_velocity = 0.0
        self.current_angular_velocity = 0.0
        self.moving = False
        self.direction = None
        self.thread = threading.Thread(target=self.publish_cmd_vel)
        self.thread.start()

    def publish_cmd_vel(self):
        while rclpy.ok():
            if self.moving:
                msg = Twist()
                if self.direction == 'up':
                    msg.linear.x = self.linear_velocity
                elif self.direction == 'down':
                    msg.linear.x = -self.linear_velocity
                elif self.direction == 'left':
                    msg.angular.z = self.angular_velocity
                elif self.direction == 'right':
                    msg.angular.z = -self.angular_velocity
                self.current_linear_velocity = msg.linear.x
                self.current_angular_velocity = msg.angular.z
                self.publisher_.publish(msg)
            else:
                self.current_linear_velocity = 0.0
                self.current_angular_velocity = 0.0
            time.sleep(0.1)

    def set_direction(self, direction):
        self.direction = direction
        self.moving = True

    def stop(self):
        self.moving = False

teleop_node = None

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    action = data['action']
    direction = data['direction']
    if action == 'start':
        teleop_node.set_direction(direction)
    elif action == 'stop':
        teleop_node.stop()
    return jsonify({"status": "success"})

@app.route('/speed', methods=['GET'])
def get_speed():
    return jsonify({
        "linear_velocity": teleop_node.current_linear_velocity,
        "angular_velocity": teleop_node.current_angular_velocity
    })

@app.route('/shutdown', methods=['POST'])
def shutdown():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({"status": "shutting down"})

def gen_frames():  # Gera quadros da webcam
    cap = cv2.VideoCapture(0)
    while True:
        start_time = time.time()
        success, frame = cap.read()
        if not success:
            break
        else:
            end_time = time.time()
            latency = (end_time - start_time) * 1000  # Calcula a latência em milissegundos
            # Adiciona a latência como texto na imagem
            cv2.putText(frame, f'Latency: {latency:.2f} ms', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def main(args=None):
    rclpy.init(args=args)
    global teleop_node
    teleop_node = TeleopNode()
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        pass
    rclpy.spin(teleop_node)
    teleop_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
