"""
This module contains utility functions:
    1) Transformation functions
    2) Useful geometry functions e.g. Intersections
"""

from __future__ import absolute_import, division, print_function

import re

import Rhino.Geometry as rg
from compas.geometry import Frame, Point, Rotation, Transformation
from compas_fab.robots.configuration import Configuration
from compas_fab.robots.ur5 import Robot
from compas_rcf.utils import cgframe_to_rgplane, matrix_to_rgtransform

# ----- Coordinate System conversions -----


def rhino_to_robotbase(ref_plane, model_base):
    """
    Function that transforms a reference plane from Rhino coordinate system to
    the robot's base coordinate system
    TODO (Jason): maybe change this whole method? maybe not model but robot base

    Args:
        ref_plane: Rhino.Geometry plane object. The reference plane to transform
        model_base: Rhino.Geometry plane object. The base plane for building on.
        Given in robot's base coordinate system.

    Returns:
        ref_plane: Reference plane transformed to robot space
    """
    # TODO: Replace with compas method

    # Transform the orientation plane based on model_base coordinate system
    _matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY, model_base)
    # _matrix = rg.Transform.PlaneToPlane(model_base,rg.Plane.WorldXY,)
    ref_plane.Transform(_matrix)
    return ref_plane


def visualize_ur_script(script):
    M = [[-1000,    0,    0,    0], # noqa E201
         [    0, 1000,    0,    0], # noqa E201
         [    0,    0, 1000,    0], # noqa E201
         [    0,    0,    0,    1]] # noqa E201 # yapf: disable
    rgT = matrix_to_rgtransform(M)
    cgT = Transformation.from_matrix(M)

    robot = Robot()

    viz_planes = []

    movel_matcher = re.compile(r'^\s*move([lj]).+((-?\d+\.\d+,?\s?){6}).*$')
    for line in script.splitlines():
        mo = re.search(movel_matcher, line)
        if mo:
            if mo.group(1) == 'l':  # movel
                ptX, ptY, ptZ, rX, rY, rZ = mo.group(2).split(',')

                pt = Point(float(ptX), float(ptY), float(ptZ))
                pt.transform(cgT)
                frame = Frame(pt, [1, 0, 0], [0, 1, 0])

                R = Rotation.from_axis_angle_vector([float(rX), float(rY), float(rZ)], pt)
                T = matrix_to_rgtransform(R)

                plane = cgframe_to_rgplane(frame)
                plane.Transform(T)

                viz_planes.append(plane)
            else:  # movej
                joint_values = mo.group(2).split(',')
                configuration = Configuration.from_revolute_values([float(d) for d in joint_values])
                frame = robot.forward_kinematics(configuration)

                plane = cgframe_to_rgplane(frame)
                plane.Transform(rgT)

                viz_planes.append(plane)

    return viz_planes
