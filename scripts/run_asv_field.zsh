#!/usr/bin/env zsh

emulate -L zsh
setopt ERR_EXIT PIPE_FAIL

script_dir=${0:A:h}
repo_dir=${script_dir:h}
world_file="$repo_dir/worlds/asv_field.world"
ros_setup="/opt/ros/jazzy/setup.zsh"

if [[ ! -f "$ros_setup" ]]; then
  print -u2 "ROS 2 Jazzy setup tidak ditemukan: $ros_setup"
  exit 1
fi

if [[ ! -f "$world_file" ]]; then
  print -u2 "World tidak ditemukan: $world_file"
  exit 1
fi

source "$ros_setup"

# Cloudflare WARP dapat mengambil alih route multicast Gazebo.
export GZ_IP="${GZ_IP:-127.0.0.1}"
export GZ_PARTITION="${GZ_PARTITION:-asv_debug}"
export GZ_SIM_RESOURCE_PATH="$repo_dir${GZ_SIM_RESOURCE_PATH:+:$GZ_SIM_RESOURCE_PATH}"

print "Menjalankan Gazebo Harmonic world: $world_file"
print "GZ_IP=$GZ_IP"
print "GZ_PARTITION=$GZ_PARTITION"

exec gz sim -r "$world_file" "$@"
