"""Configuration setup for fabrication runs."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

import confuse

log = logging.getLogger(__name__)


class ZoneDataTemplate(confuse.Template):
    """:class:`confuse.Template` for ABB zonedata."""

    # Describes the valid zone data definitions.
    ZONE_DICT = {
        "FINE": -1,
        "Z0": 0,
        "Z1": 1,
        "Z5": 5,
        "Z10": 10,
        "Z15": 15,
        "Z20": 20,
        "Z30": 30,
        "Z40": 40,
        "Z50": 50,
        "Z60": 60,
        "Z80": 80,
        "Z100": 100,
        "Z150": 150,
        "Z200": 200,
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
    "pick_conf": confuse.Path(),
    "run_data_path": confuse.Template(),  # Already type checked by argparse
    "publish_tf_xform": bool,
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
                "compress_at_pick": float,
            },
            "dist_sensor": {
                "name": str,
                "serial_port": confuse.String(default=None),
                "serial_baudrate": int,
                "max_z_adjustment": float,
                "adjust_loc_frames": bool,
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
            "zone": {
                "precise": ZoneDataTemplate(),
                "travel": ZoneDataTemplate(),
                "absj_precise": ZoneDataTemplate(),
            },
            "set_joint_pos": {
                "start": confuse.Sequence([float] * 6),
                "end": confuse.Sequence([float] * 6),
            },
        },
    },
}

fab_conf = confuse.LazyConfig("compas_rcf", modname=__name__)
