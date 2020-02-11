from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_rcf.abb.helpers import ZONE_DICT
import confuse


class ZoneDataTemplate(confuse.Template):
    def __init__(self, default=confuse.REQUIRED):
        super(ZoneDataTemplate, self).__init__(default=default)

    def convert(self, value, view):
        if isinstance(value, (int, float)):
            if not -1 >= value >= 2000:  # arbitrary max value
                self.fail(u"ZoneData needs to be from -1 to 2000", view)
            return value
        if value.upper() not in ZONE_DICT.keys():
            self.fail(u"ZoneData must match one of {0}".format(", ".join(ZONE_DICT.keys())), view)
        print(value)
        print(ZONE_DICT[value.upper()])
        return ZONE_DICT[value.upper()]


ABB_RCF_CONF_TEMPLATE = {
    'is_target_real': confuse.TypeTemplate(bool, default=False),
    'wobjs': {
        'picking_wobj_name': str,
        'placing_wobj_name': str,
    },
    'tool': {
        'tool_name': str,
        'io_needles_pin': str,
        'grip_state': int,
        'release_state': int,
    },
    'speed_values': {
        'speed_override': float,
        'speed_max_tcp': float,
        'accel': float,
        'accel_ramp': float,
    },
    'safe_joint_positions': {
        'start': confuse.Sequence([float] * 6),
        'end': confuse.Sequence([float] * 6)
    },
    'movement': {
        'offset_distance': float,
        'speed_placing': float,
        'speed_picking': float,
        'speed_travel': float,
        'zone_travel': ZoneDataTemplate(),
        'zone_pick_place': ZoneDataTemplate(),
    },
}


def get_numerical_zone_value(zone_data):
    """Take input and return numerical zone data.

    Parameters
    ----------
    zone_value : str, float or int
        Either zone data in mm or one of RAPID's defined variable names for zone data

    Returns
    -------
    float or int
        zone data in mm
    """
    return ZONE_DICT[zone_data.upper()]


fabrication_conf = confuse.LazyConfig('FabricationRunner', __name__)
