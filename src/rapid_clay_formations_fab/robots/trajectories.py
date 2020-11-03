"""A minimal trajectory class to mix frame sequences and joint trajectories.

Module name in reference to :mod:`class_fab.robots`.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame
from compas_fab.robots import Configuration
from compas_fab.robots import to_degrees
from compas_rrc import RobotJoints

try:
    from collections.abc import MutableSequence
except ImportError:
    from collections import MutableSequence


class _ListLike(MutableSequence):
    """Class to use as parent for listlike classes."""

    __slots__ = ()

    def __getitem__(self, index):
        return self.list_[index]

    def __setitem__(self, index, item):
        self.list_[index] = item

    def __delitem__(self, index):
        del self.list_[index]

    def __len__(self):
        return len(self.list_)

    def insert(self, index, item):
        """Insert element at specified index."""
        self.list_.insert(index, item)


class MinimalTrajectories(_ListLike):
    """List of :class:`MinimalTrajectory` objects.

    This class inherits from :obj:`MutableSequence` which means that it behaves
    like a :obj:`list` exposing methods such as ``index``, ``__iter__`` ``__len__``.

    Parameters
    ----------
    trajectories : :obj:`list` of :class:`MinimalTrajectory`
        Trajectory points.
    """

    __slots__ = "list_"

    def __init__(self, trajectories):
        self.trajectories = list(trajectories)

    def __repr__(self):
        return "MinimalTrajectories({})".format(self.trajectories)

    @property
    def trajectories(self):
        """:obj:`list` : List of trajectories."""
        return self.list_

    @trajectories.setter
    def trajectories(self, trajectories):
        self.list_ = trajectories

    @property
    def data(self):
        """Get a :obj:`dict` representation of :class:`MinimalTrajectories`."""
        return {"trajectories": [t.to_data() for t in self.trajectories]}

    @data.setter
    def data(self, data):
        self.trajectories = [
            MinimalTrajectory.from_data(t) for t in data["trajectories"]
        ]

    def reverse_recursively(self):
        """Reverse list and the lists elements."""
        self.reverse()
        for traj in self:
            traj.reverse()

    def copy(self):
        """Get an independent copy of object."""
        cls = type(self)
        return cls([o.copy() for o in self])

    def reversed_recursively(self):
        """Get an independent, recursively reversed copy of object."""
        copy = self.copy()
        copy.reverse_recursively()
        return copy

    def to_data(self):
        """Get a :obj:`dict` representation of :class:`MinimalTrajectories`."""
        return self.data

    @classmethod
    def from_data(cls, data):
        """Construct a :class:`MinimalTrajectories` from a :obj:`dict` representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        :class:`MinimalTrajectories`
        """
        obj = cls([])
        obj.data = data
        return obj


class MinimalTrajectory(_ListLike):
    """Trajectory defined either as joint positions or frames.

    This class inherits from UserList which means that it behaves like a
    :obj:`list` implementing methods such as ``index``, ``__iter__`` and
    reveresed.

    Parameters
    ----------
    points : :obj:`list`
        Trajectory points.
    """

    __slots__ = "list_"

    JOINT_TRAJECTORY = 0
    FRAME_TRAJECTORY = 1

    def __init__(self, points):
        self.list_ = list(points)

    def __repr__(self):
        return "MinimalTrajectory({})".format(self.points)

    @property
    def points(self):
        """:obj:`list` : List of trajectory points."""
        return self.list_

    @points.setter
    def points(self, points):
        self.list_ = points

    @property
    def data(self):
        """Get a :obj:`dict` representation of :class:`MinimalTrajectory`."""
        return {"points": [pt.to_data() for pt in self.points]}

    @data.setter
    def data(self, data):
        print("Data: {}".format(data))
        print("Type: {}".format(type(data)))
        if data["points"][0].get("xaxis"):  # check if data is of frame.data
            self.points = [Frame.from_data(pt) for pt in data["points"]]
        # check if first elem is Configuration dict
        elif data["points"][0].get("values"):
            self.points = [Configuration.from_data(pt) for pt in data["points"]]
        else:
            raise NotImplementedError("Object not recognized.")

    @property
    def trajectory_type(self):
        """:obj:`type` : Return the type of elements in the trajectory."""
        self._raise_if_mixed_types()
        if isinstance(self[0], Configuration):
            return self.JOINT_TRAJECTORY
        if isinstance(self[0], Frame):
            return self.FRAME_TRAJECTORY

        raise NotImplementedError("Trajectory not recognized: {}".format(self))

    def _raise_if_mixed_types(self):
        """Raise error if the list contains mixed types of objects."""
        types = (type(pt) for pt in self)

        if len(set(types)) != 1:
            raise RuntimeError(
                "Trajectory contains more than one type of objects: {}".format(types)
            )

    def as_robot_joints_points(self):
        """:obj:`list` of :class:`compas_rrc.RobotJoints` : Trajectory as list of ``RobotJoints``."""  # noqa: E501
        return [RobotJoints(*to_degrees(pt.values)) for pt in self.points]

    def copy(self):
        """Get an independent copy of object."""
        cls = type(self)
        return cls([o.copy() for o in self])

    def reversed(self):
        """Get an independent, reversed copy of object."""
        copy = self.copy()
        copy.reverse()

        return copy

    @classmethod
    def from_joint_trajectory(cls, joint_trajectory):
        """Construct a instance from a :class:`compas_fab.robots.JointTrajectory`."""
        conf_list = [
            Configuration.from_revolute_values(pt.values)
            for pt in joint_trajectory.points
        ]
        return cls(conf_list)

    def to_data(self):
        """Get :obj:`dict` representation of :class:`MinimalTrajectory`."""
        return self.data

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
        obj = cls([])
        obj.data = data
        return obj
