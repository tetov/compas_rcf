"""Configuration setup for fabrication runs."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

import confuse

from compas_rcf.abb import ZONE_DICT

log = logging.getLogger(__name__)


class ZoneDataTemplate(confuse.Template):
    """:class:`confuse.Template` for ABB zonedata."""

    def __init__(self, default=confuse.REQUIRED):
        super(ZoneDataTemplate, self).__init__(default=default)

    def convert(self, value, view):
        if isinstance(value, (int, float)):
            if not -1 >= value >= 2000:  # arbitrary max value
                self.fail("ZoneData needs to be from -1 to 2000", view)
            return value
        if value.upper() not in ZONE_DICT.keys():
            self.fail(
                "ZoneData must match one of {0}".format(", ".join(ZONE_DICT.keys())),
                view,
            )
        return ZONE_DICT[value.upper()]


ABB_RCF_CONF_TEMPLATE = {
    # The following is set by command line arguments
    "debug": confuse.TypeTemplate(bool, default=False),
    "quiet": confuse.TypeTemplate(bool, default=False),
    "skip_logfile": bool,
    "skip_progress_file": bool,
    "target": str,
    "paths": {
        "log_dir": confuse.Filename(),
        "pick_conf_path": confuse.Filename(),
        "fab_data_path": confuse.Filename(),
    },
    "wobjs": {"picking_wobj_name": str, "placing_wobj_name": str},
    "tool": {
        "tool_name": str,
        "io_needles_pin": str,
        "grip_state": int,
        "release_state": int,
        "wait_before_io": float,
        "wait_after_io": float,
    },
    "speed_values": {
        "speed_override": float,
        "speed_max_tcp": float,
        "accel": float,
        "accel_ramp": float,
    },
    "safe_joint_positions": {
        "start": confuse.Sequence([float] * 6),
        "end": confuse.Sequence([float] * 6),
    },
    "movement": {
        "offset_distance": float,
        "speed_placing": float,
        "speed_picking": float,
        "speed_travel": float,
        "zone_travel": ZoneDataTemplate(),
        "zone_pick": ZoneDataTemplate(),
        "zone_place": ZoneDataTemplate(),
        "compress_at_pick": float,
    },
    "docker": {"timeout_ping": float, "sleep_after_up": float},
}

fab_conf = confuse.LazyConfig("compas_rcf", modname=__name__)
