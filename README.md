# Alpha Robot Simulation & Navigation Stack

This repository contains the complete ROS 2 Jazzy software stack for the Alpha Robot. It includes the robot description (URDF), Gazebo Harmonic simulations, SLAM (mapping), and Nav2 autonomous navigation.

## Repository Structure
- `alpha_description_new`: URDF, meshes, and robot state publishers.
- `gazebo_simulations`: Gazebo Harmonic worlds, environment models, and launch configurations.
- `slam`: SLAM Toolbox integration for 2D map generation.
- `navigation`: Nav2 stack configurations, costmaps, and planners for autonomous point-to-point navigation.

## Prerequisites
- **ROS 2 Jazzy**
- **Gazebo Harmonic** (`ros-jazzy-ros-gz`)
- **Nav2** (`ros-jazzy-navigation2`, `ros-jazzy-nav2-bringup`)
- **SLAM Toolbox** (`ros-jazzy-slam-toolbox`)

## 1. Setup & Installation
```bash
# 1. Create a new ROS 2 workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# 2. Clone this repository inside the src folder
git clone https://github.com/OYASIMRAJA1316/SLAM-complex-Mapping-using-Lidar-and-Autonomous-Navigation-A-and-DWB-with-custom-robot-.git alpha_robot_stack

# Install dependencies using rosdep
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y

# Build the workspace
colcon build --symlink-install --packages-select alpha_description_new gazebo_simulations slam navigation

# Source the workspace
source install/setup.bash
```

## 2. Gazebo Simulation
Launch the Alpha robot inside the simulated warehouse environment in Gazebo Harmonic.
```bash
ros2 launch gazebo_simulations gazebo.launch.py sim:=true
```

## 3. Mapping (SLAM)
To create a new map of the environment, launch the SLAM Toolbox.
```bash
# In a new terminal (ensure simulation is running)
source install/setup.bash
ros2 launch slam slam.launch.py sim:=true
```
*Drive the robot around the environment (using teleop or rviz) until the map is fully generated.*

To save the map:
```bash
ros2 run nav2_map_server map_saver_cli -f ~/ros2_ws/src/alpha_robot_stack/navigation/maps/my_new_map
```

## 4. Navigation (Nav2)
To autonomously navigate the robot using a pre-saved map:
```bash
# In a new terminal (ensure simulation is running)
source install/setup.bash
ros2 launch navigation navigation.launch.py sim:=true
```
*Use the "2D Pose Estimate" tool in RViz to initialize the robot's location, then use the "Nav2 Goal" tool to command the robot to drive.*
