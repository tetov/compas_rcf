"""Configuration setup for fabrication runs."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

import compas_rrc
import confuse

log = logging.getLogger(__name__)


class ZoneDataTemplate(confuse.Template):
    """:class:`confuse.Template` for ABB zonedata."""

    # Describes the valid zone data definitions.
    ZONE_DICT = {
        key: value
        for key, value in vars(compas_rrc.Zone).items()
        if not key.startswith("__")
    }

    def __init__(self, default=confuse.REQUIRED):
        super(ZoneDataTemplate, self).__init__(default=default)

    def convert(self, value, view):
        """Convert zonedata from :obj:`str` to number if needed."""
        if isinstance(value, (int, float)):
            if not -1 >= value >= 2000:  # arbitrary max value
                self.fail("ZoneData needs to be from -1 to 2000", view)
            return value
        if value.upper() not in self.ZONE_DICT.keys():
            self.fail(
                "ZoneData must match one of {0}".format(
                    ", ".join(self.ZONE_DICT.keys())
                ),
                view,
            )
        return self.ZONE_DICT[value.upper()]


ABB_RCF_CONF_TEMPLATE = {
    "log_dir": confuse.Filename(),
    "run_data_path": confuse.Template(),  # Already type checked by argparse
    "robot_client": {
        "controller": str,
        "docker": {"timeout_ping": float, "sleep_after_up": float},
        "wobjs": {"pick": str, "place": str},
        "tools": {
            "pick_place": {
                "name": str,
                "io_pin_needles": str,
                "extend_signal": int,
                "retract_signal": int,
                "needles_pause": float,
            },
        },
        "robot_movement": {
            "global_speed_accel": {
                "speed_override": float,
                "speed_max_tcp": float,
                "accel": float,
                "accel_ramp": float,
            },
            "speed": {
                "pick": float,
                "travel": float,
                "place": float,
            },
            "zone": {
                "pick": ZoneDataTemplate(),
                "place": ZoneDataTemplate(),
                "travel": ZoneDataTemplate(),
            },
            "joint_positions": {
                "start": confuse.Sequence([float] * 6),
                "end": confuse.Sequence([float] * 6),
                "travel_trajectory": confuse.TypeTemplate(list, default=None),
            },
        },
    },
}

fab_conf = confuse.LazyConfig("rapid_clay_formations_fab", modname=__name__)
