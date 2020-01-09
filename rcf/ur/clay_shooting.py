from __future__ import division, absolute_import, print_function
import math as m

import Rhino.Geometry as rg

from rcf.ur import ur_standard, comm

# UR movement
ROBOT_SPEED = 0.2  # m/s
ROBOT_ACCEL = 0.2  # m/s2
BLEND_RADIUS = 0.02  # m

# Tool related variables      ###
TOOL_HEIGHT = 192  # mm

# Process related variables   ###
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


def clay_shooting(picking_planes, placing_planes, safe_travel_plane,
                  picking_rotation=0,
                  tool_height_correction=0, z_calib_picking=0,
                  z_calib_placing=0, entry_exit_offset=-40):
    reload(comm)
    reload(ur_standard)

    # debug setup
    # debug = []
    # viz_planes = []

    # Create a script object      ###
    script = ""

    # set tcp
    tool_height = TOOL_HEIGHT + tool_height_correction
    script += ur_standard.set_tcp_by_angles(0, 0, tool_height, 0.0, 0.0, m.pi + m.radians(0))
    # Ensure actuator is retracted ###
    script += ur_standard.set_digital_out(ACTUATOR_IO, False)

    # Send Robot to an initial known configuration ###
    pos = [m.radians(202), m.radians(-85), m.radians(87), m.radians(-92), m.radians(-89), m.radians(24)]
    script += ur_standard.move_j(pos, 0.15, 0.15)

    # Start general clay fabrication process ###
    for i, picking_plane in enumerate(picking_planes):
        if i > len(placing_planes) - 1:
            break

        # apply z calibration specific to picking station
        picking_plane.Translate(rg.Vector3d(0, 0, z_calib_picking))

        # Pick clay                   ###
        entry_exit_pick_plane = _get_offset_plane(picking_plane, entry_exit_offset)

        if picking_rotation > 0:
            rotated_picking_plane = picking_plane.Clone()
            rotated_picking_plane.Rotate(m.radians(picking_rotation), picking_plane.Normal)

        script += _default_movel(entry_exit_pick_plane)
        script += _default_movel(picking_plane)
        if picking_rotation > 0:
            script += _default_movel(rotated_picking_plane)
        script += _default_movel(entry_exit_pick_plane)

        # Move to safe travel plane   ###
        # TODO: Allow for list of safe planes
        script += _default_movel(safe_travel_plane)

        # Place clay                  ###

        placing_plane = placing_planes[i]

        # apply z calibration specific to placing station
        placing_plane.Translate(rg.Vector3d(0, 0, z_calib_placing))

        entry_exit_place_plane = _get_offset_plane(placing_plane, entry_exit_offset)

        script += _default_movel(entry_exit_place_plane)
        script += _default_movel(placing_plane)
        script += ur_standard.set_digital_out(ACTUATOR_IO, True)
        script += ur_standard.sleep(0.2)
        script += _default_movel(entry_exit_place_plane)
        script += ur_standard.set_digital_out(ACTUATOR_IO, False)

        # Move to safe travel plane   ###
        # TODO: Allow for list of safe planes
        script += _default_movel(safe_travel_plane)

    # Send Robot to a final known configuration ###
    pos = [m.radians(180), m.radians(-108), m.radians(105), m.radians(-87), m.radians(-88), m.radians(-29)]
    script += ur_standard.move_j(pos, 0.1, 0.1)

    # Concatenate script ###
    return comm.concatenate_script(script)
