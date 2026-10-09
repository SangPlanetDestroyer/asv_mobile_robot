#!/usr/bin/env zsh

emulate -L zsh
setopt ERR_EXIT PIPE_FAIL

script_dir=${0:A:h}
repo_dir=${script_dir:h}
ros_setup="/opt/ros/jazzy/setup.zsh"
ros_workspace="$repo_dir/ros2_ws"
package_dir="$ros_workspace/src/my_robot"

if [[ ! -f "$ros_setup" ]]; then
  print -u2 "ROS 2 Jazzy setup tidak ditemukan: $ros_setup"
  exit 1
fi

if [[ ! -d "$package_dir" ]]; then
  print -u2 "Package my_robot tidak ditemukan: $package_dir"
  exit 1
fi

unset AMENT_PREFIX_PATH COLCON_PREFIX_PATH COLCON_CURRENT_PREFIX
source "$ros_setup"

# Cloudflare WARP dapat mengambil alih route multicast Gazebo.
export GZ_IP="${GZ_IP:-127.0.0.1}"
export GZ_PARTITION="${GZ_PARTITION:-asv_debug}"
export GZ_SIM_RESOURCE_PATH="$repo_dir${GZ_SIM_RESOURCE_PATH:+:$GZ_SIM_RESOURCE_PATH}"

cd "$ros_workspace"
print "Membangun package my_robot..."
colcon build --packages-select my_robot
source install/setup.zsh

print "Menjalankan robot ASV di Gazebo Harmonic"
print "GZ_IP=$GZ_IP"
print "GZ_PARTITION=$GZ_PARTITION"

exec ros2 launch my_robot asv_gazebo.launch.py "$@"