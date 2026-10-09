import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    package_name = "my_robot"
    package_share = Path(get_package_share_directory(package_name))
    urdf_path = package_share / "description" / "urdf" / "robot.urdf"
    world_path = package_share / "worlds" / "asv_field.world"

    robot_description = urdf_path.read_text(encoding="utf-8")
    gazebo_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=(
            f"{package_share.parent}:"
            f"{os.environ.get('GZ_SIM_RESOURCE_PATH', '')}"
        ),
    )

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("ros_gz_sim"), "launch", "gz_sim.launch.py"]
            )
        ),
        launch_arguments={"gz_args": f"-r {world_path}"}.items(),
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description, "use_sim_time": True}],
    )

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        name="spawn_asv_mobile_robot",
        output="screen",
        arguments=[
            "-name",
            "asv_mobile_robot",
            "-file",
            str(urdf_path),
            "-x",
            "-4.47",
            "-y",
            "-12.82",
            "-z",
            "0.65",
        ],
    )

    bridges = [
        ("clock_bridge", "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock"),
        ("cmd_vel_bridge", "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist"),
        ("odom_bridge", "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry"),
        ("tf_bridge", "/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose"),
        ("imu_bridge", "/imu@sensor_msgs/msg/Imu[gz.msgs.IMU"),
        (
            "camera_image_bridge",
            "/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image",
        ),
        (
            "camera_info_bridge",
            "/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo",
        ),
    ]

    bridge_nodes = [
        Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            name=name,
            output="screen",
            arguments=[bridge],
        )
        for name, bridge in bridges
    ]

    return LaunchDescription(
        [gazebo_resource_path, gz_sim, robot_state_publisher, spawn_robot, *bridge_nodes]
    )
