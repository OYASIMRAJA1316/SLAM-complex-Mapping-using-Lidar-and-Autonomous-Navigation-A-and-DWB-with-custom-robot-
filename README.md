# Alpha Robot Simulation & Navigation Stack

This repository contains the complete ROS 2 Jazzy software stack for the custom-built Alpha Robot. In this project, I fully created my own custom robot using custom 3D meshes and URDF files, designed a custom Gazebo Harmonic warehouse world to spawn the robot in, and developed tailored RViz configurations and launch files specifically for SLAM mapping and autonomous Nav2 navigation. I built the complete SLAM and navigation pipeline for Alpha and integrating SLAM Toolbox for real-time mapping and localization with the Nav2 stack for global/local path planning, costmap configuration, complex dynamic Obstcale avoidance and autonomous goal-based navigation fully validated within the ROS 2 Jazzy and Gazebo Harmonic simulation environment.

## Repository Structure
- `alpha_description_new`: URDF, meshes, and robot state publishers.
- `gazebo_simulations`: Gazebo Harmonic worlds, environment models, and launch configurations.
- `slam`: SLAM Toolbox integration for 2D map generation.
- `navigation`: Nav2 stack configurations, costmaps, and planners for autonomous point-to-point navigation.

## Demo Videos
# Mapping Demo


https://github.com/user-attachments/assets/c176a1ce-d326-43d0-adbb-b17d9784e069






## Prerequisites
- **ROS 2 Jazzy**
- **Gazebo Harmonic** (`ros-jazzy-ros-gz`)
- **Nav2** (`ros-jazzy-navigation2`, `ros-jazzy-nav2-bringup`)
- **SLAM Toolbox** (`ros-jazzy-slam-toolbox`)

## 1. Setup & Installation
```bash
# 1. Clone this repository to act as your ROS 2 workspace
git clone https://github.com/OYASIMRAJA1316/SLAM-complex-Mapping-using-Lidar-and-Autonomous-Navigation-A-and-DWB-with-custom-robot-.git ros2_ws
cd ~/ros2_ws

# Install dependencies using rosdep
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y

# Build the workspace
colcon build --symlink-install --packages-select alpha_description_new gazebo_simulations slam navigation

# Source the workspace
source install/setup.bash
```

## Execution Flow for Simulation

#### Phase 1: Verify Robot Description (URDF)
Check that the robot's physical model, links, and joints are rendering correctly in RViz before launching the physics engine.
```bash
ros2 launch alpha_description_new robot_description.launch.py
```
*(You should see the Alpha robot appear in RViz. Close RViz before proceeding to Phase 2).*

#### Phase 2: Verify Gazebo Simulation
Check that Gazebo Harmonic launches correctly and the Alpha robot spawns inside the 3D warehouse environment.
```bash
ros2 launch gazebo_simulations gazebo.launch.py
```
*(If everything looks correct, you can leave this running for Phase 3, or close it and start fresh).*

#### Phase 3: SLAM Mapping
To map a new environment, run these commands in three separate terminals:

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

**How to Map and Save:**
* **Drive the Robot:** Use the built-in Gazebo teleop to move the Alpha robot around the warehouse. Click the orange "Play" button in Gazebo if physics are paused.
* **Save the Map:** Once the map is fully generated in RViz, click the **"Panels"** menu at the top of RViz, select **"Add New Panel"**, and add the **"SLAMToolboxPlugin"**. In that panel, type a name for your map (e.g., `my_warehouse_map`) and click **"Save Map"** or **"Serialize Map"**.

#### Phase 4: Navigation
Once you have saved a map, you can use the Navigation stack to autonomously move the robot.

1. **Start Simulation (Terminal 1)**:
   ```bash
   ros2 launch gazebo_simulations gazebo.launch.py
   ```
2. **Start Navigation (Terminal 2)**:
   *(Make sure to replace `your_map_name` with the EXACT name of the map you saved in the SLAM Toolbox plugin during Phase 3!)*
   ```bash
   ros2 launch navigation navigation.launch.py sim:=true map:=your_map_name
   ```
3. **Launch RViz for Navigation (Terminal 3)**:
   ```bash
   ros2 launch navigation rviz_navigation.launch.py sim:=true
   ```
*(Use the "2D Pose Estimate" tool in the top bar of RViz to tell the robot where it is on the map. Then, use the "2D Nav Goal" tool to command the robot to drive!)*

#### Phase 5: Advanced Parameter Tuning (Nav2)
To achieve more complex and specific navigation behaviors (such as tuning dynamic obstacle avoidance, altering path planning characteristics, or modifying the robot's velocity profiles), you can edit the Navigation parameters.

* **Target File:** `navigation/config/nav2_params.yaml` (inside this repository)
* **What you can tune:**
  * **Costmap Inflation Radius:** Adjust how far the robot stays away from walls.
  * **DWB Controller:** Modify `max_vel_x`, `max_vel_theta`, and acceleration limits to make the Alpha robot drive faster or slower.
  * **Path Planning:** Tweak the Smac/NavFn parameters to change how the robot calculates its global path through the warehouse.
  * **AMCL:** Adjust the particle filter parameters (`alpha1` to `alpha5` for the `OmniMotionModel`) if the robot struggles to localize while strafing.

*(Playing with these parameters will directly impact how aggressively or safely the robot navigates complex scenarios!)*
