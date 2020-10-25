from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from compas.geometry import Frame
from compas.geometry import Transformation
from compas.geometry import Translation

log = logging.getLogger(__name__)


class PickStation(object):
    """Picking station setup."""

    def __init__(self, pick_frames):
        """Init function for PickSetup.

        Parameters
        ----------
        plate_frames : list of :class:`compas.geometry.Frame`
            List of picking frames
        """
        self.pick_frames = pick_frames
        self.counter = 0
        self.n_pick_frames = len(pick_frames)

    def get_egress_frame(self, offset=400):
        Tr = Translation([0, 0, offset])
        return self.pick_frames[0].transformed(Tr)

    def get_next_pick_elem(self, place_element):
        """Get next pick element.

        Parameters
        ----------
        place_element : :class:`rapid_clay_formations_fab.fab_data.FabricationElement`
            Element to place.

        Returns
        -------
        :class:`rapid_clay_formations_fab.fab_data.FabricationElement`
        """
        idx = self.counter % self.n_pick_frames
        self.counter += 1

        log.debug("Counter at: {}, Frame index at {}".format(self.counter, idx))

        pick_location = self.pick_frames[idx]

        T = Transformation.from_frame_to_frame(place_element.location, pick_location)

        # Copy place_cylinder to get same height properties
        pick_cylinder = place_element.copy()
        pick_cylinder.location.transform(T)

        return pick_cylinder

    @classmethod
    def from_data(cls, data):
        """TODO: Docstring for function.

        Parameters
        ----------
        data : :obj:`dict`

        Returns
        -------
        :class:`PickStation`
        """
        frames = [Frame.from_data(frame_data) for frame_data in data]

        return cls(frames)
