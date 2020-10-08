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


def reversed_trajectory(trajectory):
    """Get a reversed copy of a trajectory.

    Parameters
    ----------
    trajectory : :class:`compas_fab.robots.JointTrajectory` or :obj:`list` of :class:`compas.geometry.Frame`
        Trajectory described by joint positions or frames.

    Returns
    -------
    :class:`compas_fab.robots.JointTrajectory` or :obj:`list` of :class:`compas.geometry.Frame`
        Reversed trajectory.
    """  # noqa: E501
    copy = deepcopy(trajectory)
    type_ = get_trajectory_type(trajectory)
    if type_ == JOINT_TRAJECTORY_TYPE:
        copy.points.reverse()
    elif type_ == FRAME_LIST_TRAJECTORY_TYPE:
        copy.reverse()
    return copy


def joint_trajectory_to_robot_joints_list(joint_trajectory):
    """Convert a compas_fab ``JointTrajectory`` object to a list of compas_rrc ``RobotJoints``.

    Parameter
    ---------
    joint_trajectory : :class:`compas_fab.robots.JointTrajectory`

    Returns
    -------
    :obj:`list` of :class:`compas_rrc.RobotJoints`.
    """  # noqa: E501
    robot_joints_list = []
    for pt in joint_trajectory.points:
        in_degrees = [math.degrees(pos) for pos in pt.values]
        robot_joints_list.append(RobotJoints(*in_degrees))

    return robot_joints_list
