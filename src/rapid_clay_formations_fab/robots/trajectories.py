"""A minimal trajectory class to mix frame sequences and joint trajectories.

Module name in reference to :mod:`class_fab.robots`.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_rrc
from compas.geometry import Frame
from compas_fab.robots import Configuration
from compas_fab.robots import JointTrajectory
from compas_fab.robots import to_degrees

try:
    from collections.abc import MutableSequence
except ImportError:
    from collections import MutableSequence

try:
    from typing import Any
    from typing import Callable
    from typing import List
    from typing import Tuple
    from typing import Union
except ImportError:
    pass


class _ListLike(MutableSequence):
    """Class to use as parent for listlike classes."""

    __slots__ = ()

    def __init__(self, list_):
        self._list = list(list_)  # type: List

    def __getitem__(self, index):  # type: (Union[int, slice]) -> Any
        return self._list[index]

    def __setitem__(self, index, item):  # type: (Union[int, slice], Any) -> None
        self._list[index] = item

    def __delitem__(self, index):  # type: (Union[int, slice]) -> None
        del self._list[index]

    def __len__(self):  # type: () -> int
        return len(self._list)

    def insert(self, index, item):  # type: (int, Any) -> None
        """Insert element at specified index."""
        self._list.insert(index, item)


class MinimalTrajectories(_ListLike):
    """List of :class:`MinimalTrajectory` objects.

    This class inherits from :obj:`MutableSequence` which means that it behaves
    like a :obj:`list` exposing methods such as ``index``, ``__iter__`` ``__len__``.

    Parameters
    ----------
    trajectories : :obj:`list` of :class:`MinimalTrajectory`
        Trajectory points.
    """

    __slots__ = "_list"

    def __init__(  # skipcq
        self, trajectories
    ):  # type: (List[MinimalTrajectory]) -> None
        super(MinimalTrajectories, self).__init__(trajectories)

    def __repr__(self):
        return "MinimalTrajectories({})".format(self.trajectories)

    @property
    def trajectories(self):  # type: () -> List[MinimalTrajectory]
        """:obj:`list` : List of trajectories."""
        return self._list

    @trajectories.setter
    def trajectories(self, trajectories):
        self._list = trajectories

    @property
    def data(self):  # type: () -> dict
        """Get a :obj:`dict` representation of :class:`MinimalTrajectories`."""
        return {"trajectories": [t.to_data() for t in self.trajectories]}

    @data.setter
    def data(self, data):  # type: (dict) -> None
        self.trajectories = data["trajectories"]

    def reverse_recursively(self):  # type: () -> None
        """Reverse list and the lists elements."""
        self.reverse()
        for traj in self:
            traj.reverse()

    def copy(self):  # type: () -> MinimalTrajectories
        """Get an independent copy of object."""
        cls = type(self)
        return cls([o.copy() for o in self])

    def reversed_recursively(self):  # type: () -> MinimalTrajectories
        """Get an independent, recursively reversed copy of object."""
        copy = self.copy()
        copy.reverse_recursively()
        return copy

    def to_data(self):  # type: () -> dict
        """Get a :obj:`dict` representation of :class:`MinimalTrajectories`."""
        return self.data

    @classmethod
    def from_data(cls, data):  # type: (dict) -> MinimalTrajectories
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

    __slots__ = "_list"

    JOINT_TRAJECTORY = 0
    FRAME_TRAJECTORY = 1

    def __init__(  # skipcq
        self, points
    ):  # type: (List[Union[Frame, Configuration]]) -> None
        super(MinimalTrajectory, self).__init__(points)

    def __repr__(self):
        return "MinimalTrajectory({})".format(self.points)

    @property
    def points(self):  # type: () -> List[Union[Frame, Configuration]]
        """:obj:`list` : List of trajectory points."""
        return self._list

    @points.setter
    def points(self, points):  # type: (List[Union[Frame, Configuration]]) -> None
        self._list = points

    @property
    def data(self):  # type: () -> dict
        """Get a :obj:`dict` representation of :class:`MinimalTrajectory`."""
        return {"points": self.points}

    @data.setter
    def data(self, data):  # type: (dict) -> None
        self.points = data["points"]

    @property
    def trajectory_type(self):  # type: () -> int
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

    def copy(self):  # type: () -> MinimalTrajectory
        """Get an independent copy of object."""
        cls = type(self)
        return cls([o.copy() for o in self])

    def reversed(self):  # type: () -> MinimalTrajectory
        """Get an independent, reversed copy of object."""
        copy = self.copy()
        copy.reverse()

        return copy

    def to_compas_rrc(
        self,
    ):  # type: () -> Tuple[Callable, List[Union[Frame, compas_rrc.RobotJoints]]]
        if self.trajectory_type == self.FRAME_TRAJECTORY:
            rrc_trajectory = self._list
            rrc_instruction = compas_rrc.MoveToRobtarget
        if self.trajectory_type == self.JOINT_TRAJECTORY:
            rrc_trajectory = [
                compas_rrc.RobotJoints(*to_degrees(pt.values)) for pt in self.points
            ]
            rrc_instruction = compas_rrc.MoveToJoints

        return rrc_instruction, rrc_trajectory

    @classmethod
    def from_joint_trajectory(
        cls, joint_trajectory
    ):  # type: (JointTrajectory) -> MinimalTrajectory
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
    def from_data(cls, data):  # type: (dict) -> MinimalTrajectory
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
