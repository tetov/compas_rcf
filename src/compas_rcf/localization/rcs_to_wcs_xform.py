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

import compas.geometry as cg
import compas

compas.PRECISION = "12f"


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
    translation = cg.Translation(robot_base_frame.point)
    rotation = cg.Rotation.from_basis_vectors(
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

    return transform
