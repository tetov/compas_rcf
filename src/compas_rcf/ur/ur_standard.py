"""Will be replaced by urscript_wrapper.

This module wraps standard UR Script functions.
Main change is that plane information substitute for pose data
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas.geometry as cg
import Rhino.Geometry as rg
from compas.geometry.transformations import axis_angle_vector_from_matrix

from compas_rcf.utils.rhino_to_compas import rgtransform_to_matrix


# Import this from helpers when I've solved problem with format_ur_cmd
def axis_angle_vector_from_plane_to_plane(plane_to, plane_from=rg.Plane.WorldXY):
    T = rg.Transform.PlaneToPlane(plane_from, plane_to)
    M = rgtransform_to_matrix(T)
    return cg.axis_angle_vector_from_matrix(M)


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
    return "set_analog_out({:d}, {})\n".format(id, signal)


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
    return "set_digital_out({:d}, {})\n".format(id, signal)


def socket_open(address, port):
    """
    Function that returns UR script for setting digital out
    TODO(Jason) - some form of error checking?

    Args:
        address: string. IP address
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


def _format_pose(pt_like, axis_angle):

    if isinstance(pt_like, (list, tuple)):
        pt_coords = [float(c) for c in pt_like]
        if len(pt_coords) < 3:
            for i in range(3 - len(pt_coords)):
                pt_coords += [0]
            # pt_coords += [0.] * (3 - len(pt_coords))
    elif isinstance(pt_like, rg.Point3d):
        pt_coords = [pt_like.X, pt_like.Y, pt_like.Z]
    elif isinstance(pt_like, cg.Point):
        pt_coords = pt_like.data
    elif isinstance(pt_like, rg.Plane):
        pt_coords = [pt_like.OriginX, pt_like.OriginY, pt_like.OriginZ]
    elif isinstance(pt_like, cg.Frame):
        pt_coords = pt_like.point.data
    else:
        raise TypeError("Could not convert argument to point")
    pose_data = [c / 1000.0 for c in pt_coords] + [float(a) for a in axis_angle]
    pose_fmt = "p[" + ", ".join(["{:.4f}"] * 6) + "]"
    return pose_fmt.format(*pose_data)


def _format_joint_positions(joint_values):
    jpos_fmt = "[" + ", ".join(["{:.4f}"] * 6) + "]"
    return jpos_fmt.format(*joint_values)


