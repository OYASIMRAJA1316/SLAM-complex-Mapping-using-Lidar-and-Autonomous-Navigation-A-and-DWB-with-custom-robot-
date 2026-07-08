import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription, LaunchService
from launch.actions import DeclareLaunchArgument, OpaqueFunction, GroupAction, IncludeLaunchDescription, ExecuteProcess
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node, PushRosNamespace

def launch_setup(context):
    navigation_package_path = get_package_share_directory('navigation')
   
    sim = LaunchConfiguration('sim', default='false').perform(context)
    use_sim_time = 'true' if sim == 'true' else 'false'

    robot_name = LaunchConfiguration('robot_name', default='').perform(context)

    actions = []
    if robot_name and robot_name != '/':
        actions.append(PushRosNamespace(robot_name))
        
    actions.append(
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', os.path.join(navigation_package_path, 'rviz/navigation.rviz'), '--ros-args', '-p', f'use_sim_time:={use_sim_time}'],
            output='screen'
        )
    )

    rviz_node = GroupAction(actions=actions)

    return [rviz_node]

def generate_launch_description():
    return LaunchDescription([
        OpaqueFunction(function = launch_setup)
    ])

if __name__ == '__main__':
    # 创建一个LaunchDescription对象(create a LaunchDescription object)
    ld = generate_launch_description()

    ls = LaunchService()
    ls.include_launch_description(ld)
    ls.run()
