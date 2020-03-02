from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

import confuse
import questionary

from compas_rcf.utils import ui

import pathlib

__all__ = ["FABRICATION_CONF"]

log = logging.getLogger(__name__)

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


class ZoneDataTemplate(confuse.Template):
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


ROBOT_CONTROL_FOLDER_DRIVE = pathlib.Path(
    "G:\\Shared drives\\2020_MAS\\T2_P1\\02_Groups\\Phase2\\rcf_fabrication\\02_robot_control"  # noqa E501
)
DEFAULT_CONF_DIR = ROBOT_CONTROL_FOLDER_DRIVE / "05_fabrication_confs"
DEFAULT_JSON_DIR = ROBOT_CONTROL_FOLDER_DRIVE / "04_fabrication_data_jsons"
DEFAULT_LOG_DIR = ROBOT_CONTROL_FOLDER_DRIVE / "06_fabrication_logs"


class Path(confuse.Filename):
    """A template that validates strings as `pathlib.Path` objects.

    Filenames are parsed equivalent to the `Filename` template and then
    converted to `pathlib.Path` objects.
    For Python 2 it returns the original path as returned by the `Filename`
    template.

    From upstream master, commit by Szabolcs on Github.
    https://github.com/beetbox/confuse/commit/6c97e03d125cbbae5ce08040b1207d33ae3ef01c
    """

    def value(self, view, template=None):
        return pathlib.Path(super(Path, self).value(view, template))


abb_rcf_conf_template = {
    # Two following is set by command line arguments
    "debug": confuse.TypeTemplate(bool, default=False),
    "verbose": confuse.TypeTemplate(bool, default=False),
    # is_target_real is set either by command line argument, during run or in conf file
    "target": confuse.TypeTemplate(str, default=None),
    "paths": {
        "json_dir": confuse.Filename(default=str(DEFAULT_JSON_DIR)),
        "conf_dir": confuse.Filename(default=str(DEFAULT_JSON_DIR)),
        "log_dir": confuse.Filename(default=str(DEFAULT_LOG_DIR)),
    },
    "wobjs": {"picking_wobj_name": str, "placing_wobj_name": str},
    "tool": {
        "tool_name": str,
        "io_needles_pin": str,
        "grip_state": int,
        "release_state": int,
        "wait_before_io": confuse.Number(default=2),
        "wait_after_io": confuse.Number(default=0.5),
    },
    "speed_values": {
        "speed_override": confuse.Number(default=100),
        "speed_max_tcp": float,
        "accel": float,
        "accel_ramp": confuse.Number(default=100),
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
    },
    "pick": {
        "origin_grid": {
            "x": confuse.Number(default=100),
            "y": confuse.Number(default=100),
        },
        "xnum": int,
        "ynum": int,
        "grid_spacing": float,
        "compression_height_factor": confuse.Number(default=0.95),
        "xaxis": confuse.Sequence([float] * 3),
        "yaxis": confuse.Sequence([float] * 3),
    },
    "docker": {
        "timeout_ping": confuse.Number(default=10),
        "sleep_after_up": confuse.Number(default=5),
    },
}

FABRICATION_CONF = confuse.LazyConfig("FabricationRunner", modname=__name__)


def interactive_conf_setup():
    """Print and prompts user for changes to default configuration."""
    conf_sources = ["Default.", "Load."]

    """
    if confuse.CONFIG_FILENAME.exists():
        conf_sources.append("Last configuration used.")
    """

    select_conf_source = questionary.select(
        "Load config or use default?", choices=conf_sources
    ).ask()

    """
    if select_conf_source == "Load last configuration used.":
        fabrication_conf.set_file(confuse.CONFIG_FILENAME)
    """

    if select_conf_source == "Load.":
        conf_file = ui.open_file_dialog(
            initial_dir=FABRICATION_CONF["paths"]["conf_dir"].get(Path()),
            file_type=("YAML files", "*.yaml"),
        )
        # If file dialog is cancelled load default conf
        if conf_file == "":
            select_conf_source = "Default."
        else:
            FABRICATION_CONF.set_file(conf_file)
            log.info("Configuration loaded from {}".format(conf_file))

    if select_conf_source == "Default.":
        FABRICATION_CONF.read(defaults=True, user=False)
        log.info("Default configuration loaded from package")

    if not FABRICATION_CONF["target"].exists():
        question = questionary.select(
            "Target?", choices=["Virtual robot", "Real robot"], default="Virtual robot"
        ).ask()
        FABRICATION_CONF["target"] = "real" if question == "Real robot" else "virtual"

    log.info(
        "Target is {} controller.".format(FABRICATION_CONF["target"].get().upper())
    )

    # Validate conf
    FABRICATION_CONF.get(abb_rcf_conf_template)

    log.info("Configuration \n{}".format(FABRICATION_CONF.dump()))
