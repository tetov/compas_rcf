"""Transformation functions for localization using Rhino and rhinoscriptsyntax.

Code adapted from source code by Selen Ercan and Sandro Meier at Gramazio
Kohler Research, ETH Zurich (2019).

Original code:
https://github.com/gramaziokohler/IF_jamming/blob/master/if_jamming/localization/transform.py

Ercan, Selen, Sandro Meier, Fabio Gramazio, and Matthias Kohler. 2019.
"Automated Localization of a Mobile Construction Robot with an External
Measurement Device." In Proceedings of the 36th International Symposium on
Automation and Robotics in Construction (ISARC 2019), 929-36. International
Association on Automation and Robotics in Construction.
https://doi.org/10.3929/ethz-b-000328442.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas
from compas.geometry import Rotation
from compas.geometry import Transformation
from compas.geometry import Translation
from compas.geometry import quaternion_from_matrix
from compas.geometry import translation_from_matrix


def rcs_to_wcs_xform(robot_base_frame):
    """Calculate the transformation matrix for transformations between WCS to RCS.

    Parameters
    ----------
    robot_base_frame : :class:`compas.geometry.Frame`
        Robot base frame in WCS. The frame origin is the location of the RCS origo
        in WCS, the X axis and Y axis are the X and Y axes of the RCS in WCS.

    Returns
    -------
    :obj:`list` of :obj:`list` of :obj:`float`
        The transformation matrix.
    """
    old_prec = compas.PRECISION
    compas.PRECISION = "12f"

    # TODO: Replace with xform from frame?
    translation = Translation(robot_base_frame.point)
    rotation = Rotation.from_basis_vectors(
        robot_base_frame.xaxis, robot_base_frame.yaxis
    )

    print("---- Calculated translation ----")
    print(translation)
    print("----- Calculated rotation ----")
    print(rotation)

    transform = translation * rotation
    transform.invert()

    print("---- Calculated transformation ----")
    print(transform)

    compas.PRECISION = old_prec

    return transform


def xform_to_xyz_quaternion(xform):
    """Convert transformation to :obj:`list` of coords and quaternion values.

    Parameters
    ----------
    xform
        Transformation to be converted. Can be given as
        :class:`Rhino.Geometry.Transform`, :class:`compas.geometry.Transformation`
        or :obj:`list` of :obj:`list` of :obj:`float`.

    Returns
    -------
    :obj:`list` of :float:`float`
        X, Y, Z, QW, QX, QY, QZ values as a list.

    >>> from compas.geometry import Frame, Rotation, Translation
    >>> Tr = Translation([100, 100, 100])
    >>> R = Rotation.from_frame(Frame.worldYZ())
    >>> T = Tr * R
    >>> xform_to_xyz_quaternion(T)
    [100.0, 100.0, 100.0, 0.5, 0.5, 0.5, 0.5]
    """
    old_prec = compas.PRECISION
    compas.PRECISION = "12f"

    M = _get_matrix(xform)
    xyzwxyz = _matrix_to_xyz_quaternion(M)

    compas.PRECISION = old_prec

    return xyzwxyz


def _get_matrix(xform):

    try:
        from Rhino.Geometry import Transform

        from compas_rcf.rhino import rgtransform_to_matrix
    except ImportError:
        pass
    else:
        if isinstance(xform, Transform):
            return rgtransform_to_matrix(xform)

    if isinstance(xform, Transformation):
        return xform.matrix

    # TODO: Maybe add np array?

    # TODO: Maybe check that it actually is list of list of float
    return xform


def _matrix_to_xyz_quaternion(M):
    xyz = translation_from_matrix(M)
    quaternion = quaternion_from_matrix(M)

    return xyz + quaternion
