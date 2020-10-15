"""Helper functions for :mod:`compas_fab.robots` and :mod:`compas_rrc`."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from copy import deepcopy

import compas_rrc
from compas_fab.robots import to_degrees


def reversed_trajectory(trajectory):
    """Get a reversed copy of a trajectory.

    Parameters
    ----------
    trajectory : :class:`compas_fab.robots.JointTrajectory`

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
    reversed_list = deepcopy(trajectories)  # added because of paranoia
    reversed_list.reverse()
    return [reversed_trajectory(trajectory) for trajectory in reversed_list]


def revolute_configuration_to_robot_joints(configuration):
    """Convert a :class:`compas_fab.robots.Configuration` to a :class:`compas_rrc.RobotJoints`.

    This function ignores non revolute values.

    Parameter
    ---------
    configuration : :class:`Configuration`

    Returns
    -------
    :class:`RobotJoints`
    """  # noqa: E501
    revolute_values_in_degrees = to_degrees(configuration.revolute_values)
    return compas_rrc.RobotJoints(*revolute_values_in_degrees)
