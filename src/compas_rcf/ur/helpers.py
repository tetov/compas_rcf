from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas.geometry as cg
import Rhino.Geometry as rg

from compas_rcf.ur.urscript_wrapper import set_DO
from compas_rcf.ur.urscript_wrapper import set_standard_analog_out
from compas_rcf.ur.urscript_wrapper import textmsg
from compas_rcf.utils.rhino_to_compas import rgplane_to_cgframe

# Programs


def turn_off_outputs_program():
    script = ""
    script += "def program():\n"
    script += textmsg("Turning of all DOs and AOs.")
    for i in range(7):
        script += set_DO(i, False)
    for i in range(1):
        script += set_standard_analog_out(i, 0)
    script += "end\n"
    script += "program()\n"
    return script


# Geometry

""" Bug in Grasshopper when importing this, "Cannot import name format_urscript_cmd"
    Moved to ur_standard temporarily
def axis_angle_vector_from_plane_to_plane(plane_to, plane_from=rg.Plane.WorldXY):
    T = rg.Transform.PlaneToPlane(plane_from, plane_to)
    M = rgtransform_to_matrix(T)
    return cg.axis_angle_vector_from_matrix(M)
"""


# UR script helpers


def format_joint_positions(joint_values):
    jpos_fmt = "[" + ", ".join(["{:.4f}"] * 6) + "]"
    return jpos_fmt.format(*joint_values)


def format_pose(frame_like):
    if isinstance(frame_like, rg.Plane):
        frame = rgplane_to_cgframe(frame_like)
    elif isinstance(frame_like, cg.Frame):
        frame = frame_like
    else:
        raise TypeError

    pose_data = [c / 1000. for c in frame.origin.data] + frame.axis_angle_vector()
    pose_fmt = "p[" + ", ".join(["{:.4f}"] * 6) + "]"
    return pose_fmt.format(*pose_data)


def format_urscript_cmd(func):
    # @wraps(func)
    def wrapper(*arg, **kwargs):
        cmd = "\t{}\n".format(func(*arg, **kwargs))
        return cmd
    return wrapper
