from __future__ import division, absolute_import, print_function
import math as m

import Rhino.Geometry as rg

from rcf import utils
from rcf.ur import ur_standard, comm

# UR movement
ROBOT_SPEED = 0.2  # m/s
ROBOT_ACCEL = 0.2  # m/s2
BLEND_RADIUS = 0.02  # m

# Tool related variables
TOOL_HEIGHT = 192  # mm

# Process related variables
ACTUATOR_IO = 4


def _get_offset_plane(rob_plane, distance):
    """
    generates an offset plane.
    archetypical use: generate entry or exit planes for robotic processes.
    """
    plane = rob_plane.Clone()
    plane.Translate(rob_plane.Normal * distance)
    return plane


def _default_movel(plane):
    return ur_standard.move_l(plane, ROBOT_ACCEL, ROBOT_ACCEL)


def _picking_moves(plane, entry_exit_offset, rotation):
    script = ""

    entry_exit_plane = _get_offset_plane(plane, entry_exit_offset)

    if rotation > 0:
        rotated_plane = plane.Clone()
        rotated_plane.Rotate(m.radians(rotation), plane.Normal)

    script += _default_movel(entry_exit_plane)
    script += _default_movel(plane)
    if rotation > 0:
        script += _default_movel(rotated_plane)
    script += _default_movel(entry_exit_plane)

    return script


def _shooting_moves(plane, entry_exit_offset, push_conf, sleep=.2):
    script = ""

    entry_exit_plane = _get_offset_plane(plane, entry_exit_offset)

    script += _default_movel(entry_exit_plane)
    script += _default_movel(plane)

    script += ur_standard.set_digital_out(ACTUATOR_IO, True)
    script += ur_standard.sleep(sleep)

    if push_conf['pushing']:
        script += _temp_push_moves(plane, push_conf)

    script += _default_movel(entry_exit_plane)

    script += ur_standard.set_digital_out(ACTUATOR_IO, False)

    return script


"""
def _push_moves(plane, transformations, entry_exit_offset):
    script = ""
    entry_exit_plane = _get_offset_plane(plane, entry_exit_offset)

    push_planes = []
    for T in transformations:
        plane.Transform(T)
        push_planes.append(plane.Clone())

    script += ur_standard.set_digital_out(ACTUATOR_IO, True)

    script += _default_movel(entry_exit_plane)
    script += _default_movel(plane)

    for p in push_planes:
        script += _default_movel(p)

    script += ur_standard.set_digital_out(ACTUATOR_IO, False)

    return script
"""


def _temp_push_moves(plane, push_conf):

    n = push_conf['n_pushes']
    dist = push_conf['push_offsets']
    angle_step = push_conf['angle_steps']
    rot_axis = push_conf['push_rotation_axis']

    script = ""

    for i in range(n):
        p_plane = plane.Clone()
        trans_vector = plane.Normal * -dist
        p_plane.Translate(trans_vector)
        p_plane.Rotate(m.radians(i + 1 * angle_step), rot_axis, plane.Origin)

        script += _default_movel(p_plane)

    return script


def _safe_travel_plane_moves(planes, reverse=False):

    if reverse:
        planes.reverse()

    script = ""
    for plane in planes:
        script += _default_movel(plane)

    return script


def clay_shooting(picking_planes,
                  placing_planes,
                  safe_travel_planes,
                  dry_run=False,
                  push_conf=None,
                  tool_rotation=0,
                  picking_rotation=0,
                  tool_height_correction=0,
                  z_calib_picking=0,
                  z_calib_placing=0,
                  entry_exit_offset=-40):
    reload(comm)  # noqa E0602
    reload(ur_standard)  # noqa E0602

    # debug setup
    # debug = []
    # viz_planes = []

    # Create a script object      ###
    script = ""

    # set tcp
    tool_height = TOOL_HEIGHT + tool_height_correction
    script += ur_standard.set_tcp_by_angles(0, 0, tool_height, 0.0, 0.0, m.pi + m.radians(tool_rotation))
    # Ensure actuator is retracted ###
    script += ur_standard.set_digital_out(ACTUATOR_IO, False)

    # setup instructions

    if not isinstance(safe_travel_planes, list):
        safe_travel_planes = [safe_travel_planes]

    for key, value in push_conf.iteritems():
        if value is None:
            continue
        if not (len(value) == len(picking_planes) or len(value) == 1):
            raise Exception('Mismatched between {} list and placing_plane list'.format(key))

    instructions = []
    for i, placing_plane in enumerate(placing_planes):
        instruction = []

        picking_plane = utils.list_elem_w_index_wrap(picking_planes, i)
        instruction.append(picking_plane)

        instruction.append(placing_plane)

        plane_push_conf = {}

        for key, value in push_conf.iteritems():
            if value is not None:
                list_elem = utils.list_elem_w_index_wrap(value, i)
                plane_push_conf.update({key: list_elem})
            else:
                plane_push_conf.update({key: None})

        instruction.append(plane_push_conf)

        instructions.append(instruction)

    # Send Robot to an initial known configuration ###
    pos = [m.radians(202), m.radians(-85), m.radians(87), m.radians(-92), m.radians(-89), m.radians(24)]
    script += ur_standard.move_j(pos, 0.15, 0.15)

    # Start general clay fabrication process ###
    for instruction in instructions:
        picking_plane, placing_plane, push_conf = instruction

        # Pick clay
        if not dry_run:
            # apply z calibration specific to picking station
            picking_plane.Translate(rg.Vector3d(0, 0, z_calib_picking))

            script += _picking_moves(picking_plane, entry_exit_offset, picking_rotation)

            # Move to safe travel plane   ###
            script += _safe_travel_plane_moves(safe_travel_planes)

        # Placing bullet
        # apply z calibration specific to placing station
        placing_plane.Translate(rg.Vector3d(0, 0, z_calib_placing))

        script += _shooting_moves(placing_plane, entry_exit_offset, push_conf)

        # Move to safe travel plane   ###
        script += _safe_travel_plane_moves(safe_travel_planes, reverse=True)

    # Send Robot to a final known configuration ###
    pos = [m.radians(180), m.radians(-108), m.radians(105), m.radians(-87), m.radians(-88), m.radians(-29)]
    script += ur_standard.move_j(pos, 0.1, 0.1)

    # Concatenate script ###
    return comm.concatenate_script(script)
