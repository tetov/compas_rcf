"""Procedures for pick and place operations on ABB robot arms."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from compas_rrc import FeedbackLevel
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
from compas_rcf.sensing import get_distance_measurement
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
    # for safety
    retract_needles(client)

    client.send(SetTool(fab_conf["tools"]["pick_place"]["tool_name"].as_str()))
    log.debug("Tool {} set.".format(fab_conf["tools"]["pick_place"]["tool_name"].get()))
    client.send(SetWorkObject(fab_conf["wobjs"]["placing_wobj_name"].as_str()))
    log.debug(
        "Work object {} set.".format(fab_conf["wobjs"]["placing_wobj_name"].get())
    )

    # Set Acceleration
    client.send(
        SetAcceleration(
            fab_conf["robot_movement"]["accel"].as_number(),
            fab_conf["robot_movement"]["accel_ramp"].as_number(),
        )
    )
    log.debug("Acceleration values set.")

    # Set Max Speed
    client.send(
        SetMaxSpeed(
            fab_conf["robot_movement"]["speed_override"].as_number(),
            fab_conf["robot_movement"]["speed_max_tcp"].as_number(),
        )
    )
    log.debug("Speed set.")

    # Initial configuration
    client.send(
        MoveToJoints(
            fab_conf["robot_joint_pos"]["start"].get(),
            EXTERNAL_AXIS_DUMMY,
            fab_conf["robot_movement"]["speed_travel"].as_number(),
            fab_conf["robot_movement"]["zone_travel"].get(ZoneDataTemplate()),
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
    retract_needles(client)

    client.send(
        MoveToJoints(
            fab_conf["robot_joint_pos"]["end"].get(),
            EXTERNAL_AXIS_DUMMY,
            fab_conf["robot_movement"]["speed_travel"].as_number(),
            fab_conf["robot_movement"]["zone_travel"].get(),
        )
    )

    client.send_and_wait(PrintText("Finished"))

    # Close client
    client.close()
    client.terminate()


def pick_bullet(client, picking_frame):
    """Send movement and IO instructions to pick up a clay bullet.

    Uses `fab_conf` set up with command line arguments and configuration
    file.

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
        picking_frame, fab_conf["robot_movement"]["offset_distance"].get()
    )

    # start watch
    client.send(StartWatch())

    client.send(
        MoveToFrame(
            offset_picking,
            fab_conf["robot_movement"]["speed_travel"].get(),
            fab_conf["robot_movement"]["zone_travel"].get(),
        )
    )

    client.send(
        MoveToFrame(
            picking_frame,
            fab_conf["robot_movement"]["speed_travel"].get(),
            fab_conf["robot_movement"]["zone_pick"].get(),
        )
    )

    client.send(WaitTime(fab_conf["robot_movement"]["needles_pause"].get()))
    extend_needles(client)
    client.send(WaitTime(fab_conf["robot_movement"]["needles_pause"].get()))

    client.send(
        MoveToFrame(
            offset_picking,
            fab_conf["robot_movement"]["speed_picking"].get(),
            fab_conf["robot_movement"]["zone_pick"].get(),
        )
    )

    client.send(StopWatch())

    return client.send(ReadWatch())


def place_bullet(client, bullet):
    """Send movement and IO instructions to place a clay bullet.

    Uses `fab_conf` set up with command line arguments and configuration
    file.

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

    # move there with distance sensor TCP active
    # client.send(SetTool(fab_conf["tools"]["dist_sensor"]["tool_name"].as_str()))

    # add offset placing plane to pre and post frames
    offset_placement = get_offset_frame(
        bullet.location,
        bullet.height + fab_conf["robot_movement"]["offset_distance"].as_number(),
    )

    # start watch
    client.send(StartWatch())

    # Safe pos then vertical offset
    for frame in bullet.trajectory_to:
        client.send(
            MoveToFrame(
                frame,
                fab_conf["robot_movement"]["speed_travel"].as_number(),
                fab_conf["robot_movement"]["zone_travel"].get(ZoneDataTemplate()),
            )
        )

    client.send(
        MoveToFrame(
            offset_placement,
            fab_conf["robot_movement"]["speed_travel"].as_number(),
            fab_conf["robot_movement"]["zone_travel"].get(ZoneDataTemplate()),
        )
    )

    client.send_and_wait(WaitTime(2, feedback_level=FeedbackLevel.NONE))

    dist_read = get_distance_measurement()
    log.debug("Dist read: {}".format(dist_read))

    tool0_to_dist_sensor_z = fab_conf["tools"]["tool0_z_dist"].get()
    tool0_to_tool_z = fab_conf["tools"]["pick_place"]["tool0_z_dist"].get()
    tool0_to_loc_z = (
        tool0_to_tool_z
        + fab_conf["robot_movement"]["offset_distance"].get()
        + bullet.height
    )
    expected_dist = tool0_to_loc_z - tool0_to_dist_sensor_z

    dist_diff = expected_dist - dist_read
    log.debug("Dist diff: {}".format(dist_diff))

    bullet.attrs["dist_diff"] = dist_diff

    # max_diff = 20
    # if abs(dist_diff) > max_diff:
    #     bullet.attrs["dist_diff_error"] = True
    #     log.debug("Skipped because dist diff too high")
    #     return 1

    bullet.location = get_offset_frame(bullet.location, dist_diff)

    top_bullet_frame = get_offset_frame(bullet.location, bullet.height)

    client.send_and_wait(WaitTime(2))

    client.send(
        MoveToFrame(
            top_bullet_frame,
            fab_conf["robot_movement"]["speed_placing"].get(),
            fab_conf["robot_movement"]["zone_place"].get(),
        )
    )

    client.Send(WaitTime(fab_conf["robot_movement"]["needles_pause"].get()))
    retract_needles(client)
    client.Send(WaitTime(fab_conf["robot_movement"]["needles_pause"].get()))

    client.send(
        MoveToFrame(
            bullet.placement_frame,
            fab_conf["robot_movement"]["speed_placing"].as_number(),
            fab_conf["robot_movement"]["zone_place"].get(ZoneDataTemplate()),
        )
    )

    client.send(
        MoveToFrame(
            offset_placement,
            fab_conf["robot_movement"]["speed_travel"].as_number(),
            fab_conf["robot_movement"]["zone_travel"].get(ZoneDataTemplate()),
        )
    )

    # offset placement frame then safety frame
    for frame in bullet.trajectory_from:
        client.send(
            MoveToFrame(
                frame,
                fab_conf["robot_movement"]["speed_travel"].as_number(),
                fab_conf["robot_movement"]["zone_travel"].get(ZoneDataTemplate()),
            )
        )

    client.send(StopWatch())

    return client.send(ReadWatch())


def retract_needles(client):
    pin = fab_conf["tools"]["pick_place"]["io_needles_pin"].get()
    state = fab_conf["tools"]["pick_place"]["retract_signal"].get()

    client.send(SetDigital(pin, state))

    log.debug("IO {} set to {}.".format(pin, state))


def extend_needles(client):
    pin = fab_conf["tools"]["pick_place"]["io_needles_pin"].get()
    state = fab_conf["tools"]["pick_place"]["extend_signal"].get()

    client.send(SetDigital(pin, state))

    log.debug("IO {} set to {}.".format(pin, state))
