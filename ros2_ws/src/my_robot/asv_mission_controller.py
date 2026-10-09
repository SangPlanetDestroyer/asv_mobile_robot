#!/usr/bin/env python3

import math
from enum import Enum

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import Image, Imu
from std_msgs.msg import String


class MissionState(Enum):
    WAIT_FOR_SENSORS = "WAIT_FOR_SENSORS"
    FOLLOW_ROUTE = "FOLLOW_ROUTE"
    SURFACE_IMAGING = "SURFACE_IMAGING"
    UNDERWATER_IMAGING = "UNDERWATER_IMAGING"
    DOCKING = "DOCKING"
    FINISHED = "FINISHED"
    FAIL_SAFE = "FAIL_SAFE"


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def normalize_angle(angle):
    return math.atan2(math.sin(angle), math.cos(angle))


class AsvMissionController(Node):
    def __init__(self):
        super().__init__("asv_mission_controller")

        self.declare_parameter("waypoints", [
            -4.8, -8.0, -5.8, -4.0, -4.7, 0.5,
            -8.0, 5.7, -14.5, 7.9, -20.0, 7.8,
            -25.0, 3.0, -26.7, -2.0, -25.0, -7.5,
            -22.0, -10.8, -16.0, -11.5, -10.0, -11.5,
            -6.0, -11.0, -4.47, -11.0,
        ])
        self.declare_parameter("surface_imaging_pose", [-22.0, -10.8])
        self.declare_parameter("underwater_imaging_pose", [-25.0, -7.5])
        self.declare_parameter("docking_pose", [-4.47, -11.0])
        self.declare_parameter("lookahead_distance", 1.2)
        self.declare_parameter("cruise_speed", 0.55)
        self.declare_parameter("max_angular_speed", 1.2)
        self.declare_parameter("geofence", [-28.5, 28.5, -13.5, 13.5])
        self.declare_parameter("sensor_timeout", 1.0)
        self.declare_parameter("mission_timeout", 900.0)
        self.declare_parameter("imaging_hold_time", 3.0)
        self.declare_parameter("docking_hold_time", 4.0)

        self.waypoints = self._pair_parameter("waypoints")
        self.surface_pose = self._pair_parameter("surface_imaging_pose")[0]
        self.underwater_pose = self._pair_parameter("underwater_imaging_pose")[0]
        self.docking_pose = self._pair_parameter("docking_pose")[0]
        self.lookahead = self.get_parameter("lookahead_distance").value
        self.cruise_speed = self.get_parameter("cruise_speed").value
        self.max_angular_speed = self.get_parameter("max_angular_speed").value
        self.geofence = self.get_parameter("geofence").value
        self.sensor_timeout = self.get_parameter("sensor_timeout").value
        self.mission_timeout = self.get_parameter("mission_timeout").value
        self.imaging_hold_time = self.get_parameter("imaging_hold_time").value
        self.docking_hold_time = self.get_parameter("docking_hold_time").value

        self.state = MissionState.WAIT_FOR_SENSORS
        self.position = None
        self.heading = 0.0
        self.angular_velocity = 0.0
        self.last_odom_time = None
        self.last_imu_time = None
        self.last_image_time = None
        self.mission_start_time = None
        self.state_start_time = None
        self.route_index = 0
        self.imaging_pose_reached = False

        self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.state_pub = self.create_publisher(String, "/asv/mission_state", 10)
        self.monitor_pub = self.create_publisher(String, "/asv/monitoring", 10)
        self.create_subscription(Odometry, "/odom", self.odom_callback, 10)
        self.create_subscription(Imu, "/imu", self.imu_callback, 10)
        self.create_subscription(Image, "/camera/image_raw", self.image_callback, 10)
        self.timer = self.create_timer(0.05, self.control_callback)

        self.get_logger().info(
            f"ASV mission controller aktif dengan {len(self.waypoints)} waypoint"
        )

    def _pair_parameter(self, name):
        values = list(self.get_parameter(name).value)
        if len(values) < 2 or len(values) % 2 != 0:
            raise ValueError(f"Parameter {name} harus berisi pasangan x,y")
        return list(zip(values[::2], values[1::2]))

    def now(self):
        return self.get_clock().now().nanoseconds / 1e9

    def odom_callback(self, message):
        self.position = (
            message.pose.pose.position.x,
            message.pose.pose.position.y,
        )
        q = message.pose.pose.orientation
        self.heading = math.atan2(
            2.0 * (q.w * q.z + q.x * q.y),
            1.0 - 2.0 * (q.y * q.y + q.z * q.z),
        )
        self.last_odom_time = self.now()

    def imu_callback(self, message):
        self.angular_velocity = message.angular_velocity.z
        self.last_imu_time = self.now()

    def image_callback(self, _message):
        self.last_image_time = self.now()

    def control_callback(self):
        current_time = self.now()
        if self.state == MissionState.FAIL_SAFE or self.state == MissionState.FINISHED:
            self.publish_stop()
            self.publish_monitoring(current_time)
            return

        if self.position is None or self.last_odom_time is None or self.last_imu_time is None:
            self.set_state(MissionState.WAIT_FOR_SENSORS, current_time)
            self.publish_stop()
            self.publish_monitoring(current_time)
            return

        if self.mission_start_time is None:
            self.mission_start_time = current_time
            self.state_start_time = current_time

        if self._sensor_stale(current_time):
            self.enter_fail_safe("sensor timeout", current_time)
        elif current_time - self.mission_start_time > self.mission_timeout:
            self.enter_fail_safe("mission timeout", current_time)
        elif not self._inside_geofence():
            self.enter_fail_safe("geofence violation", current_time)
        else:
            self.run_state(current_time)

        self.publish_monitoring(current_time)

    def _sensor_stale(self, current_time):
        return (
            current_time - self.last_odom_time > self.sensor_timeout
            or current_time - self.last_imu_time > self.sensor_timeout
        )

    def _inside_geofence(self):
        minimum_x, maximum_x, minimum_y, maximum_y = self.geofence
        return (
            minimum_x <= self.position[0] <= maximum_x
            and minimum_y <= self.position[1] <= maximum_y
        )

    def run_state(self, current_time):
        if self.state == MissionState.WAIT_FOR_SENSORS:
            self.set_state(MissionState.FOLLOW_ROUTE, current_time)

        if self.state == MissionState.FOLLOW_ROUTE:
            if self.route_index >= len(self.waypoints):
                self.set_state(MissionState.SURFACE_IMAGING, current_time)
            else:
                self.follow_target(self.waypoints[self.route_index])
                if self.distance_to(self.waypoints[self.route_index]) < 0.65:
                    self.route_index += 1

        elif self.state == MissionState.SURFACE_IMAGING:
            self.handle_imaging(self.surface_pose, MissionState.UNDERWATER_IMAGING, current_time)
        elif self.state == MissionState.UNDERWATER_IMAGING:
            self.handle_imaging(self.underwater_pose, MissionState.DOCKING, current_time)
        elif self.state == MissionState.DOCKING:
            self.handle_docking(current_time)

    def follow_target(self, target):
        distance = self.distance_to(target)
        target_heading = math.atan2(target[1] - self.position[1], target[0] - self.position[0])
        heading_error = normalize_angle(target_heading - self.heading)
        speed_scale = clamp(1.0 - abs(heading_error) / 1.5, 0.2, 1.0)
        if distance < self.lookahead:
            speed_scale *= clamp(distance / self.lookahead, 0.25, 1.0)

        command = Twist()
        command.linear.x = self.cruise_speed * speed_scale
        command.angular.z = clamp(
            2.0 * heading_error - 0.15 * self.angular_velocity,
            -self.max_angular_speed,
            self.max_angular_speed,
        )
        self.cmd_pub.publish(command)

    def handle_imaging(self, target, next_state, current_time):
        if self.distance_to(target) > 0.7:
            self.follow_target(target)
            return

        self.publish_stop()
        image_is_fresh = (
            self.last_image_time is not None
            and current_time - self.last_image_time <= self.sensor_timeout * 2.0
        )
        if image_is_fresh and current_time - self.state_start_time >= self.imaging_hold_time:
            self.set_state(next_state, current_time)

    def handle_docking(self, current_time):
        if self.distance_to(self.docking_pose) > 0.35:
            self.follow_target(self.docking_pose)
            return
        self.publish_stop()
        if current_time - self.state_start_time >= self.docking_hold_time:
            self.set_state(MissionState.FINISHED, current_time)

    def distance_to(self, target):
        return math.hypot(target[0] - self.position[0], target[1] - self.position[1])

    def set_state(self, state, current_time):
        if self.state != state:
            self.get_logger().info(f"Mission state: {self.state.value} -> {state.value}")
            self.state = state
            self.state_start_time = current_time

    def enter_fail_safe(self, reason, current_time):
        self.get_logger().error(f"FAIL_SAFE: {reason}")
        self.set_state(MissionState.FAIL_SAFE, current_time)
        self.publish_stop()

    def publish_stop(self):
        self.cmd_pub.publish(Twist())

    def publish_monitoring(self, current_time):
        state_message = String()
        state_message.data = self.state.value
        self.state_pub.publish(state_message)

        monitor_message = String()
        elapsed = 0.0 if self.mission_start_time is None else current_time - self.mission_start_time
        x, y = self.position if self.position is not None else (float("nan"), float("nan"))
        monitor_message.data = (
            f"state={self.state.value};x={x:.3f};y={y:.3f};"
            f"heading={self.heading:.3f};route_index={self.route_index};elapsed={elapsed:.1f}"
        )
        self.monitor_pub.publish(monitor_message)


def main(args=None):
    rclpy.init(args=args)
    node = AsvMissionController()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        if rclpy.ok():
            node.publish_stop()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()