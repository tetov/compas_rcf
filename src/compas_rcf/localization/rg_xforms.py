"""Transformation functions for localization using Rhino and rhinoscriptsyntax.

Code adapted from source code by Selen Ercan et al at Gramazio Kohler Research,
ETH Zurich (2019).

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

import Rhino.Geometry as rg
import rhinoscriptsyntax as rs


def rcs_to_wcs(rcs):
    """Calculate the transformation matrix from the robot coordinate system.

    Parameters
    ----------
    rcs
        A list with three points: [origin, x, y] where origin is the origin of
        the rcs given in the wcs and x and y are vectors representing the x and
        y axis of the rcs in the wcs.

    Returns
    -------
    :class:`Rhino.Geometry.Transform`
        The transformation from the WCS to the RCS.
    """
    origin, x_vec, y_vec = rcs
    z_vec = rs.VectorUnitize(rs.VectorCrossProduct(x_vec, y_vec))

    translation = rs.XformTranslation(origin)
    rotation = rs.XformRotation4(
        rg.Point3d(1, 0, 0),
        rg.Point3d(0, 1, 0),
        rg.Point3d(0, 0, 1),
        x_vec,
        y_vec,
        z_vec,
    )

    print("---- Calculated translation ----")
    print(translation)
    print("----- Calculated rotation ----")
    print(rotation)

    transform = rs.XformInverse(translation * rotation)
    return transform
