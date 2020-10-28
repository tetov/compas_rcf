"""PickStation object to describe pick locations for fabrication process."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from itertools import cycle

from compas.geometry import Frame
from compas.geometry import Translation

from rapid_clay_formations_fab.fab_data import FabricationElement


class PickStation(object):
    """Picking station setup."""

    def __init__(
        self,
        pick_frames,
        elem_height=150,
        elem_egress_distance=150,
        station_egress_distance=400,
    ):
        """Init function for PickSetup.

        Parameters
        ----------
        plate_frames : list of :class:`compas.geometry.Frame`
            List of picking frames
        """
        self.pick_frames = pick_frames
        self.elem_height = elem_height
        self.elem_egress_distance = elem_egress_distance
        self.station_egress_distance = station_egress_distance

        # Infinite generator
        self.frame_gen = (frame for frame in cycle(self.pick_frames))

    @property
    def station_egress_frame(self):
        """:class:`compas.geometry.Frame` : Egress frame for pick plate."""
        tr = Translation([0, 0, self.station_egress_distance])
        return self.pick_frames[0].transformed(tr)

    @property
    def data(self):
        """:obj:`dict` : The data dictionary that represents the pick station."""
        return {
            # fmt: off
            "pick_frames": [f.to_data() for f in self.pick_frames],
            "elem_height": self.elem_height,
            "elem_egress_distance": self.elem_egress_distance,
            "station_egress_distance": self.station_egress_distance
            # fmt: on
        }

    @data.setter
    def data(self, data):
        self.pick_frames = [Frame.from_data(f) for f in data["pick_frames"]]
        self.elem_height = data["elem_height"]
        self.elem_egress_distance = data["elem_egress_distance"]
        self.station_egress_distance = data["station_egress_distance"]

    def get_next_pick_elem(self):
        """Get next pick element.

        Returns
        -------
        :class:`rapid_clay_formations_fab.fab_data.FabricationElement`
        """
        frame = next(self.frame_gen)
        return FabricationElement(
            # fmt: off
            frame,
            "pick_elem",
            height=self.elem_height,
            egress_frame_distance=self.elem_egress_distance
            # fmt: on
        )

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
