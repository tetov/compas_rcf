from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import docker

from rapid_clay_formations_fab.localization import xform_to_xyz_quaternion
from rapid_clay_formations_fab.robots import DRIVER_IMAGE_NAME


def publish_static_transform(
    xform,
    scale_factor=1,
    frame_id="world",
    child_frame_id="base_link",
    period_in_ms=100,
):
    container_name = "tf_base_link"
    env = {"ROS_HOSTNAME": container_name, "ROS_MASTER_URI": "http://ros-master:11311"}
    ros_network = "ros-driver"

    cmd = ["rosrun", "tf", "static_transform_publisher"]

    x, y, z, qw, qx, qy, qz = xform_to_xyz_quaternion(xform)
    x, y, z = [c * scale_factor for c in (x, y, z)]

    arg = [x, y, z, qw, qx, qy, qz, frame_id, child_frame_id, period_in_ms]
    arg = [str(a) for a in arg]

    cmd += arg

    docker_client = docker.from_env()
    try:
        running_container = docker_client.containers.get(container_name)
    except docker.errors.NotFound:
        pass
    else:
        running_container.remove(force=True)

    docker_client.containers.run(
        DRIVER_IMAGE_NAME,
        command=cmd,
        name=container_name,
        auto_remove=True,
        detach=True,
        environment=env,
        network=ros_network,
    )
    docker_client.close()
