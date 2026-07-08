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

## Execution Flow for Simulation

#### Phase 1: SLAM Mapping
To map a new environment, run these commands in four separate terminals:

1. **Start Simulation (Terminal 1)**:
   ```bash
   ros2 launch gazebo_simulations gazebo.launch.py
   ```
2. **Start SLAM (Terminal 2)**:
   ```bash
   ros2 launch slam slam.launch.py sim:=true
   ```
3. **Launch RViz for SLAM Visualization (Terminal 3)**:
   ```bash
   ros2 launch slam rviz_slam.launch.py sim:=true
   ```
4. **Drive the Robot (Terminal 4)**:
   ```bash
   ros2 run teleop_twist_keyboard teleop_twist_keyboard
   ```
*(After exploring the environment, use the RViz SLAM Toolbox panel to serialize and save your map!)*

#### Phase 2: Navigation
Once you have saved a map, you can use the Navigation stack to autonomously move the robot.

1. **Start Simulation (Terminal 1)**:
   ```bash
   ros2 launch gazebo_simulations gazebo.launch.py
   ```
2. **Start Navigation (Terminal 2)**:
   ```bash
   ros2 launch navigation navigation.launch.py sim:=true map:=your_map_name
   ```
3. **Launch RViz for Navigation (Terminal 3)**:
   ```bash
   ros2 launch navigation rviz_navigation.launch.py sim:=true
   ```
*(Use the "2D Pose Estimate" tool in RViz to tell the robot where it is on the map, then use "2D Nav Goal" to tell it where to drive!)*
