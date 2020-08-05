from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import docker
from compas.geometry import quaternion_from_matrix
from compas.geometry import translation_from_matrix

from compas_rcf.abb import DRIVER_CONTAINER_NAME


def xform_to_xyz_quaternion(xform):
    xyz = translation_from_matrix(xform)
    quaternion = quaternion_from_matrix(xform)

    return xyz + quaternion


def publish_static_transform(xform):
    container_name = "tf_base_link"
    env = {"ROS_HOSTNAME": container_name, "ROS_MASTER_URI": "http://ros-master:11311"}
    ros_network = "abb_driver"

    cmd = ["rosrun", "tf", "static_transform_publisher"]

    x, y, z, qw, qx, qy, qz = xform_to_xyz_quaternion(xform)
    x, y, z = [c / 1000 for c in (x, y, z)]

    arg = [x, y, z, qw, qx, qy, qz, "world", "base_link"]
    arg = [str(a) for a in arg]

    cmd += arg

    with docker.from_env() as docker_client:
        try:
            running_container = docker_client.get(container_name)
        except docker.errors.NotFound:
            pass
        else:
            running_container.kill()

        docker_client.run(
            DRIVER_CONTAINER_NAME,
            command=cmd,
            name=container_name,
            autoremove=True,
            detach=True,
            environment=env,
            network=ros_network,
        )
