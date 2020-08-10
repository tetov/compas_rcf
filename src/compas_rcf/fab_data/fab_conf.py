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
    "log_dir": confuse.Filename(),
    "fab_data": confuse.Path(),
    "pick_conf": confuse.Path(),
    "robot_client": {
        "docker": {"timeout_ping": float, "sleep_after_up": float},
        "controller": str,
        "wobjs": {"pick": str, "place": str},
        "tools": {
            "pick_place": {
                "name": str,
                "io_pin_needles": str,
                "extend_signal": int,
                "retract_signal": int,
                "needles_pause": float,
                "compress_at_pick": float,
            },
            "dist_sensor": {
                "name": str,
                "serial_port": confuse.String(default=None),
                "serial_baudrate": int,
                "max_z_adjustment": float,
            },
        },
        "robot_movement": {
            "global_speed_accel": {
                "speed_override": float,
                "speed_max_tcp": float,
                "accel": float,
                "accel_ramp": float,
            },
            "speed": {"precise": float, "travel": float},
            "zone": {"precise": ZoneDataTemplate(), "travel": ZoneDataTemplate()},
            "set_joint_pos": {
                "start": confuse.Sequence([float] * 6),
                "end": confuse.Sequence([float] * 6),
            },
        },
    },
}

fab_conf = confuse.LazyConfig("compas_rcf", modname=__name__)
