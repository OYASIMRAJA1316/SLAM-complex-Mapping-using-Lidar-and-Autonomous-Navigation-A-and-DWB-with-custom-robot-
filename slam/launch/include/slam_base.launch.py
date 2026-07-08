import os
from ament_index_python.packages import get_package_share_directory

from launch_ros.actions import LifecycleNode
from launch_ros.event_handlers import OnStateTransition
from launch_ros.events.lifecycle import ChangeState
from lifecycle_msgs.msg import Transition
from launch.actions import DeclareLaunchArgument, OpaqueFunction, EmitEvent, RegisterEventHandler, LogInfo
from launch.events import matches_action
from launch import LaunchDescription, LaunchService
from launch.substitutions import LaunchConfiguration
from nav2_common.launch import RewrittenYaml

def launch_setup(context):

    enable_save = LaunchConfiguration('enable_save', default='true').perform(context)
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    use_sim_time_bool = True if use_sim_time.perform(context) == 'true' else False
    map_frame = LaunchConfiguration('map_frame', default='map')
    odom_frame = LaunchConfiguration('odom_frame', default='odom')
    base_frame = LaunchConfiguration('base_frame', default='base_footprint')
    scan_topic = LaunchConfiguration('scan_topic', default='scan')

    enable_save_arg = DeclareLaunchArgument('enable_save', default_value=enable_save)
    use_sim_time_arg = DeclareLaunchArgument('use_sim_time', default_value=use_sim_time)
    map_frame_arg = DeclareLaunchArgument('map_frame', default_value=map_frame)
    odom_frame_arg = DeclareLaunchArgument('odom_frame', default_value=odom_frame)
    base_frame_arg = DeclareLaunchArgument('base_frame', default_value=base_frame)
    scan_topic_arg = DeclareLaunchArgument('scan_topic', default_value=scan_topic)

    slam_package_path = get_package_share_directory('slam')

    slam_params = RewrittenYaml(
        source_file=os.path.join(slam_package_path, 'config/slam.yaml'),
        param_rewrites={
            'use_sim_time': use_sim_time,
            'map_frame': map_frame,
            'odom_frame': odom_frame,
            'base_frame': base_frame,
            'scan_topic': scan_topic,
            },
        convert_types=True
    )

    remappings=[
        ('/tf', 'tf'),
        ('/tf_static', 'tf_static'),
        ('/map', 'map'),
        ('/map_metadata', 'map_metadata'),
    ]
    if enable_save == 'false':
        remappings.append(('/slam_toolbox/save_map', '/save_map'))

    sync_node = LifecycleNode(package='slam_toolbox',
         executable='sync_slam_toolbox_node',
         name='slam_toolbox',
         output='screen',
         namespace='',
         parameters=[
           slam_params,
           {'use_sim_time': use_sim_time_bool}
         ],
         remappings=remappings
    )

    configure_event = EmitEvent(
        event=ChangeState(
            lifecycle_node_matcher=matches_action(sync_node),
            transition_id=Transition.TRANSITION_CONFIGURE
        )
    )

    activate_event = RegisterEventHandler(
        OnStateTransition(
            target_lifecycle_node=sync_node,
            start_state="configuring",
            goal_state="inactive",
            entities=[
                LogInfo(msg="[LifecycleLaunch] Slamtoolbox node is activating."),
                EmitEvent(event=ChangeState(
                    lifecycle_node_matcher=matches_action(sync_node),
                    transition_id=Transition.TRANSITION_ACTIVATE
                ))
            ]
        )
    )

    return [
        enable_save_arg,
        use_sim_time_arg,
        map_frame_arg,
        odom_frame_arg,
        base_frame_arg,
        scan_topic_arg,
        sync_node,
        configure_event,
        activate_event
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
