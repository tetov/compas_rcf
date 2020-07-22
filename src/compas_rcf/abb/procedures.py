"""Procedures for pick and place operations on ABB robot arms."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

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

from compas_rcf.fab_data import ZoneDataTemplate
from compas_rcf.fab_data import fab_conf
from compas_rcf.utils import get_offset_frame

log = logging.getLogger(__name__)

# Define external axis, will not be used but required in move cmds
EXTERNAL_AXIS_DUMMY: list = []


def pre_procedure(client):
    """Pre fabrication setup, speed, acceleration, tool, work object and initial pose.

    Uses ``fab_conf`` set up using
    :func:`compas_rcf.fab_data.interactive_conf_setup` for fabrication settings.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
        Client connected to controller procedure should be sent to.
    """
    grip_and_release(
        client,
        fab_conf["tool"]["io_needles_pin"].get(),
        fab_conf["tool"]["release_state"].get(),
        wait_before=fab_conf["tool"]["wait_before_io"].get(),
        wait_after=fab_conf["tool"]["wait_after_io"].get(),
    )

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

    Uses ``fab_conf`` set up using
    :func:`compas_rcf.fab_data.interactive_conf_setup` for fabrication settings.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    """
    grip_and_release(
        client,
        fab_conf["tool"]["io_needles_pin"].get(),
        fab_conf["tool"]["release_state"].get(),
        wait_before=fab_conf["tool"]["wait_before_io"].get(),
        wait_after=fab_conf["tool"]["wait_after_io"].get(),
    )

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

    Uses ``fab_conf`` set up using
    :func:`compas_rcf.fab_data.interactive_conf_setup` for fabrication settings.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    picking_frame : :class:`compas.geometry.Frame`
        Target frame to pick up bullet
    """
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
            fab_conf["movement"]["zone_pick"].get(ZoneDataTemplate()),
        )
    )

    grip_and_release(
        client,
        fab_conf["tool"]["io_needles_pin"].get(),
        fab_conf["tool"]["grip_state"].get(),
        wait_before=fab_conf["tool"]["wait_before_io"].get(),
        wait_after=fab_conf["tool"]["wait_after_io"].get(),
    )

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

    Uses ``fab_conf`` set up using
    :func:`compas_rcf.fab_data.interactive_conf_setup` for fabrication settings.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
        Client connected to controller procedure should be sent to.
    bullet : :class:`compas_rcf.fab_data.ClayBullet`
        Bullet to place.

    Returns
    -------
    :class:`compas_rrc.FutureResult`
        Object which blocks while waiting for feedback from robot. Calling result on
        this object will return the time the procedure took.
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

    grip_and_release(
        client,
        fab_conf["tool"]["io_needles_pin"].get(),
        fab_conf["tool"]["release_state"].get(),
        wait_before=fab_conf["tool"]["wait_before_io"].get(),
        wait_after=fab_conf["tool"]["wait_after_io"].get(),
    )

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


def grip_and_release(client, do_name, do_state, wait_before=1.0, wait_after=1.0):
    """Grip or release using RCF tool, either in simulation or on real robot.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
        Client connected to controller procedure should be sent to.
    io_name : :class:`str`
        Name of DO as defined on controller.
    do_state : :class:`bool` or :class:`int` (0 or 1)
        Value to set DO to
    wait_before : :class:`float`, optional
        Time to wait in position before setting DO state. Defaults to ``1.``
    wait_after : :class:`float`, optional
        Time to wait in position after setting DO state. Defaults to ``1.``
    """
    client.send(WaitTime(wait_before))
    client.send(SetDigital(do_name, do_state))
    client.send(WaitTime(wait_after))

    log.debug("IO {} set to {}.".format(do_name, do_state))
