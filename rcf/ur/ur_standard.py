"""
This module wraps standard UR Script functions.
Main change is that plane infromation substitute for pose data
"""

import ur_utils as utils
import Rhino.Geometry as rg

# ----- UR Interfaces module -----


def set_analog_out(id, signal):
    """
    Function that returns UR script for setting analog out

    Args:
        id: int. Input id number
        signal: int. signal level 1(on) or 0(off)

    Returns:
        script: UR script
    """

    # Format UR script
    script = "set_analog_out(%s,%s)\n" % (id, signal)
    return script


def set_digital_out(id, signal):
    """
    Function that returns UR script for setting digital out

    Args:
        id: int. Input id number
        signal: boolean. signal level - on or off

    Returns:
        script: UR script
    """

    # Format UR script
    script = "set_digital_out(%s,%s)\n" % (id, signal)
    return script


def socket_open(address, port):
    """
    Function that returns UR script for setting digital out
    TODO(Jason) - some form of erroe checking?

    Args:
        adress: string. IP address
        port: int. Port number

    Returns:
        script: UR script
    """

    script = "socket_open(%s,%s)\n" % (address, port)
    return script


def socket_send_string(ref_string):
    """
    Function that returns UR script for sending strings through a socket

    Args:
        ref_string: string. Either a string or name of variable defined in urscript

    Returns:
        script: UR script
    """

    script = "socket_send_string(%s)\n" % (ref_string)
    return script


# ----- UR Motion module -----

# Some Constants
MAX_ACCEL = 1.5
MAX_VELOCITY = 2


def _format_pose(plane_to, axis_angle):
    pose_data = (plane_to.OriginX / 1000, plane_to.OriginY / 1000, plane_to.OriginZ / 1000, axis_angle[0],
                 axis_angle[1], axis_angle[2])
    pose_fmt = "p[" + ",".join(["{:.4f}"] * 6) + "]"
    return pose_fmt.format(*pose_data)


def move_l(plane_to, accel, vel, blend_radius=0):
    """
    Function that returns UR script for linear movement in tool-space.

    Args:
        plane_to: Rhino.Geometry Plane. A target plane for calculating pose (in UR base coordinate system)
        accel: tool accel in m/s^2
        vel: tool speed in m/s

    Returns:
        script: UR script
    """

    # Check acceleration and velocity are non-negative and below a set limit
    accel = MAX_ACCEL if (abs(accel) > MAX_ACCEL) else abs(accel)
    vel = MAX_VELOCITY if (abs(vel) > MAX_VELOCITY) else abs(vel)
    # Check blend radius is positive
    blend_radius = max(0, blend_radius)

    matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, plane_to)
    axis_angle = utils.matrix_to_axis_angle(matrix)
    # Create pose data
    pose = _format_pose(plane_to, axis_angle)
    # Format UR script
    script = "movel(%s, a = %.2f, v = %.2f, r = %.4f)\n" % (pose, accel, vel, blend_radius)
    return script


def move_l_time(plane_to, time, blend_radius=0):
    """
    Function that returns UR script for linear movement in tool-space.

    Args:
        plane_to: Rhino.Geometry Plane. A target plane for calculating pose (in UR base coordinate system)
        time: Amount of time the movement shoud take, in seconds. Overrides speed and acceleration.

    Returns:
        script: UR script
    """
    # Check time is positive
    time = abs(time)
    # Check blend radius is positive
    blend_radius = max(0, blend_radius)

    matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, plane_to)
    axis_angle = utils.matrix_to_axis_angle(matrix)
    # Create pose data
    pose = _format_pose(plane_to, axis_angle)
    # Format UR script
    script = "movel(%s, a = %.2f, v = %.2f, t = %.2f, r = %.4f)\n" % (pose, 1.2, 0.25, time, blend_radius)
    return script


def move_l2(plane_to, vel, blend_radius):

    matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, plane_to)
    axis_angle = utils.matrix_to_axis_angle(matrix)
    # Create pose data
    pose = _format_pose(plane_to, axis_angle)
    # Format UR script
    script = "movel(%s, v = %.4f, r= %.4f)\n" % (pose, vel, blend_radius)
    return script


def move_j(joints, accel, vel):
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
    # Check acceleration and velocity are non-negative and below a set limit

    _j_fmt = "[" + ("%.4f," * 6)[:-1] + "]"
    _j_fmt = _j_fmt % tuple(joints)
    script = "movej(%s, a = %.2f, v = %.2f)\n" % (_j_fmt, accel, vel)
    return script


def move_j_pose(plane_to, accel, vel, blend_radius=0.):

    matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, plane_to)
    axis_angle = utils.matrix_to_axis_angle(matrix)
    # Create pose data
    pose = _format_pose(plane_to, axis_angle)
    # Format UR script
    script = "movej(%s, a=%.4f, v = %.4f, r=%.4f)\n" % (pose, accel, vel, blend_radius)
    return script


