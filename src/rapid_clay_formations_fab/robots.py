"""A minimal trajectory class to mix frame sequences and joint trajectories.

Module name in reference to :mod:`class_fab.robots`"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from copy import deepcopy

from compas.geometry import Frame
from compas_fab.robots import JointTrajectoryPoint
from compas_fab.robots import to_degrees
from compas_rrc import RobotJoints

try:
    from collections.abc import MutableSequence
except ImportError:
    from collections import MutableSequence


class MinimalTrajectory(MutableSequence):
    """Trajectory defined either as joint positions or frames.

    This class inherits from UserList which means that it behaves like a
    :obj:`list` implementing methods such as ``index``, ``__iter__`` and
    reveresed.

    Parameters
    ----------
    points : :obj:`list`
        Trajectory points.
    """

    JOINT_TRAJECTORY = 0
    FRAME_TRAJECTORY = 1

    def __init__(self, points):
        self.points = list(points)

    def __getitem__(self, index):
        return self.points[index]

    def __setitem__(self, index, item):
        self.points[index] = item

    def __delitem__(self, index):
        del self.points[index]

    def __len__(self):
        return len(self.points)

    def __repr__(self):
        return "MinimalTrajectory({})".format(self.points)

    def insert(self, index, item):
        self.points.insert(index, item)

    @property
    def trajectory_type(self):
        """:obj:`type` : Return the type of elements in the trajectory."""
        self._raise_if_mixed_types()
        if isinstance(self.points[0], JointTrajectoryPoint):
            return self.JOINT_TRAJECTORY
        if isinstance(self.points[0], Frame):
            return self.FRAME_TRAJECTORY

        raise NotImplementedError("Trajectory not recognized: {}".format(self))

    def _raise_if_mixed_types(self):
        """Raise error if the list contains mixed types of objects."""
        types = (type(pt) for pt in self.points)

        if len(set(types)) != 1:
            raise RuntimeError(
                "Trajectory contains more than one type of objects: {}".format(types)
            )

    @staticmethod
    def revolute_configuration_to_robot_joints(configuration):
        """Convert a :class:`compas_fab.robots.Configuration` to a :class:`compas_rrc.RobotJoints`.

        Parameter
        ---------
        configuration : :class:`Configuration`

        Returns
        -------
        :class:`RobotJoints`
        """  # noqa: E501
        revolute_values_in_degrees = to_degrees(configuration.revolute_values)
        return RobotJoints(*revolute_values_in_degrees)

    @classmethod
    def from_joint_trajectory(cls, joint_trajectory):
        """Construct a instance from a :class:`compas_fab.robots.JointTrajectory`."""
        return cls(joint_trajectory.points)

    def to_robot_joints(self):
        """Create a list of :class:`compas_rrc.RobotJoints` from trajectory.

        Returns
        -------
        :obj:`list` of :class:`compas_rrc.RobotJoints`
        """
        robot_joints = []
        for pt in self:
            robot_joints.append(self.revolute_configuration_to_robot_joints(pt))
        return robot_joints

    def to_data(self):
        """Get :obj:`dict` representation of :class:`MinimalTrajectory`."""
        data = []
        for item in self.points:
            if hasattr(item, "to_data"):
                data.append(item.to_data())
            else:
                data.append(item)
        return data

    @classmethod
    def from_data(cls, data):
        """Construct a :class:`MinimalTrajectory` from a dictionary representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        :class:`MinimalTrajectory`
        """
        if data[0].get("xaxis"):  # check if data is of frame.data
            return cls([Frame.from_data(d) for d in data])
        # check if first elem is JointTrajectoryPoint dict
        if data[0].get("types"):
            return cls([JointTrajectoryPoint.from_data(d) for d in data])
        raise NotImplementedError(
            "from_data method not implemented for {}".format(type(data[0]))
        )


def two_levels_reversed(parent_list):
    """Reverse list as well as sublists."""
    twice_reversed = deepcopy(parent_list)
    twice_reversed.reverse()
    for sublist in twice_reversed:
        sublist.reverse()
    return twice_reversed
