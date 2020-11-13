"""Representation of pick stations on the IF for the RCF process."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from rapid_clay_formations_fab import fab_data

try:
    import typing
except ImportError:
    pass
else:
    if typing.TYPE_CHECKING:
        from typing import List

        from compas.geometry import Frame
        from compas.geometry import Transformation


class PickStation(object):
    """Picking station setup."""

    def __init__(
        self,
        pick_frames,  # type: List[Frame]
        elem_height=150,  # type: float
        elem_egress_distance=150,  # type: float
    ):
        """Representation of pick stations on the IF for the RCF process.

        Parameters
        ----------
        pick_frames
            List of pick frames (bottom centroid of pick element).
        elem_height
            Height of pick element in mm, defaults to 150.
        elem_egress_distance
            Distance between top of element to egress frame in mm, defaults
            to 150.
        """
        self.pick_frames = pick_frames
        self.elem_height = elem_height
        self.elem_egress_distance = elem_egress_distance

        self._pick_counter = 0

    def __str__(self):  # type: () -> str
        return (
            "PickStation({}, Element height: {}, Element egress distance: {})".format(
                self.pick_frames,
                self.elem_height,
                self.elem_egress_distance,
            )
        )

    @property
    def data(self):  # type: () -> dict
        """The data dictionary that represents the pick station."""
        return {
            "pick_frames": self.pick_frames,
            "elem_height": self.elem_height,
            "elem_egress_distance": self.elem_egress_distance,
        }

    @data.setter
    def data(self, data):  # type: (dict) -> None
        self.pick_frames = data["pick_frames"]
        self.elem_height = data["elem_height"]
        self.elem_egress_distance = data["elem_egress_distance"]

    def _get_next_pick_frame(self):  # type: () -> Frame
        frame = self.pick_frames[self._pick_counter % len(self.pick_frames)]
        self._pick_counter += 1
        return frame

    def get_next_pick_elem(self):  # type: () -> fab_data.FabricationElement
        """Get next pick element.

        Returns
        -------
        :class:`rapid_clay_formations_fab.fab_data.FabricationElement`
        """
        frame = self._get_next_pick_frame()
        return fab_data.FabricationElement(
            frame,
            height=self.elem_height,
            egress_frame_distance=self.elem_egress_distance,
        )

    def copy(self):  # type: () -> PickStation
        """Create a copy of this :class:`PickStation`."""
        cls = type(self)
        return cls.from_data(self.data)

    def transform(self, transformation):  # type: (Transformation) -> None
        """Transform a :class:`PickStation`.

        Parameters
        ----------
        transformation
        """
        for frame in self.pick_frames:
            frame.transform(transformation)

    def transformed(self, transformation):  # type: (Transformation) -> PickStation
        """Get a transformed copy of :class:`PickStation`.

        Parameters
        ----------
        transformation

        Returns
        -------
        :class:`PickStation`
        """
        copy = self.copy()
        copy.transform(transformation)
        return copy

    def to_data(self):  # type: () -> dict
        """Get :obj:`dict` representation of :class:`PickStation`."""
        return self.data

    @classmethod
    def from_data(cls, data):  # type: (dict) -> PickStation
        """Construct an instance from its data representation.

        Parameters
        ----------
        data

        Returns
        -------
        :class:`PickStation`
        """
        obj = cls([])
        obj.data = data

        return obj
