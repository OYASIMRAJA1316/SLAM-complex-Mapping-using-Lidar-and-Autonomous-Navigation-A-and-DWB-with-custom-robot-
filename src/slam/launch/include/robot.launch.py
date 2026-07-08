import os
from ament_index_python.packages import get_package_share_directory

from launch_ros.actions import PushRosNamespace
from launch import LaunchDescription, LaunchService
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, GroupAction, OpaqueFunction, TimerAction

def launch_setup(context):
    sim = LaunchConfiguration('sim', default='true').perform(context)
    use_joy = LaunchConfiguration('use_joy', default='true').perform(context)
    use_depth_camera = LaunchConfiguration('use_depth_camera', default='false')
    master_name = LaunchConfiguration('master_name', default='/').perform(context)
    robot_name = LaunchConfiguration('robot_name', default='/').perform(context)
    depth_camera_name = LaunchConfiguration('depth_camera_name', default='depth_cam').perform(context)
    action_name = LaunchConfiguration('action_name', default='init').perform(context)

    sim_arg = DeclareLaunchArgument('sim', default_value=sim)
    master_name_arg = DeclareLaunchArgument('master_name', default_value=master_name)
    robot_name_arg = DeclareLaunchArgument('robot_name', default_value=robot_name)
    depth_camera_name_arg = DeclareLaunchArgument('depth_camera_name', default_value=depth_camera_name)
    use_joy_arg = DeclareLaunchArgument('use_joy', default_value=use_joy)
    use_depth_camera_arg = DeclareLaunchArgument('use_depth_camera', default_value=use_depth_camera)
    action_name_arg = DeclareLaunchArgument('action_name', default_value=action_name)

    max_linear_sim = '0.7'
    max_linear = '0.2'
    max_angular_sim = '3.5'
    max_angular = '0.5'

    topic_prefix = '' if robot_name == '/' or not robot_name else '/%s'%robot_name
    frame_prefix = '' if robot_name == '/' or not robot_name else '%s/'%robot_name
    use_namespace = 'false' if robot_name == '/' or not robot_name else 'true'    
    namespace = '' if robot_name == '/' or not robot_name else robot_name
    use_sim_time = 'true' if sim == 'true' else 'false'

    map_frame = '{}map'.format(frame_prefix) if robot_name == master_name else '{}/map'.format(master_name)
    cmd_vel_topic = '{}/cmd_vel'.format(topic_prefix) if sim == 'true' else '{}/controller/cmd_vel'.format(topic_prefix)
    scan_raw = '{}/scan_raw'.format(topic_prefix)
    scan_topic = '{}/scan'.format(topic_prefix)
    odom_frame = '{}odom'.format(frame_prefix)
    base_frame = '{}base_footprint'.format(frame_prefix)
    lidar_frame = '{}lidar_frame'.format(frame_prefix)
    imu_frame = '{}imu_link'.format(frame_prefix)

    bringup_actions = []
    bringup_launch = GroupAction(actions=bringup_actions)

    return [sim_arg, 
            master_name_arg,
            robot_name_arg, 
            depth_camera_name_arg,
            use_joy_arg,
            use_depth_camera_arg,
            action_name_arg,
            bringup_launch,
            ]

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
