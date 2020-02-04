from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math as m

import Rhino.Geometry as rg

from compas_rcf.ur import comm
from compas_rcf.ur import ur_standard
from compas_rcf.ur.visualize_urscript import visualize_urscript
from compas_rcf.utils.util_funcs import list_elem_w_index_wrap

# UR movement
ROBOT_L_SPEED = 0.6  # m/s
ROBOT_ACCEL = 0.8  # m/s2
ROBOT_SAFE_SPEED = .8
ROBOT_J_SPEED = .8
BLEND_RADIUS_PUSHING = .002  # m

# Tool related variables
TOOL_HEIGHT = 192  # mm
ACTUATOR_IO = 4


def _get_offset_plane(initial_plane, dist, vertical_offset_bool):
    """
    generates an offset plane.
    archetypical use: generate entry or exit planes for robotic processes.
    """

    plane_normal = initial_plane.Normal

    if vertical_offset_bool:
        directions = [rg.Vector3d(0, 0, -1), plane_normal]
    else:
        directions = [plane_normal, plane_normal]

    entry_plane = initial_plane.Clone()
    exit_plane = initial_plane.Clone()

    entry_plane.Translate(directions[0] * dist)
    exit_plane.Translate(directions[1] * dist)

    return entry_plane, exit_plane


def _default_movel(plane, blend_radius=0):
    return ur_standard.move_l(plane, ROBOT_L_SPEED, ROBOT_ACCEL, blend_radius=blend_radius)


def _picking_moves(plane, entry_exit_offset, rotation, vertical_offset_bool):
    script = ""

    entry_plane, exit_plane = _get_offset_plane(plane, entry_exit_offset, vertical_offset_bool)

    if rotation > 0:
        rotated_plane = plane.Clone()
        rotated_plane.Rotate(m.radians(rotation), plane.Normal)

    script += _default_movel(entry_plane)
    script += _default_movel(plane)
    if rotation > 0:
        script += _default_movel(rotated_plane)
    script += _default_movel(exit_plane)

    return script


def _shooting_moves(plane, entry_exit_offset, push_conf, vertical_offset_bool, sleep=.5):
    script = ""

    entry_plane, exit_plane = _get_offset_plane(plane, entry_exit_offset, vertical_offset_bool)

    script += _default_movel(entry_plane)
    script += _default_movel(plane)

    script += ur_standard.set_digital_out(ACTUATOR_IO, True)
    script += ur_standard.sleep(sleep)

    if push_conf['pushing']:
        script += _push_moves(plane, push_conf, vertical_offset_bool)

    script += _default_movel(exit_plane)

    script += ur_standard.set_digital_out(ACTUATOR_IO, False)

    return script


def _push_moves(plane, push_conf, vertical_offset_bool):

    n = push_conf['n_pushes']
    dist = push_conf['push_offsets']
    angle_step = push_conf['angle_steps']
    rot_axis = push_conf['push_rotation_axis']

    script = ""

    offset_plane = plane.Clone()
    if vertical_offset_bool:
        direction = rg.Vector3d(0, 0, -1)
    else:
        direction = plane.Normal

    offset_plane.Translate(direction * -dist)

    for i in range(n):
        rot_plane = offset_plane.Clone()

        rot_plane.Rotate(m.radians((i + 1) * angle_step), rot_axis, plane.Origin)

        script += _default_movel(rot_plane, blend_radius=BLEND_RADIUS_PUSHING)

    return script


def _safe_travel_moves(safe_pos_list, reverse=False):

    if reverse:
        safe_pos_list = safe_pos_list[::-1]

    script = ""
    for safe_pos in safe_pos_list:
        script += ur_standard.move_j(safe_pos, ROBOT_SAFE_SPEED, ROBOT_ACCEL)

    return script


def ur_clay_shooting(picking_planes,
                     placing_planes,
                     safe_pos_list,
                     dry_run=False,
                     push_conf={'pushing': [False]},
                     tool_rotation=0,
                     picking_rotation=0,
                     tool_height_correction=0,
                     z_calib_picking=0,
                     z_calib_placing=0,
                     entry_exit_offset=-40,
                     vertical_offset_bool=False,
                     viz_planes_bool=False,
                     placing_index=0):

    reload(comm)  # noqa E0602
    reload(ur_standard)  # noqa E0602

    # extract planes if input is ClayBullets
    if not is_elems_rgPlane(placing_planes):
        placing_planes = [bullet.plane.Clone() for bullet in placing_planes]

    # Create a string object to store script
    script = ""

    # set tcp
    tool_height = TOOL_HEIGHT + tool_height_correction
    script += ur_standard.set_tcp_by_plane_angles(0, 0, tool_height, 0.0, 0.0, m.radians(tool_rotation))
    # Ensure actuator is retracted ###
    script += ur_standard.set_digital_out(ACTUATOR_IO, False)

    # Send Robot to an initial known configuration ###
    script += ur_standard.move_j(safe_pos_list[0], ROBOT_ACCEL, ROBOT_SAFE_SPEED)

    # setup instructions

    for key, value in push_conf.iteritems():
        if value is None:
            continue
        if len(value) == len(placing_planes) or len(value) == 1:
            continue

        raise Exception('Mismatched between {} list and placing_plane list'.format(key))

    instructions = []
    for i, placing_plane in enumerate(placing_planes):
        instruction = []

        picking_plane = list_elem_w_index_wrap(picking_planes, i)
        instruction.append(picking_plane)

        instruction.append(placing_plane)

        plane_push_conf = {}

        for key, value in push_conf.iteritems():
            if value is not None:
                list_elem = list_elem_w_index_wrap(value, i)
                plane_push_conf.update({key: list_elem})
            else:
                plane_push_conf.update({key: None})

        instruction.append(plane_push_conf)

        instructions.append(instruction)

    # Start general clay fabrication process ###
    for i, instruction in enumerate(instructions):
        picking_plane, placing_plane, push_conf = instruction

        # Pick clay
        if not dry_run:
            # apply z calibration specific to picking station
            picking_plane.Translate(rg.Vector3d(0, 0, z_calib_picking))

            script += _picking_moves(picking_plane, entry_exit_offset, picking_rotation, vertical_offset_bool)

        # safe moves
        script += _safe_travel_moves(safe_pos_list)

        # apply z calibration specific to placing station
        placing_plane.Translate(rg.Vector3d(0, 0, z_calib_placing))

        script += _shooting_moves(placing_plane, entry_exit_offset, push_conf, vertical_offset_bool)
        script += ur_standard.UR_log('Bullet {} placed.'.format(i + placing_index))

        # safe moves
        script += _safe_travel_moves(safe_pos_list, reverse=True)

    if viz_planes_bool:
        viz_planes = visualize_urscript(script)
    else:
        viz_planes = None

    return comm.concatenate_script(script), viz_planes


def is_elems_rgPlane(obj):
    """ From https://stackoverflow.com/a/18495146
    """
    return bool(obj) and all(isinstance(elem, rg.Plane) for elem in obj)