def move_c(plane_to, point_via, accel, vel):
    """
    Function that returns UR script for circular movement in tool-space. Only via planes, joint angles not wrapped

    Args:
        plane_to:  Rhino.Geometry Plane.A target plane used for calculating pose (in UR base coordinate system)
        point_via: Rhino.Geometry Point. A waypoint that movement passes through
        accel: tool accel in m/s^2
        vel: tool speed in m/s

    Returns:
        script: UR script
    """

    # Check acceleration and velocity are non-negative and below a set limit
    accel = MAX_ACCEL if (abs(accel) > MAX_ACCEL) else abs(accel)
    vel = MAX_VELOCITY if (abs(vel) > MAX_VELOCITY) else abs(vel)

    _matrix = rg.Transform.PlaneToPlane(plane_to, rg.Plane.WorldXY)
    _axis_angle = utils.matrix_to_axis_angle(_matrix)
    # Create pose data
    _pose_to = [
        plane_to.OriginX / 1000, plane_to.OriginY / 1000, plane_to.OriginZ / 1000, _axis_angle[0], _axis_angle[1],
        _axis_angle[2]
    ]
    _pose_via = [
        point_via.X / 1000, point_via.Y / 1000, point_via.Z / 1000, _axis_angle[0], _axis_angle[1], _axis_angle[2]
    ]

    _pose_fmt = "p[" + ("%.4f," * 6)[:-1] + "]"
    _pose_to_fmt = _pose_fmt % tuple(_pose_to)
    _pose_via_fmt = _pose_fmt % tuple(_pose_via)
    # Format UR script
    script = "movec(%s, %s, a = %.2f, v = %.2f)\n" % (_pose_via_fmt, _pose_to_fmt, accel, vel)
    return script


# ----- UR Internals module -----


def set_tcp_by_plane(x_offset, y_offset, z_offset, ref_plane=rg.Plane.WorldXY):
    """
    TODO: Need to test if this gives the correct result
    Function that returns UR script for setting tool center point

    Args:
        x_offset: float. tooltip offset in mm
        y_offset: float. tooltip offset in mm
        z_offset: float. tooltip offset in mm
        ref_plane: Plane that defines orientation of the tip. If none specified, world XY plane used as default. (in UR base coordinate system)

    Returns:
        script: UR script
    """

    if (ref_plane != rg.Plane.WorldXY):
        _matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, ref_plane)
        _axis_angle = utils.matrix_to_axis_angle(_matrix)
    else:
        _axis_angle = rg.Vector3d(0, 0, 0)
    # Create pose data
    _pose = [x_offset / 1000, y_offset / 1000, z_offset / 1000, _axis_angle[0], _axis_angle[1], _axis_angle[2]]
    _pose_fmt = "p[" + ("%.4f," * 6)[:-1] + "]"
    _pose_fmt = _pose_fmt % tuple(_pose)

    # Format UR script
    script = "set_tcp(%s)\n" % (_pose_fmt)
    return script


def set_tcp_by_angles(x_offset, y_offset, z_offset, x_rotate, y_rotate, z_rotate):
    """
    TODO(Jason): Need to test this
    Function that returns UR script for setting tool center point

    Args:
        x_offset: float. tooltip offset in mm
        y_offset: float. tooltip offset in mm
        z_offset: float. tooltip offset in mm
        x_rotation: float. rotation around world x axis in radians
        y_rotation: float. rotation around world y axis in radians
        z_rotation: float. rotation around world z axis in radians

    Returns:
        script: UR script
    """

    # Create rotation matrix
    _rX = rg.Transform.Rotation(x_rotate, rg.Vector3d(1, 0, 0), rg.Point3d(0, 0, 0))
    _rY = rg.Transform.Rotation(y_rotate, rg.Vector3d(0, 1, 0), rg.Point3d(0, 0, 0))
    _rZ = rg.Transform.Rotation(z_rotate, rg.Vector3d(0, 0, 1), rg.Point3d(0, 0, 0))
    _r = _rX * _rY * _rZ
    _axis_angle = utils.matrix_to_axis_angle(_r)

    # Create pose data
    _pose = [x_offset / 1000, y_offset / 1000, z_offset / 1000, _axis_angle[0], _axis_angle[1], _axis_angle[2]]
    _pose_fmt = "p[" + ("%.4f," * 6)[:-1] + "]"
    _pose_fmt = _pose_fmt % tuple(_pose)

    # Format UR script
    script = "set_tcp(%s)\n" % (_pose_fmt)
    return script


def popup(message, title):
    """
    Function that returns UR script for popup

    Args:
        message: float. tooltip offset in mm
        title: float. tooltip offset in mm

    Returns:
        script: UR script
    """
    script = 'popup("%s","%s") \n' % (message, title)
    return script


def UR_log(message):
    return 'textmsg(\"{}\")\n'.format(message)


def sleep(time):
    """
    Function that returns UR script for sleep()

    Args:
        time: float.in s

    Returns:
        script: UR script
    """
    script = "sleep(%s) \n" % (time)
    return script


def get_forward_kin(var_name):
    """
    Function that returns UR script for get_forward_kin(). Transformation from joint space to tool space.

    Args:
        var_name: String. name of variable to store forward kinematics information

    Returns:
        script: UR script
    """
    script = "%s = get_forward_kin()\n" % (var_name)
    return script


def get_inverse_kin(var_name, ref_plane):
    """
    Function that returns UR script for get_forward_kin(). Transformation from joint space to tool space.

    Args:
        var_name: String. name of variable to store inverse kinematics information
        ref_plane: Rhino.Geometry Plane. A target plane for calculating pose

    Returns:
        script: UR script
    """

    _matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, ref_plane)
    _axis_angle = utils.matrix_to_axis_angle(_matrix)
    # Create pose data
    _pose = [
        plane_to.OriginX / 1000, plane_to.OriginY / 1000, plane_to.OriginZ / 1000, _axis_angle[0], _axis_angle[1],
        _axis_angle[2]
    ]
    _pose_fmt = "p[" + ("%.4f," * 6)[:-1] + "]"
    _pose_fmt = _pose_fmt % tuple(_pose)
    # Format UR script
    script = "%s = get_inverse_kin()\n" % (var_name, _pose_fmt)
    return script


def get_joint_positions(var_name):
    """
    Function that returns UR script for get_inverse_kin(). Transformation from tool space to joint space.

    Args:
        var_name: String. name of variable to store inverse kinematics information
    Returns:
        script: UR script
    """
    script = "%s = get_joint_positions()\n" % (var_name)
    return script
