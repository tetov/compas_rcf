"""Standalone move to frame function using compas_rrc."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_fab.backends import RosClient
from compas_rrc import AbbClient
from compas_rrc import Motion
from compas_rrc import MoveToFrame
from compas_rrc import Noop
from compas_rrc import PrintText
from compas_rrc import SetAcceleration
from compas_rrc import SetMaxSpeed
from compas_rrc import SetTool
from compas_rrc import SetWorkObject
from compas_rrc import Zone

try:
    from collections.abc import Sequence
except ImportError:
    from collections import Sequence


def standalone_move_to_frame(
    frame,
    tool="tool0",
    wobj="wobj0",
    motion_type=Motion.LINEAR,
    speed=200,
    accel=100,
    zone=Zone.FINE,
    timeout=None,
):
    """Move robot arm to frame or frames in one single function.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame` or :obj:`list` of :class:`compas.geometry.Frame`
        Target frame or frames.
    tool : :obj:`str`
        Name of tool as named in RAPID code on controller to use for TCP data.
    wobj : :obj:`str`
        Name of work object as named in RAPID code on controller to use for
        coordinate system.
    motion_type : :class:`compas_rrc.Motion`
        Motion type, either linear (:class:`~compas_rrc.Motion.LINEAR`) or
        joint (:class:`~compas_rrc.Motion.JOINT`).
    speed : :obj:`float`
        TCP speed in mm/s. Limited by hard coded max speed in this function as
        well as safety systems on controller.
    accel : :obj:`float`
        Acceleration in percentage of standard acceleration.
    zone : :class:`compas_rrc.Zone`
        Set zone value of movement, (acceptable deviation from target).
    timeout : :obj:`float`
        Time to wait for indication of finished movement. If not defined no
        feedback will be requested.
    """  # noqa: E501
    if not isinstance(frame, Sequence):
        frames = [frame]
    else:
        frames = frame

    with RosClient() as ros:
        # Create ABB Client
        abb = AbbClient(ros)
        abb.run(timeout=5)

        abb.send(SetTool(tool))
        abb.send(SetWorkObject(wobj))

        # Set acceleration data
        ramp = 100  # % Higher values makes the acceleration ramp longer
        abb.send(SetAcceleration(accel, ramp))

        # Set speed override and max speed
        speed_override = 100  # %
        max_tcp_speed = 500  # mm/s
        abb.send(SetMaxSpeed(speed_override, max_tcp_speed))

        # Move to Frame
        for f in frames:
            abb.send(
                PrintText(" Moving to {:.3f}, {:.3f}, {:.3f}.".format(*f.point.data))
            )
            abb.send(MoveToFrame(f, speed, zone, motion_type))

        if timeout:
            abb.send_and_wait(Noop(), timeout=timeout)
