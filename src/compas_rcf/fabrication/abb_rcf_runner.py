"""Fabrication runner for Rapid Clay Fabrication project for fullscale structure.

Run from command line using :code:`python -m compas_rcf.fabrication.abb_rcf_runner`
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import questionary
from colorama import init, Fore, Style
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
from compas_rrc import Zone

from compas_rcf.utils import get_offset_frame
from compas_rcf.utils.json_ import load_bullets
from compas_rcf.utils.ui import open_file_dialog
from compas_rcf.utils.ui import print_dict_w_colors

DEFAULT_JSON_DIR = 'G:\\Shared drives\\2020_MAS\\T2_P1\\02_Groups\\Phase2\\rcf_fabrication\\02_robot_control\\04_fabrication_data_jsons\\'  # noqa: E501

# These are the default values, can be changed while script is running
ROBOT_CONF = {
    # tool & wobj
    'tool': 't_A057_MockTool01',
    'picking_wobj': 'ob_A057_WobjPicking01',
    'placing_wobj': 'ob_A057_WobjPlacing01',
    # IO
    'io_needles': 'doDNetOut1',
    'grip': 1,
    'release': 0,
    # Acceleration
    'accel': 100,  # %
    'accel_ramp': 100,  # %: The rate at which acceleration and deceleration
                        # increases as a percentage of the normal values.
    # Max Speed
    'speed_override': 100,  # %
    'speed_max_tcp': 500,  # mm/2
    # Safe positions
    'robot_joints_start_position': [-127, 54, 9, -2, 30, 7],
    'robot_joints_end_position':  [-127, 54, 9, -2, 30, 7]
}

FABRICATION_CONF = {
    'offset_distance': 120  # mm
}


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

    return get_offset_frame(picking_frame, bullet_height)


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
    if ROBOT_CONF['is_target_real']:
        client.send(SetDigital(ROBOT_CONF['tool'], do_state))
    else:
        # Custom instruction can grip a bullet in RobotStudio note the tool tip must touch the bullet
        if do_state == ROBOT_CONF['grip']:
            client.send(CustomInstruction('r_A057_RS_ToolGrip'))
        else:
            client.send(CustomInstruction('r_A057_RS_ToolRelease'))


def initial_setup(client):
    """Pre fabrication setup, speed, acceleration, tool, work object and initial pose.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    """
    client.send(SetTool(ROBOT_CONF['tool']))
    client.send(SetWorkObject(ROBOT_CONF['placing_wobj']))

    # Set Acceleration
    client.send(SetAcceleration(ROBOT_CONF['accel'], ROBOT_CONF['accel_ramp']))

    # Set Max Speed
    client.send(SetMaxSpeed(ROBOT_CONF['speed_override'], ROBOT_CONF['speed_max_tcp']))

    print('Tool, Wobj, Acc and MaxSpeed sent to robot')

    # Initial configuration
    client.send(MoveToJoints(ROBOT_CONF['robot_joints_start_position'], EXTERNAL_AXIS_DUMMY, 500, Zone.FINE))


def shutdown_procedure(client):
    """Post fabrication procedure, end pose and closing and termination of client.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    """
    client.send(MoveToJoints(ROBOT_CONF['robot_joints_end_position'], EXTERNAL_AXIS_DUMMY, 1000, Zone.FINE))

    client.send_and_wait(PrintText('Finished'))

    # Close client
    client.close()
    client.terminate()


def set_check_settings(target_select):
    """Print and prompts user for changes to default configuration.

    Parameters
    ----------
    target_select : str ('real' or 'virtual')
        Target for script, either virtual robot controller or real. From argparse.
    """
    init(autoreset=True)

    if target_select is None:
        question = questionary.select(
            "Target?",
            choices=[
                "Virtual robot",
                "Real robot",
            ]).ask()
        is_target_real = question == "Real robot"
    else:
        is_target_real = target_select == "real"

    ROBOT_CONF.update({'is_target_real': is_target_real})

    print(Fore.CYAN + Style.BRIGHT + "\nRobot configuration")

    print_dict_w_colors(ROBOT_CONF)

    # edit or confirm ROBOT_CONF
    edit_keys = questionary.checkbox(
        "Select settings to change:",
        choices=ROBOT_CONF.keys()
    ).ask()

    if edit_keys is not None:
        for key in edit_keys:
            answer = questionary.text("New value for {} [{}]:".format(key, ROBOT_CONF[key])).ask()

            if answer is not None:
                ROBOT_CONF[key] = answer
                print(Fore.BLUE + str(key) +
                      Style.RESET_ALL + " changed to: " +
                      Fore.GREEN + str(ROBOT_CONF[key]))

        print(Fore.CYAN + Style.BRIGHT + "\nRobot configuration")
        print_dict_w_colors(ROBOT_CONF)
        questionary.confirm("Is this correct?")

    # edit or confirm FABRICATION_CONF
    print(Fore.CYAN + Style.BRIGHT + "Fabrication configuration")
    print_dict_w_colors(FABRICATION_CONF)

    edit_keys = questionary.checkbox(
        "Select settings to change:",
        choices=FABRICATION_CONF.keys()
    ).ask()

    if edit_keys is not None:
        for key in edit_keys:
            answer = questionary.text("New value for {} [{}]:".format(key, FABRICATION_CONF[key])).ask()

            if answer is not None:
                ROBOT_CONF[key] = answer
                print(Fore.BLUE + str(key) +
                      Style.RESET_ALL + " changed to: " +
                      Fore.GREEN + str(ROBOT_CONF[key]))

        print(Fore.CYAN + Style.BRIGHT + "Fabrication configuration")
        print_dict_w_colors(FABRICATION_CONF)
        questionary.confirm("Is this correct?")


def send_picking(client, picking_frame):
    """Send movement and IO instructions to pick up a clay bullet.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    picking_frame : compas.geometry.Frame
        Target frame to pick up bullet
    """
    if not ROBOT_CONF['is_target_real']:
        # Custom instruction create a clay bullet in RobotStudio
        # TODO: Create bullet at picking point
        client.send(CustomInstruction('r_A057_RS_Create_Bullet'))

    # change work object before picking
    client.send(SetWorkObject(ROBOT_CONF['picking_wobj']))

    # pick bullet
    offset_picking = get_offset_frame(picking_frame, FABRICATION_CONF['offset_distance'])

    client.send(MoveToFrame(offset_picking, 500, Zone.FINE))

    client.send_and_wait(MoveToFrame(picking_frame, 500, Zone.FINE))
    # TODO: Try compress bullet a little bit before picking

    send_grip_release(client, ROBOT_CONF['grip'])

    client.send_and_wait(MoveToFrame(offset_picking, 500, Zone.FINE))


def send_placing(client, placement_frame, trajectory_to, trajectory_from):
    """Send movement and IO instructions to place a clay bullet.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    picking_frame : compas.geometry.Frame
        Target frame to pick up bullet
    """
    # change work object before placing
    client.send(SetWorkObject(ROBOT_CONF['placing_wobj']))

    # add offset placing plane to pre and post frames

    offset_placement = get_offset_frame(placement_frame, FABRICATION_CONF['offset_distance'])

    # Safe pos then vertical offset
    for frame in trajectory_to:
        client.send(MoveToFrame(frame, 500, Zone.FINE))

    client.send(MoveToFrame(offset_placement, 500, Zone.FINE))
    client.send_and_wait(MoveToFrame(placement_frame, 500, Zone.FINE))

    send_grip_release(client, ROBOT_CONF['release'])

    client.send(MoveToFrame(offset_placement, 500, Zone.FINE))

    # offset placement frame then safety frame
    for frame in trajectory_from:
        client.send(MoveToFrame(frame, 500, Zone.FINE))

    client.send_and_wait(MoveToFrame(trajectory_from[-1], 500, Zone.FINE))


def abb_run(debug=False, target_select=None):
    """Fabrication runner, sets conf, reads json input and runs fabrication process."""
    print('\ncompas_rfc abb runner\n')

    set_check_settings(target_select)

    # TODO: Add function to get latest script or previous script

    json_path = open_file_dialog(initial_dir=DEFAULT_JSON_DIR)
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

        placement_frame = bullet.placement_frame
        trajectory_to = bullet.trajectory_to
        trajectory_from = bullet.trajectory_from

        bullet_height = bullet.height

        picking_frame = get_picking_frame(bullet_height)

        # Pick bullet
        send_picking(abb, picking_frame)

        # Place bullet
        send_placing(abb, placement_frame, trajectory_to, trajectory_from)

    shutdown_procedure(abb)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', choices=('real', 'virtual'))

    args = parser.parse_args()
    abb_run(target_select=args.target)
