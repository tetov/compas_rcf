from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from compas_rrc import CustomInstruction
from compas_rrc import MoveToFrame
from compas_rrc import MoveToJoints
from compas_rrc import PrintText
from compas_rrc import ReadWatch
from compas_rrc import SetAcceleration
from compas_rrc import SetDigital
from compas_rrc import SetMaxSpeed
from compas_rrc import SetTool
from compas_rrc import SetWorkObject
from compas_rrc import StartWatch
from compas_rrc import StopWatch
from compas_rrc import WaitTime

from compas_rcf.fabrication.conf import FABRICATION_CONF as fab_conf
from compas_rcf.fabrication.conf import ZoneDataTemplate
from compas_rcf.utils.util_funcs import get_offset_frame

log = logging.getLogger(__name__)

# Define external axis, will not be used but required in move cmds
EXTERNAL_AXIS_DUMMY: list = []


def pre_procedure(client):
    """Pre fabrication setup, speed, acceleration, tool, work object and initial pose.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    """
    grip_and_release(client, fab_conf["tool"]["release_state"].get(int))

    client.send(SetTool(fab_conf["tool"]["tool_name"].as_str()))
    log.debug("Tool {} set.".format(fab_conf["tool"]["tool_name"].get()))
    client.send(SetWorkObject(fab_conf["wobjs"]["placing_wobj_name"].as_str()))
    log.debug(
        "Work object {} set.".format(fab_conf["wobjs"]["placing_wobj_name"].get())
    )

    # Set Acceleration
    client.send(
        SetAcceleration(
            fab_conf["speed_values"]["accel"].as_number(),
            fab_conf["speed_values"]["accel_ramp"].as_number(),
        )
    )
    log.debug("Acceleration values set.")

    # Set Max Speed
    client.send(
        SetMaxSpeed(
            fab_conf["speed_values"]["speed_override"].as_number(),
            fab_conf["speed_values"]["speed_max_tcp"].as_number(),
        )
    )
    log.debug("Speed set.")

    # Initial configuration
    client.send(
        MoveToJoints(
            fab_conf["safe_joint_positions"]["start"].get(),
            EXTERNAL_AXIS_DUMMY,
            fab_conf["movement"]["speed_travel"].as_number(),
            fab_conf["movement"]["zone_travel"].get(ZoneDataTemplate()),
        )
    )
    log.debug("Sent move to safe joint position")


def post_procedure(client):
    """Post fabrication procedure, end pose and closing and termination of client.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    """
    grip_and_release(client, fab_conf["tool"]["release_state"].get(int))

    client.send(
        MoveToJoints(
            fab_conf["safe_joint_positions"]["end"].get(),
            EXTERNAL_AXIS_DUMMY,
            fab_conf["movement"]["speed_travel"].as_number(),
            fab_conf["movement"]["zone_travel"].get(ZoneDataTemplate()),
        )
    )

    client.send_and_wait(PrintText("Finished"))

    # Close client
    client.close()
    client.terminate()


def pick_bullet(client, picking_frame):
    """Send movement and IO instructions to pick up a clay bullet.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    picking_frame : compas.geometry.Frame
        Target frame to pick up bullet
    """
    if fab_conf["target"] == "virtual":
        # Custom instruction create a clay bullet in RobotStudio
        # TODO: Create bullet at picking point
        client.send(CustomInstruction("r_A057_RS_Create_Bullet"))

    # change work object before picking
    client.send(SetWorkObject(fab_conf["wobjs"]["picking_wobj_name"].get()))

    # pick bullet
    offset_picking = get_offset_frame(
        picking_frame, fab_conf["movement"]["offset_distance"].get()
    )

    # start watch
    client.send(StartWatch())

    client.send(
        MoveToFrame(
            offset_picking,
            fab_conf["movement"]["speed_travel"].as_number(),
            fab_conf["movement"]["zone_travel"].get(ZoneDataTemplate()),
        )
    )

    client.send(
        MoveToFrame(
            picking_frame,
            fab_conf["movement"]["speed_travel"].as_number(),
            fab_conf["movement"]["zone_travel"].get(ZoneDataTemplate()),
        )
    )

    grip_and_release(client, fab_conf["tool"]["grip_state"].get(int))

    client.send(
        MoveToFrame(
            offset_picking,
            fab_conf["movement"]["speed_picking"].as_number(),
            fab_conf["movement"]["zone_pick"].get(ZoneDataTemplate()),
        )
    )

    client.send(StopWatch())

    return client.send(ReadWatch())


def place_bullet(client, bullet):
    """Send movement and IO instructions to place a clay bullet.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    picking_frame : compas.geometry.Frame
        Target frame to pick up bullet
    """
    log.debug("Location frame: {}".format(bullet.location))

    # change work object before placing
    client.send(SetWorkObject(fab_conf["wobjs"]["placing_wobj_name"].as_str()))

    # add offset placing plane to pre and post frames

    top_bullet_frame = get_offset_frame(bullet.location, bullet.height)
    offset_placement = get_offset_frame(
        top_bullet_frame, fab_conf["movement"]["offset_distance"].as_number()
    )

    # start watch
    client.send(StartWatch())

    # Safe pos then vertical offset
    for frame in bullet.trajectory_to:
        client.send(
            MoveToFrame(
                frame,
                fab_conf["movement"]["speed_travel"].as_number(),
                fab_conf["movement"]["zone_travel"].get(ZoneDataTemplate()),
            )
        )

    client.send(
        MoveToFrame(
            offset_placement,
            fab_conf["movement"]["speed_travel"].as_number(),
            fab_conf["movement"]["zone_travel"].get(ZoneDataTemplate()),
        )
    )
    client.send(
        MoveToFrame(
            top_bullet_frame,
            fab_conf["movement"]["speed_placing"].as_number(),
            fab_conf["movement"]["zone_place"].get(ZoneDataTemplate()),
        )
    )

    grip_and_release(client, fab_conf["tool"]["release_state"].get(int))

    client.send(
        MoveToFrame(
            bullet.placement_frame,
            fab_conf["movement"]["speed_placing"].as_number(),
            fab_conf["movement"]["zone_place"].get(ZoneDataTemplate()),
        )
    )

    client.send(
        MoveToFrame(
            offset_placement,
            fab_conf["movement"]["speed_travel"].as_number(),
            fab_conf["movement"]["zone_travel"].get(ZoneDataTemplate()),
        )
    )

    # offset placement frame then safety frame
    for frame in bullet.trajectory_from:
        client.send(
            MoveToFrame(
                frame,
                fab_conf["movement"]["speed_travel"].as_number(),
                fab_conf["movement"]["zone_travel"].get(ZoneDataTemplate()),
            )
        )

    client.send(StopWatch())

    return client.send(ReadWatch())


def grip_and_release(client, do_state):
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
    if fab_conf["target"] == "real":
        client.send(WaitTime(fab_conf["tool"]["wait_before_io"].as_number()))
        client.send(SetDigital(fab_conf["tool"]["io_needles_pin"].as_str(), do_state))
        client.send(WaitTime(fab_conf["tool"]["wait_after_io"].as_number()))
    else:
        # Custom instruction can grip a bullet in RobotStudio
        # note the tool tip must touch the bullet
        if do_state == fab_conf["tool"]["grip_state"].get(int):
            client.send(CustomInstruction("r_A057_RS_ToolGrip"))
        else:
            client.send(CustomInstruction("r_A057_RS_ToolRelease"))

    log.debug(
        "Signal sent to {}".format(
            "grip" if do_state == fab_conf["tool"]["grip_state"].get(int) else "release"
        )
    )