def move_l(plane_to, accel, vel, blend_radius=0):
    """
    Function that returns UR script for linear movement in tool-space.

    Args:
        plane_to: Rhino.Geometry Plane. A target plane for calculating pose
            (in UR base coordinate system)
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

    axis_angle_vector = axis_angle_vector_from_plane_to_plane(plane_to)

    # Create pose data
    pose = _format_pose(plane_to, axis_angle_vector)

    # Format UR script
    return "movel(%s, a = %.2f, v = %.2f, r = %.2f)\n" % (
        pose,
        accel,
        vel,
        blend_radius,
    )


def move_l_time(plane_to, time, blend_radius=0):
    """
    Function that returns UR script for linear movement in tool-space.

    Args:
        plane_to: Rhino.Geometry Plane. A target plane for calculating pose
            (in UR base coordinate system)
        time: Amount of time the movement should take, in seconds.
            Overrides speed and acceleration.

    Returns:
        script: UR script
    """
    # Check time is positive
    time = abs(time)
    # Check blend radius is positive
    blend_radius = max(0, blend_radius)

    axis_angle_vector = axis_angle_vector_from_plane_to_plane(plane_to)

    # Create pose data
    pose = _format_pose(plane_to, axis_angle_vector)

    # Format UR script
    return "movel(%s, a = %.2f, v = %.2f, t = %.2f, r = %.4f)\n" % (
        pose,
        1.2,
        0.25,
        time,
        blend_radius,
    )


def move_l2(plane_to, vel, blend_radius):
    # TODO: Test

    axis_angle_vector = axis_angle_vector_from_plane_to_plane(plane_to)

    # Create pose data
    pose = _format_pose(plane_to, axis_angle_vector)

    # Format UR script
    return "movel(%s, v = %.4f, r= %.4f)\n" % (pose, vel, blend_radius)


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
    # TODO: Test
    # TODO: Check acceleration and velocity are below set limit
    joint_positions = _format_joint_positions(joints)

    return "movej({}, a = {:.2f}, v = {:.2f})\n".format(
        joint_positions, abs(accel), abs(vel)
    )


def move_j_pose(plane_to, accel, vel, blend_radius=0.0):
    axis_angle_vector = axis_angle_vector_from_plane_to_plane(plane_to)

    # Create pose data
    pose = _format_pose(plane_to, axis_angle_vector)

    # Return UR script
    return "movej({}, a = {:.2f}, v = {:.2f}, r = {:.2f})\n".format(
        pose, accel, vel, blend_radius
    )


def move_c(plane_to, point_via, accel, vel):
    """
    Function that returns UR script for circular movement in tool-space.

    Only via planes, joint angles not wrapped

    Args:
        plane_to:  Rhino.Geometry Plane.A target plane used for calculating pose
            (in UR base coordinate system)
        point_via: Rhino.Geometry Point. A waypoint that movement passes through
        accel: tool accel in m/s^2
        vel: tool speed in m/s

    Returns:
        script: UR script
    """
    # TODO: Test
    # Check acceleration and velocity are non-negative and below a set limit
    accel = MAX_ACCEL if (abs(accel) > MAX_ACCEL) else abs(accel)
    vel = MAX_VELOCITY if (abs(vel) > MAX_VELOCITY) else abs(vel)

    axis_angle_vector = axis_angle_vector_from_plane_to_plane(plane_to)

    # Create pose data
    pose_to = _format_pose(plane_to, axis_angle_vector)
    pose_via = _format_pose(point_via, axis_angle_vector)

    # Format UR script
    return "movec({}, {}, a = {:.2f}, v = {:.2f})\n".format(
        pose_to, pose_via, accel, vel
    )


# ----- UR Internals module -----


def set_tcp_by_plane(x_offset, y_offset, z_offset, ref_plane=rg.Plane.WorldXY):
    """
    Function that returns UR script for setting tool center point

    Args:
        x_offset: float. tooltip offset in mm
        y_offset: float. tooltip offset in mm
        z_offset: float. tooltip offset in mm
        ref_plane: Plane that defines orientation of the tip. If none specified,
        world XY plane used as default. (in UR base coordinate system)

    Returns:
        script: UR script
    """
    # TODO: Test

    axis_angle_vector = axis_angle_vector_from_plane_to_plane(
        rg.Plane.WorldXY, plane_from=ref_plane
    )

    # Create pose data
    pose = _format_pose([x_offset, y_offset, z_offset, axis_angle_vector])

    # Return UR script
    return "set_tcp({})\n".format(pose)


def set_tcp_by_plane_angles(x_offset, y_offset, z_offset, x_rotate, y_rotate, z_rotate):
    """
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
    rX = rg.Transform.Rotation(x_rotate, rg.Vector3d(1, 0, 0), rg.Point3d(0, 0, 0))
    rY = rg.Transform.Rotation(y_rotate, rg.Vector3d(0, 1, 0), rg.Point3d(0, 0, 0))
    rZ = rg.Transform.Rotation(z_rotate, rg.Vector3d(0, 0, 1), rg.Point3d(0, 0, 0))
    R = rX * rY * rZ
    M = rgtransform_to_matrix(R)
    axis_angle_vector = axis_angle_vector_from_matrix(M)

    # Create pose data
    pose = _format_pose([x_offset, y_offset, z_offset], axis_angle_vector)

    # Format UR script
    return "set_tcp({})\n".format(pose)


def popup(message, title):
    """
    Function that returns UR script for popup

    Args:
        message: float. tooltip offset in mm
        title: float. tooltip offset in mm

    Returns:
        script: UR script
    """
    return 'popup("{}","{}") \n'.format(message, title)


def UR_log(message):
    return 'textmsg("{}")\n'.format(message)


def sleep(time):
    """
    Function that returns UR script for sleep()

    Args:
        time: float.in s

    Returns:
        script: UR script
    """
    return "sleep({})\n".format(time)


def get_forward_kin(var_name):
    """
    Function that returns UR script for get_forward_kin().

    Transformation from joint space to tool space.

    Args:
        var_name: String. name of variable to store forward kinematics information

    Returns:
        script: UR script
    """
    return "%s = get_forward_kin()\n" % (var_name)


def get_inverse_kin(var_name, ref_plane):
    """
    Function that returns UR script for get_forward_kin().

    Transformation from joint space to tool space.

    Args:
        var_name: String. name of variable to store inverse kinematics information
        ref_plane: Rhino.Geometry Plane. A target plane for calculating pose

    Returns:
        script: UR script
    """
    # TODO: Test

    axis_angle_vector = axis_angle_vector_from_plane_to_plane(ref_plane)

    # Create pose data
    pose = _format_pose(ref_plane, axis_angle_vector)

    # Return UR script
    return "{} = get_inverse_kin({})\n".format(var_name, pose)


def get_joint_positions(var_name):
    """
    Function that returns UR script for get_inverse_kin().
    Transformation from tool space to joint space.

    Args:
        var_name: String. name of variable to store inverse kinematics information
    Returns:
        script: UR script
    """
    # TODO: Test

    return "{} = get_joint_positions()\n".format(var_name)
