from __future__ import division, absolute_import, print_function
import math as m

import Rhino.Geometry as rg

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


def _shooting_moves(plane, entry_exit_offset, sleep=.2):
    script = ""

    entry_exit_plane = _get_offset_plane(plane, entry_exit_offset)

    script += _default_movel(entry_exit_plane)
    script += _default_movel(plane)

    script += ur_standard.set_digital_out(ACTUATOR_IO, True)
    script += ur_standard.sleep(sleep)

    script += _default_movel(entry_exit_plane)

    script += ur_standard.set_digital_out(ACTUATOR_IO, False)

    return script


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
                  tool_rotation=0,
                  picking_rotation=0,
                  tool_height_correction=0,
                  z_calib_picking=0,
                  z_calib_placing=0,
                  entry_exit_offset=-40,
                  push_transformations=None):
    reload(comm)
    reload(ur_standard)

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

    if push_transformations is not None:
        if len(push_transformations) != len(placing_planes):
            raise Exception('Mismatched length between list of placing planes and list of pushing transformations')
        execute_push_moves = True
    else:
        execute_push_moves = False

    j = 0
    instructions = []
    for i, placing_plane in enumerate(placing_planes):
        instruction = []

        instruction.append(placing_plane)

        if execute_push_moves and push_transformations[i] is not None and push_transformations[i] != [None]:
            instruction.append(None)
            instruction.append(push_transformations[i])
        else:
            # if out of picking planes start at the first one again
            j += 1
            j = j % len(picking_planes)
            instruction.append(picking_planes[j])
            instruction.append(None)

        instructions.append(instruction)

    # Send Robot to an initial known configuration ###
    pos = [m.radians(202), m.radians(-85), m.radians(87), m.radians(-92), m.radians(-89), m.radians(24)]
    script += ur_standard.move_j(pos, 0.15, 0.15)

    # Start general clay fabrication process ###
    for instruction in instructions:
        placing_plane, picking_plane, push_Ts = instruction

        # Pick clay
        if picking_plane is not None:
            # apply z calibration specific to picking station
            picking_plane.Translate(rg.Vector3d(0, 0, z_calib_picking))

            script += _picking_moves(picking_plane, entry_exit_offset, picking_rotation)

            # Move to safe travel plane   ###
            script += _safe_travel_plane_moves(safe_travel_planes)

        # Placing bullet
        # apply z calibration specific to placing station
        placing_plane.Translate(rg.Vector3d(0, 0, z_calib_placing))

        if push_Ts is not None:
            script += _push_moves(placing_plane, push_Ts, entry_exit_offset)
        else:
            script += _shooting_moves(placing_plane, entry_exit_offset)

        # Move to safe travel plane   ###
        script += _safe_travel_plane_moves(safe_travel_planes, reverse=True)

    # Send Robot to a final known configuration ###
    pos = [m.radians(180), m.radians(-108), m.radians(105), m.radians(-87), m.radians(-88), m.radians(-29)]
    script += ur_standard.move_j(pos, 0.1, 0.1)

    # Concatenate script ###
    return comm.concatenate_script(script)
