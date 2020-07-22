"""Three points method for robot relocalization.

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
import compas.geometry as cg

compas.PRECISION = "12f"


def three_point_localization(rcs_coords, wcs_coords):
    """Get the robot base frame in WCS using three points method.

    Parameters
    ----------
    rcs_coords : :obj:`list` of :class:`compas.geometry.Point`
        List of the RCS coordinates used for measurements.
    wcs_coords : :obj:`list` of :class:`compas.geometry.Point`
        List of the WCS coordinates used for measurements.

    Returns
    -------
    :class:`compas.geometry.Frame`
        The base frame of the robot in WCS.
    """
    # Calculate the directions of the X, Y and X axis of the robot in WCS
    rcs_o, rcs_x, rcs_y = rcs_coords
    wcs_o, wcs_x, wcs_y = wcs_coords

    wcs_robot_x_dir = wcs_x - wcs_o
    wcs_robot_y_dir = wcs_y - wcs_o
    wcs_robot_z_dir = wcs_robot_x_dir.cross(wcs_robot_y_dir)

    wcs_robot_x_dir.unitize()
    wcs_robot_y_dir.unitize()
    wcs_robot_z_dir.unitize()

    x_dist = wcs_robot_x_dir * rcs_o.x
    y_dist = wcs_robot_y_dir * rcs_o.y
    z_dist = wcs_robot_z_dir * rcs_o.z

    wcs_robot_base_origin = wcs_o - x_dist - y_dist - z_dist
    wcs_robot_base = cg.Frame(wcs_robot_base_origin, wcs_robot_x_dir, wcs_robot_y_dir)

    print("---- Localization points ----")
    print("RCS_o: {}".format(rcs_o))
    print("RCS_x: {}".format(rcs_x))
    print("RCS_y: {}".format(rcs_y))

    print("---- Measured points ----")
    print("WCS_o: {}".format(wcs_o))
    print("WCS_x: {}".format(wcs_x))
    print("WCS_y: {}".format(wcs_y))

    print("Robot X Direction in WCS: {}".format(wcs_robot_base.xaxis))
    print("Robot Y Direction in WCS: {}".format(wcs_robot_base.yaxis))
    print("Robot Z Direction in WCS: {}".format(wcs_robot_base.zaxis))

    print("RCS origin in WCS: {}".format(wcs_robot_base.point))

    return wcs_robot_base
