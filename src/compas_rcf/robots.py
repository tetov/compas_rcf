from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
from collections import Sequence
from copy import deepcopy

from compas.geometry import Frame
from compas_fab.robots import JointTrajectory
from compas_rrc import RobotJoints

JOINT_TRAJECTORY_TYPE = 0
FRAME_LIST_TRAJECTORY_TYPE = 1


def get_trajectory_type(trajectory):
    """Get trajectory type.

    Returns
    -------
    :obj:`int`
        Identifier for trajectory type.
    """
    if isinstance(trajectory, JointTrajectory):
        return JOINT_TRAJECTORY_TYPE
    if isinstance(trajectory, Sequence):
        for elem in trajectory:
            if not isinstance(elem, Frame):
                raise ValueError(
                    "Trajectory should be JointTrajectory or Frames, not {}.".format(
                        type(elem)
                    )
                )

        return FRAME_LIST_TRAJECTORY_TYPE


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
