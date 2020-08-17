from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
from collections import Sequence
from copy import deepcopy

from compas.geometry import Frame
from compas_fab.robots import JointTrajectory
from compas_rrc import RobotJoints


def get_trajectory_type(trajectory):
    if isinstance(trajectory, JointTrajectory):
        return "JointTrajectory"
    if isinstance(trajectory, Sequence):
        for elem in trajectory:
            if not isinstance(elem, Frame):
                break
        else:
            return "FrameList"

    raise ValueError(
        "Trajectory should contain JointTrajectory or Frame objects, not {}.".format(
            type(elem)
        )
    )


def reverse_trajectory(trajectory):
    if isinstance(trajectory, JointTrajectory):
        copy = deepcopy(trajectory)
        copy.points.reverse()

        return copy


def joint_trajectory_to_robot_joints_list(joint_trajectory):
    robot_joints_list = []
    for pt in joint_trajectory.points:
        in_degrees = [math.degrees(pos) for pos in pt.values]
        robot_joints_list.append(RobotJoints(*in_degrees))

    return robot_joints_list
