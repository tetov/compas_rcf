from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Frame

from compas_rcf.utils.util_funcs import ensure_frame

try:
    from typing import List
except ImportError:
    pass


def format_joint_positions(joint_values):
    jpos_fmt = "[" + ", ".join(["{:.4f}"] * 6) + "]"
    return jpos_fmt.format(*joint_values)


def format_pose(frame_like):
    frame = ensure_frame(frame_like)

    pose_data = [c / 1000.0 for c in frame.origin.data] + frame.axis_angle_vector()
    pose_fmt = "p[" + ", ".join(["{:.4f}"] * 6) + "]"
    return pose_fmt.format(*pose_data)


def format_urscript_cmd(func):
    # @wraps(func)
    def wrapper(*arg, **kwargs):
        cmd = "\t{}\n".format(func(*arg, **kwargs))
        return cmd

    return wrapper


# Motion
@format_urscript_cmd
def movel(frame_to, accel=1.2, vel=0.25, time=0, zone=0):
    # type: (Frame, float, float, float, float) -> str
    pose = format_pose(frame_to)
    return "movel({:s}, a={:.2f}, v={:2f}, t={:2f} r={:2f})".format(
        pose, accel, vel, time, zone
    )


@format_urscript_cmd
def movej(joint_positions, accel=1.4, vel=1.05, time=0, zone=0):
    # type: (List[float], float, float, float, float) -> str
    """
    Function that returns UR script for linear movement in joint space.

    Args:
        joints: A list of 6 joint angles (double).
        accel: tool accel in m/s^2
        accel: tool accel in m/s^2
        vel: tool speed in m/s

    Returns:
        script: UR script
    """
    # TODO: Test
    # TODO: Check acceleration and velocity are below set limit
    _joint_positions = format_joint_positions(joint_positions)

    return "movej({:s}, a={:.2f}, v={:.2f}), t={:.2f}, r={:.2f}".format(
        _joint_positions, accel, vel, time, zone
    )


# Utility


@format_urscript_cmd
def set_TCP(tcp_frame):
    # type: (Frame) -> str
    pose = format_pose(tcp_frame)
    return "set_tcp({:s})".format(pose)


@format_urscript_cmd
def textmsg(string):
    # type: (str) -> str
    return 'textmsg("' + string + '")'


@format_urscript_cmd
def popup(string):
    # type: (str) -> str
    # Popup title not implemented, neither is error or warning flags
    return 'popup("{}")'.format(string)


@format_urscript_cmd
def sleep(seconds):
    # type: (float) -> str
    """
    Function that returns UR script for sleep()

    Args:
        time: float.in s

    Returns:
        script: UR script
    """
    return "sleep({})\n".format(seconds)


# Communication


@format_urscript_cmd
def socket_open(server_address, server_port):
    # type: (str, int) -> str
    return 'socket_open("{}", {:d})'.format(server_address, server_port)


@format_urscript_cmd
def socket_send_string(text):
    # type: (str) -> str
    return 'socket_send_string("' + text + '")'


@format_urscript_cmd
def socket_close():
    # type: () -> str
    return "socket_close()"


# IO


@format_urscript_cmd
def set_DO(pin, state):
    # type: (int, bool) -> str
    # deprecation warning in UR manual
    # return "set_digital_out({:d}, {})".format(pin, state)
    return set_standard_digital_out(pin, state)


@format_urscript_cmd
def set_standard_digital_out(pin, state):
    # type: (int, bool) -> str
    """Set standard digital output signal level

    Parameters
    ----------
    pin : int, 0 to 7
        Pin number
    state: bool

    Returns
    -------
    str
    """
    # TODO: Test
    return "set_standard_digital_out({}, {})".format(id, str(state))


@format_urscript_cmd
def set_standard_analog_out(pin, signal_level):
    # type: (int, float) -> str
    """Set standard analog output level

    Parameters
    ----------
    pin : int, 0 to 1
        Pin number
    signal_level : float, 0 to 1
        Relative signal level

    Returns
    -------
    str
    """
    # TODO: Test

    return "set_standard_analog_out({}, {:.3})".format(id, signal_level)
