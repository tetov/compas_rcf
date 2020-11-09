"""Representation of pick stations on the IF for the RCF process."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Translation

from rapid_clay_formations_fab import fab_data


class PickStation(object):
    """Picking station setup."""

    def __init__(
        self,
        pick_frames,
        elem_height=150,
        elem_egress_distance=150,
        station_egress_distance=400,
    ):
        """Representation of pick stations on the IF for the RCF process.

        Parameters
        ----------
        pick_frames : list of :class:`compas.geometry.Frame`
            List of pick frames (bottom centroid of pick element).
        elem_height : :obj:`float`, optional
            Height of pick element in mm, defaults to 150.
        elem_egress_distance : :obj:`float`, optional
            Distance between top of element to egress frame in mm, defaults
            to 150.
        station_egress_distance: :obj:`float`, optional
            Distance between first elements top and egress frame to station.
        """
        self.pick_frames = pick_frames
        self.elem_height = elem_height
        self.elem_egress_distance = elem_egress_distance
        self.station_egress_distance = station_egress_distance

        self._pick_counter = 0

    def __repr__(self):
        return "PickStation({}, {}, {}, {})".format(
            self.pick_frames,
            self.elem_height,
            self.elem_egress_distance,
            self.station_egress_distance,
        )

    # TODO: Should maybe remove this, not used in client anymore
    @property
    def station_egress_frame(self):
        """:class:`compas.geometry.Frame` : Egress frame for pick plate."""
        tr = Translation(self.pick_frames[0].normal * -self.station_egress_distance)
        return self.pick_frames[0].transformed(tr)

    @property
    def data(self):
        """:obj:`dict` : The data dictionary that represents the pick station."""
        return {
            "pick_frames": self.pick_frames,
            "elem_height": self.elem_height,
            "elem_egress_distance": self.elem_egress_distance,
            "station_egress_distance": self.station_egress_distance,
        }

    @data.setter
    def data(self, data):
        self.pick_frames = data["pick_frames"]
        self.elem_height = data["elem_height"]
        self.elem_egress_distance = data["elem_egress_distance"]
        self.station_egress_distance = data["station_egress_distance"]

    def _get_next_pick_frame(self):
        frame = self.pick_frames[self._pick_counter % len(self.pick_frames)]
        self._pick_counter += 1
        return frame

    def get_next_pick_elem(self):
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

    def copy(self):
        """Create a copy of this :class:`PickStation`.

        Returns
        -------
        :class:`PickStation`
            An instance of :class:`FabricationElement`
        """
        cls = type(self)
        return cls.from_data(self.data)

    def transform(self, transformation):
        """Transforms a :class:`PickStation`.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`
        """
        for frame in self.pick_frames:
            frame.transform(transformation)

    def transformed(self, transformation):
        """Get a transformed copy of :class:`PickStation`.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`

        Returns
        -------
        :class:`PickStation`
        """
        copy = self.copy()
        copy.transform(transformation)
        return copy

    def to_data(self):
        """Get :obj:`dict` representation of :class:`PickStation`."""
        return self.data

    @classmethod
    def from_data(cls, data):
        """Construct an instance from its data representation.

        Parameters
        ----------
        data : :obj:`dict`

        Returns
        -------
        :class:`PickStation`
        """
        obj = cls([])
        obj.data = data

        return obj
