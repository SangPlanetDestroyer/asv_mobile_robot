#!/usr/bin/env python3

import json

import cv2
import numpy as np
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String


class AsvVision(Node):
    def __init__(self):
        super().__init__("asv_vision")
        self.declare_parameter("min_blob_area", 120.0)
        self.declare_parameter("publish_rate_limit", 10.0)
        self.min_blob_area = float(self.get_parameter("min_blob_area").value)
        self.publish_period = 1.0 / float(self.get_parameter("publish_rate_limit").value)
        self.last_publish_time = 0.0

        self.detection_pub = self.create_publisher(String, "/asv/vision/detections", 10)
        self.status_pub = self.create_publisher(String, "/asv/vision/status", 10)
        self.create_subscription(Image, "/camera/image_raw", self.image_callback, 10)

        self.get_logger().info("ASV vision aktif: deteksi warna merah, hijau, dan biru")

    def now(self):
        return self.get_clock().now().nanoseconds / 1e9

    def image_callback(self, message):
        current_time = self.now()
        if current_time - self.last_publish_time < self.publish_period:
            return

        image = self.image_to_bgr(message)
        if image is None:
            self.publish_status("unsupported_encoding")
            return

        height, width = image.shape[:2]
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        detections = {
            "stamp": current_time,
            "width": width,
            "height": height,
            "colors": {
                "red": self.detect_color(hsv, "red", width, height),
                "green": self.detect_color(hsv, "green", width, height),
                "blue": self.detect_color(hsv, "blue", width, height),
            },
        }

        output = String()
        output.data = json.dumps(detections, separators=(",", ":"))
        self.detection_pub.publish(output)
        self.publish_status("ok")
        self.last_publish_time = current_time

    def image_to_bgr(self, message):
        channels = {
            "mono8": 1,
            "rgb8": 3,
            "bgr8": 3,
            "rgba8": 4,
            "bgra8": 4,
        }
        channel_count = channels.get(message.encoding.lower())
        if channel_count is None:
            return None

        array = np.frombuffer(message.data, dtype=np.uint8)
        expected_size = message.height * message.step
        if array.size < expected_size:
            return None
        array = array[:expected_size].reshape(message.height, message.step)
        array = array[:, : message.width * channel_count]
        if channel_count == 1:
            return cv2.cvtColor(array.reshape(message.height, message.width), cv2.COLOR_GRAY2BGR)
        image = array.reshape(message.height, message.width, channel_count)
        encoding = message.encoding.lower()
        if encoding == "rgb8":
            return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if encoding == "rgba8":
            return cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
        if encoding == "bgra8":
            return cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
        return image

    def detect_color(self, hsv, color, width, height):
        ranges = {
            "red": [((0, 90, 70), (10, 255, 255)), ((170, 90, 70), (180, 255, 255))],
            "green": [((35, 70, 50), (90, 255, 255))],
            "blue": [((90, 70, 50), (135, 255, 255))],
        }
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for lower, upper in ranges[color]:
            mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lower, upper))
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        blobs = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < self.min_blob_area:
                continue
            moments = cv2.moments(contour)
            if moments["m00"] == 0:
                continue
            center_x = moments["m10"] / moments["m00"]
            center_y = moments["m01"] / moments["m00"]
            x, y, blob_width, blob_height = cv2.boundingRect(contour)
            blobs.append({
                "x": round(center_x / width * 2.0 - 1.0, 4),
                "y": round(center_y / height * 2.0 - 1.0, 4),
                "area": round(area / (width * height), 6),
                "pixel_area": round(area, 1),
                "bbox": [x, y, blob_width, blob_height],
            })
        return sorted(blobs, key=lambda blob: blob["pixel_area"], reverse=True)

    def publish_status(self, status):
        message = String()
        message.data = status
        self.status_pub.publish(message)


def main(args=None):
    rclpy.init(args=args)
    node = AsvVision()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()