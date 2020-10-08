from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
from copy import deepcopy

from compas_rrc import RobotJoints


def reversed_trajectory(trajectory):
    """Get a reversed copy of a trajectory.

    Parameters
    ----------
    trajectory : :class:`compas_fab.robots.JointTrajectory`
        Trajectory described by joint positions or frames.

    Returns
    -------
    :class:`compas_fab.robots.JointTrajectory`
        Reversed trajectory.
    """
    copy = deepcopy(trajectory)
    copy.points.reverse()
    return copy


def reversed_trajectories(trajectories):
    """Get a reversed list of reversed trajectories.

    Parameters
    ----------
    trajectories : :obj:`list` of :class:`compas_fab.robots.JointTrajectory`
        Trajectories described by joint positions.

    Returns
    -------
    :obj:`list` of :class:`compas_fab.robots.JointTrajectory`
        Reversed trajectories.
    """  # noqa: E501
    reversed_list = trajectories[::-1]
    return [reversed_trajectory(trajectory) for trajectory in reversed_list]


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
