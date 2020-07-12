from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from compas.geometry import Frame

from compas_rcf.fab_data.conf import fab_conf
from compas_rcf.utils import get_offset_frame

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

    def get_next_frame(self, bullet):
        """Get next frame to pick bullet at.

        Parameters
        ----------
        bullet : :class:`compas_rcf.fab_data.ClayBullet`
            Bullet to place

        Returns
        -------
        :class:`compas.geometry.Frame`
        """
        idx = self.counter % self.n_pick_frames
        self.counter += 1

        log.debug("Counter at: {}, Frame index at {}".format(self.counter, idx))

        location_frame = self.pick_frames[idx]

        pick_height = bullet.height * (
            1 - fab_conf["movement"]["compress_at_pick"].get()
        )
        frame = get_offset_frame(location_frame, pick_height)

        log.debug("Pick frames: {}".format(frame))

        return frame

    @classmethod
    def from_data(cls, data):
        """TODO: Docstring for function.

        Parameters
        ----------
        arg1 : TODO

        Returns
        -------
        TODO

        """
        frames = [Frame.from_data(frame_data) for frame_data in data]

        return cls(frames)
