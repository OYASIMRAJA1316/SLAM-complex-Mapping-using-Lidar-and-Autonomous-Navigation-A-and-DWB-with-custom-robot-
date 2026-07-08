#!/usr/bin/env python3
# encoding: utf-8
# @data:2022/11/23
# @author:aiden
import os
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
from slam_toolbox.srv import SaveMap

class MapSaveNode(Node):
    def __init__(self, name):
        rclpy.init()
        super().__init__(name)
        self.create_service(SaveMap, '/slam_toolbox/save_map', self.save_srv_callback)

        self.create_service(Trigger, '~/init_finish', self.get_node_state)
        self.get_logger().info('\033[1;32m%s\033[0m' % 'start')

    def get_node_state(self, request, response):
        response.success = True
        return response

    def save_srv_callback(self, request, response):
        map_name = request.name.data
        if not map_name:
            map_name = "map"
        self.get_logger().info('\033[1;32m%s\033[0m' % f"Saving map as: {map_name}")
        save_dir = os.path.expanduser('~/ros2_ws/src/src/slam/maps')
        os.makedirs(save_dir, exist_ok=True)
        os.system(f'cd {save_dir} && ros2 run nav2_map_server map_saver_cli -f "{map_name}" --ros-args -p map_subscribe_transient_local:=true')
        response.result = 0
        return response

def main():
    node = MapSaveNode('map_save_node')
    rclpy.spin(node)
    rclpy.shutdown()
    node.destroy_node()
 
if __name__ == "__main__":
    main()
