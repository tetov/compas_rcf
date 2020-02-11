"""Fabrication runner for Rapid Clay Fabrication project for fullscale structure.

Run from command line using :code:`python -m compas_rcf.fabrication.abb_rcf_runner`
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
from os import path

try:
    import questionary
except ModuleNotFoundError:  # Error conveniently introduced in 3.6
    raise  # Raise original exception
except ImportError:
    raise Exception('This module requires Python >=3.6')
from colorama import Fore
from colorama import Style
from colorama import init
from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector
from compas_fab.backends.ros import RosClient
from compas_rrc import AbbClient
from compas_rrc import CustomInstruction
from compas_rrc import MoveToFrame
from compas_rrc import MoveToJoints
from compas_rrc import PrintText
from compas_rrc import SetAcceleration
from compas_rrc import SetDigital
from compas_rrc import SetMaxSpeed
from compas_rrc import SetTool
from compas_rrc import SetWorkObject
from compas_rrc import WaitTime

from compas_rcf.fabrication.conf import ABB_RCF_CONF_TEMPLATE
from compas_rcf.fabrication.conf import fabrication_conf
from compas_rcf.utils import get_offset_frame
from compas_rcf.utils import ui
from compas_rcf.utils.json_ import load_bullets

ROBOT_CONTROL_FOLDER_DRIVE = 'G:\\Shared drives\\2020_MAS\\T2_P1\\02_Groups\\Phase2\\rcf_fabrication\\02_robot_control'

DEFAULT_CONF_DIR = path.join(ROBOT_CONTROL_FOLDER_DRIVE, '05_fabrication_confs')
DEFAULT_JSON_DIR = path.join(ROBOT_CONTROL_FOLDER_DRIVE, '04_fabrication_data_jsons')

# Define external axis, will not be used but required in move cmds
EXTERNAL_AXIS_DUMMY: list = []


def get_picking_frame(bullet_height):
    """Get next picking frame.

    Parameters
    ----------
    bullet_height : float
        Height of bullet to pick up

    Returns
    -------
    `class`:compas.geometry.Frame
    """
    # TODO: Set up a grid to pick from
    picking_frame = Frame(Point(0, 0, 0), Vector(0, 1, 0), Vector(1, 0, 0))

    return get_offset_frame(picking_frame, bullet_height * .95)


def send_grip_release(client, do_state):
    """Grip or release using RCF tool, either in simulation or on real robot.

    If script target is real robot this will set the digital output on the robot,
    and if the target is virtual robot it will use RobotStudio code to visualize
    clay bullet gripping and releasing

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    do_state : int (0 or 1)
        Value to set DO to
    """
    if CONF.is_target_real:
        client.send(WaitTime(.5))
        client.send(SetDigital(CONF.tool.io_needles_pin, do_state))
        client.send(WaitTime(2))
    else:
        # Custom instruction can grip a bullet in RobotStudio note the tool tip must touch the bullet
        if do_state == CONF.tool.grip_state:
            client.send(CustomInstruction('r_A057_RS_ToolGrip'))
        else:
            client.send(CustomInstruction('r_A057_RS_ToolRelease'))


def initial_setup(client):
    """Pre fabrication setup, speed, acceleration, tool, work object and initial pose.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    """
    accel = CONF.speed_values.accel
    accel_ramp = CONF.speed_values.accel_ramp
    speed_override = CONF.speed_values.speed_override
    speed_max_tcp = CONF.speed_values.speed_max_tcp

    client.send(SetTool(CONF.tool.tool_name))
    client.send(SetWorkObject(CONF.wobjs.placing_wobj_name))

    # Set Acceleration
    client.send(SetAcceleration(accel, accel_ramp))

    # Set Max Speed
    client.send(SetMaxSpeed(speed_override, speed_max_tcp))

    print('Tool, Wobj, Acc and MaxSpeed sent to robot')

    # Initial configuration
    client.send(
        MoveToJoints(CONF.safe_joint_positions.start, EXTERNAL_AXIS_DUMMY, CONF.movement.speed_travel,
                     CONF.movement.zone_travel))


def shutdown_procedure(client):
    """Post fabrication procedure, end pose and closing and termination of client.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    """
    client.send(
        MoveToJoints(CONF.safe_joint_positions.end, EXTERNAL_AXIS_DUMMY, CONF.movement.speed_travel,
                     CONF.movement.zone_travel))

    client.send_and_wait(PrintText('Finished'))

    # Close client
    client.close()
    client.terminate()


def get_settings(target_select):
    """Print and prompts user for changes to default configuration.

    Parameters
    ----------
    target_select : str ('real' or 'virtual')
        Target for script, either virtual robot controller or real. From argparse.
    """
    init(autoreset=True)

    load_or_default = questionary.select("Load config or use default?", choices=['Default', 'Load'],
                                         default='Default').ask()

    if load_or_default == 'Load':
        conf_file = ui.open_file_dialog(initial_dir=DEFAULT_CONF_DIR, file_type=('YAML files', '*.yaml'))
        fabrication_conf.set_file(conf_file)
    else:
        fabrication_conf.read(defaults=True, user=False)

    global CONF

    CONF = fabrication_conf.get(ABB_RCF_CONF_TEMPLATE)  # Will raise exception if conf is invalid

    if target_select is None:
        question = questionary.select("Target?", choices=["Virtual robot", "Real robot"], default='Virtual robot').ask()
        CONF.is_target_real = question == "Real robot"
    else:
        CONF.is_target_real = target_select == "real"

    print(Fore.CYAN + Style.BRIGHT + "Configuration")

    ui.print_conf_w_colors(fabrication_conf)

    conf_ok = questionary.confirm("Configuration correct?").ask()
    if not conf_ok:
        print("Exiting.")
        sys.exit()


def send_picking(client, picking_frame):
    """Send movement and IO instructions to pick up a clay bullet.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    picking_frame : compas.geometry.Frame
        Target frame to pick up bullet
    """
    offset_distance = CONF.movement.offset_distance

    speed_travel = CONF.movement.speed_travel
    speed_picking = CONF.movement.speed_picking

    zone_pick_place = CONF.movement.zone_pick_place
    zone_travel = CONF.movement.zone_travel

    zone_travel = CONF.movement.zone_travel

    if not CONF.is_target_real:
        # Custom instruction create a clay bullet in RobotStudio
        # TODO: Create bullet at picking point
        client.send(CustomInstruction('r_A057_RS_Create_Bullet'))

    # change work object before picking
    client.send(SetWorkObject(CONF.wobjs.picking_wobj_name))

    # pick bullet
    offset_picking = get_offset_frame(picking_frame, offset_distance)

    client.send(MoveToFrame(offset_picking, speed_travel, zone_travel))

    client.send_and_wait(MoveToFrame(picking_frame, speed_picking, zone_pick_place))
    # TODO: Try compress bullet a little bit before picking

    send_grip_release(client, CONF.tool.grip_state)

    client.send_and_wait(MoveToFrame(offset_picking, speed_travel, zone_travel))


def send_placing(client, bullet):
    """Send movement and IO instructions to place a clay bullet.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    picking_frame : compas.geometry.Frame
        Target frame to pick up bullet
    """
    offset_distance = CONF.movement.offset_distance

    speed_travel = CONF.movement.speed_travel
    speed_placing = CONF.movement.speed_placing

    zone_pick_place = CONF.movement.zone_pick_place
    zone_travel = CONF.movement.zone_travel

    # change work object before placing
    client.send(SetWorkObject(CONF.wobjs.placing_wobj_name))

    # add offset placing plane to pre and post frames

    offset_placement = get_offset_frame(bullet.placement_frame, offset_distance)
    top_bullet_frame = get_offset_frame(bullet.location, bullet.height)

    # Safe pos then vertical offset
    for frame in bullet.trajectory_to:
        client.send(MoveToFrame(frame, speed_travel, zone_travel))

    client.send(MoveToFrame(offset_placement, speed_travel, zone_travel))
    client.send(MoveToFrame(top_bullet_frame, speed_travel, zone_travel))

    send_grip_release(client, CONF.tool.release_state)

    client.send_and_wait(MoveToFrame(bullet.placement_frame, speed_placing, zone_pick_place))

    client.send(MoveToFrame(offset_placement, speed_travel, zone_travel))

    # offset placement frame then safety frame
    for frame in bullet.trajectory_from:
        client.send(MoveToFrame(frame, speed_travel, zone_travel))


def abb_run(debug=False, target_select=None):
    """Fabrication runner, sets conf, reads json input and runs fabrication process."""
    print('\ncompas_rfc abb runner\n')

    get_settings(target_select)

    # TODO: Add function to get latest script or previous script

    json_path = ui.open_file_dialog(initial_dir=DEFAULT_JSON_DIR)
    clay_bullets = load_bullets(json_path)

    # Create Ros Client
    ros = RosClient()

    # Create ABB Client
    abb = AbbClient(ros)
    abb.run()
    print('Connected.')

    # Set speed, accel, tool, wobj and move to start pos
    initial_setup(abb)

    for bullet in clay_bullets:

        picking_frame = get_picking_frame(bullet.height)

        # Pick bullet
        send_picking(abb, picking_frame)

        # Place bullet
        send_placing(abb, bullet)

    shutdown_procedure(abb)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', choices=('real', 'virtual'))

    args = parser.parse_args()
    abb_run(target_select=args.target)
