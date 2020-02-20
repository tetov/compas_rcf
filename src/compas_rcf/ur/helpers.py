from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas.geometry as cg
import Rhino.Geometry as rg

from compas_rcf.ur.urscript_wrapper import set_DO
from compas_rcf.ur.urscript_wrapper import set_standard_analog_out
from compas_rcf.ur.urscript_wrapper import textmsg
from compas_rcf.utils.rhino_to_compas import rgtransform_to_matrix

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


def axis_angle_vector_from_plane_to_plane(plane_to, plane_from=rg.Plane.WorldXY):
    T = rg.Transform.PlaneToPlane(plane_from, plane_to)
    M = rgtransform_to_matrix(T)
    return cg.axis_angle_vector_from_matrix(M)
