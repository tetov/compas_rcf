from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Rotation
from compas.geometry import Transformation
from compas_fab.robots.configuration import Configuration
from compas_fab.robots.ur5 import Robot

from compas_rcf.rhino import cgframe_to_rgplane
from compas_rcf.rhino import matrix_to_rgtransform

__all__ = ["visualize_urscript"]


def visualize_urscript(script):
    M = [
        [-1000, 0, 0, 0],
        [0, 1000, 0, 0],
        [0, 0, 1000, 0],
        [0, 0, 0, 1],
    ]
    rgT = matrix_to_rgtransform(M)
    cgT = Transformation.from_matrix(M)

    robot = Robot()

    viz_planes = []

    movel_matcher = re.compile(r"^\s*move([lj]).+((-?\d+\.\d+,?\s?){6}).*$")
    for line in script.splitlines():
        mo = re.search(movel_matcher, line)
        if mo:
            if mo.group(1) == "l":  # movel
                ptX, ptY, ptZ, rX, rY, rZ = mo.group(2).split(",")

                pt = Point(float(ptX), float(ptY), float(ptZ))
                pt.transform(cgT)
                frame = Frame(pt, [1, 0, 0], [0, 1, 0])

                R = Rotation.from_axis_angle_vector(
                    [float(rX), float(rY), float(rZ)], pt
                )
                T = matrix_to_rgtransform(R)

                plane = cgframe_to_rgplane(frame)
                plane.Transform(T)

                viz_planes.append(plane)
            else:  # movej
                joint_values = mo.group(2).split(",")
                configuration = Configuration.from_revolute_values(
                    [float(d) for d in joint_values]
                )
                frame = robot.forward_kinematics(configuration)

                plane = cgframe_to_rgplane(frame)
                plane.Transform(rgT)

                viz_planes.append(plane)

    return viz_planes
