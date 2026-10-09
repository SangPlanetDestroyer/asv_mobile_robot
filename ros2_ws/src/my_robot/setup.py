from glob import glob
import os

from setuptools import setup

package_name = "my_robot"

setup(
    name=package_name,
    version="0.1.0",
    packages=[],
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name],
        ),
        ("share/" + package_name, ["package.xml"]),
        (
            os.path.join("share", package_name, "description", "meshes"),
            glob("description/meshes/*"),
        ),
        (
            os.path.join("share", package_name, "description", "urdf"),
            glob("description/urdf/*.urdf"),
        ),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
        (os.path.join("share", package_name, "worlds"), glob("worlds/*.world")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="ekonawa",
    maintainer_email="ekonawa@example.com",
    description="ASV mobile robot model and Gazebo Harmonic launch files.",
    license="Apache-2.0",
)
