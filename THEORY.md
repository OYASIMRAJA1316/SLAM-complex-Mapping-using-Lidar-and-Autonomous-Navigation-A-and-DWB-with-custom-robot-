# Alpha Robot Pipeline Theory

This document explains the architectural theory and data flow of the Alpha Robot simulation and navigation pipeline.

## 1. Robot Description (`alpha_description_new`)
The robot's physical structure, joints, and sensor placements are defined using URDF (Unified Robot Description Format) and Xacro. 
- **`robot_state_publisher`**: Reads the URDF and broadcasts the static and dynamic transforms (`tf2`) of the robot's links. This allows all other nodes to know exactly where the Lidar is relative to the robot's base frame (`base_footprint`).

## 2. Simulation (`gazebo_simulations`)
We use **Gazebo Harmonic** as the physics engine to replicate real-world environments. 
- **`ros_gz_bridge`**: Acts as a translator between Gazebo's internal transport system and ROS 2 topics. It bridges simulated Lidar scans (`/scan`), odometry (`/odom`), and clock signals (`/clock`) into ROS 2, while forwarding velocity commands (`/cmd_vel`) from ROS 2 back to Gazebo's simulated motors.
- **Mecanum Drive**: The robot operates on a holonomic mecanum drive, meaning it can strafe sideways in addition to driving forward and rotating.

## 3. Mapping (`slam`)
We use **SLAM Toolbox** (Simultaneous Localization and Mapping) to build a 2D occupancy grid map of the environment.
- SLAM takes the simulated Lidar scans (`/scan`) and pairs them with the robot's estimated movement (`/odom`).
- By comparing how the laser points shift as the robot moves, SLAM corrects the odometry drift and mathematically maps the environment, publishing a live map to the `/map` topic.
- A map saver node takes this live occupancy grid and saves it as a `.yaml` and `.pgm` image file.

## 4. Navigation (`navigation`)
The **Nav2** stack orchestrates autonomous movement. It consists of several interconnected systems:

### A. Localization (AMCL)
- **AMCL (Adaptive Monte Carlo Localization)** loads the static map we saved previously.
- It scatters thousands of "particles" (guesses of where the robot might be) across the map.
- As the robot receives live Lidar scans, AMCL compares those scans against the static map. Particles that match the walls survive; particles that hit empty space die.
- Because Alpha uses a Mecanum drive, AMCL uses an **OmniMotionModel** to account for horizontal slippage.

### B. Costmaps
Costmaps convert the static map and live Lidar obstacles into "costs" to keep the robot safe.
- **Global Costmap**: Uses the static map. It inflates the walls to create a buffer zone so the planner plots routes down the center of aisles.
- **Local Costmap**: Uses live Lidar data to detect dynamic obstacles (like people or moving boxes) that aren't in the static map.

### C. Planners & Controllers
- **Global Planner (NavFn/Smac)**: Calculates the absolute shortest path from Point A to Point B across the entire Global Costmap.
- **Local Controller (DWB)**: Acts as the "driver." It looks at the global path, checks the Local Costmap for immediate obstacles, and calculates the exact motor velocities (`cmd_vel`) to smoothly steer the robot without crashing.
