import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription, LaunchService
from launch.actions import DeclareLaunchArgument, OpaqueFunction, GroupAction, IncludeLaunchDescription, ExecuteProcess

from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def launch_setup(context):

    sim = LaunchConfiguration('sim', default='false').perform(context)
    use_sim_time = True if sim == 'true' else False

    slam_package_path = get_package_share_directory('slam')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', os.path.join(slam_package_path, 'rviz/slam.rviz'), '--ros-args', '-p', f'use_sim_time:={sim}'],
        output='screen'
    )

    return [rviz_node]

def generate_launch_description():
    sim_arg = DeclareLaunchArgument('sim', default_value='false')
    return LaunchDescription([
        sim_arg,
        OpaqueFunction(function = launch_setup)
    ])

if __name__ == '__main__':
    # 创建一个LaunchDescription对象(create a LaunchDescription object)
    ld = generate_launch_description()

    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()
