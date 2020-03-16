from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
from itertools import cycle

from compas.geometry import Frame

from compas_rcf.fabrication.conf import FABRICATION_CONF as fab_conf
from compas_rcf.utils.util_funcs import get_offset_frame

log = logging.getLogger(__name__)


class PickSetup(object):
    """Picking station setup with multiple sets of picking locations."""

    def __init__(self, plate_ids, plate_frames):
        """Init function for PickSetup.

        Parameters
        ----------
        plate_indicies : list of ints
            Identifiers of the plates
        plate_frames : list of list of :class:`compas.geometry.Frame`
            List of list of picking frames for every plate
        """
        self.plate_ids = plate_ids
        self.plate_frames = plate_frames

        self.counters = {}

        for id_ in plate_ids:
            self.counters.update({id_: 0})

        self.plate_indices = {}

        for id_, frames in zip(self.plate_ids, self.plate_frames):
            dict_ = {id_: list(range(len(frames)))}
            self.plate_indices.update(dict_)

    def get_next_frames(self, first_bullet, n=1):
        """Get next frame to pick bullet at.

        Parameters
        ----------
        plate_id : int, optional
            Which plate to pick from, defaults to 0.
        n : int, optinal
            Number of frames of get, defaults to 1.

        Returns
        -------
        list of :class:`compas.geometry.Frame`
        """
        plate_id = self.get_plate(first_bullet.location, first_bullet.color)

        for id_ in self.counters.keys():
            log.debug("Counter {}: {}".format(id_, self.counters[id_]))

        frame_indicies = self.get_next_indices(plate_id, n)
        log.debug("Frame indices: {}".format(frame_indicies))

        location_frames = [self.plate_frames[plate_id][i] for i in frame_indicies]

        pick_height = (
            first_bullet.height * fab_conf["pick"]["compression_height_factor"].get()
        )
        frames = [get_offset_frame(frame, pick_height) for frame in location_frames]

        log.debug("Pick frames: {}".format(frames))

        return frames

    def get_next_indices(self, plate_id, num_bullets):
        """TODO: Docstring for get_next_indices.

        Parameters
        ----------
        plate_id : int
            Identifier of plate to pick from.
        n : int
            Number of picking frame positions to return.

        Returns
        -------
        list of int
            List of frame indices.
        """
        start_idx = self.counters[plate_id]
        start_idx %= len(self.plate_indices[plate_id])

        all_idx = self.plate_indices[plate_id]

        rotated_list = all_idx[start_idx:] + all_idx[:start_idx]

        inf_list = cycle(rotated_list)

        indices = []
        for _ in range(num_bullets):
            indices.append(next(inf_list))

        self.counters[plate_id] += num_bullets

        return indices

    @classmethod
    def from_data(cls, setup_dict):
        """TODO: Docstring for function.

        Parameters
        ----------
        arg1 : TODO

        Returns
        -------
        TODO

        """
        indices = setup_dict.keys()
        plate_frames = setup_dict.values()

        return cls(indices, plate_frames)

    @classmethod
    def from_fab_conf(cls):
        """Get next picking frame.

        Parameters
        ----------
        index : int
            Counter to iterate through picking positions.
        bullet_height : float
            Height of bullet to pick up.

        Returns
        -------
        :class:`PickSetup`
        """
        frames = []

        for xn in range(fab_conf["pick"]["xnum"].get()):
            for yn in range(fab_conf["pick"]["ynum"].get()):

                x = (
                    fab_conf["pick"]["origin_grid"]["x"].get()
                    + xn * fab_conf["pick"]["grid_spacing"].get()
                )
                y = (
                    fab_conf["pick"]["origin_grid"]["y"].get()
                    + yn * fab_conf["pick"]["grid_spacing"].get()
                )
                z = 0

                frame = Frame(
                    [x, y, z],
                    [*fab_conf["pick"]["xaxis"].get()],
                    [*fab_conf["pick"]["yaxis"].get()],
                )
                frames.append(frame)

        return cls([0], [frames])
