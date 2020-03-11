"""Helpers for scripts interacting with ABB robots or RAPID code."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import math

from compas import IPY
from compas.geometry import Frame

from compas_rcf.utils.util_funcs import ensure_frame

if IPY:
    from compas_rcf.rhino import cgframe_to_rgplane


log = logging.getLogger(__name__)


class RapidToolData(object):
    """Create Rapid ToolData.

    Parameters
    ----------
    tcp_coord : list of floats
        Coordinate of tool center point
    tcp_quaternion : list of floats
        Rotation of tool center plane in quaternions
    cog_coord : list of floats, optional
        Coordinates of center of gravity of tool
    name : str, optional
    weight : float, optional
        Tool weight in kg

    Note
    ----
    Axes of moment and inertia not implemented
    """

    RAPID_TOOLDATA_FORMAT = (
        "TASK PERS tooldata {}"
        + ":=[TRUE,[[{},{},{}],[{},{},{},{}]],"
        + "[{},[{},{},{}],[1,0,0,0],0,0,0]];"
    )

    def __init__(
        self,
        tcp_coord,
        tcp_quaternion,
        cog_coord=[0, 0, 100],
        name="tool",
        weight=5.0,
        tolerance=1e-6,
    ):
        self.tcp_coord = tcp_coord
        self.tcp_quaternion = tcp_quaternion
        self.cog_coord = cog_coord
        self.name = name
        self.weight = weight
        self.tolerance = tolerance

    def __repr__(self):
        return self.get_rapid_tooldata()

    @property
    def tcp_frame(self):
        return Frame.from_quaternion(self.tcp_quaternion, point=self.tcp_coord)

    @property
    def tcp_plane(self):
        return cgframe_to_rgplane(self.tcp_frame)

    @classmethod
    def from_frame_point(cls, tcp_frame, cog_pt=None, **kwargs):
        """Create RapidToolData object from :class:`compas.Geometry.Primitive` objects.

        Parameters
        ----------
        tcp_frame : :class:`compas.geometry.Frame`
            Frame at tool center plane.
        cog_pt : :class:`compas.geometry.Point`, optional
            Point at tool center of gravity.
        name : str, optional
        weight : float, optional
            Tool weight in kg

        Returns
        -------
        :class:`RapidToolData`

        """
        tcp_coord = tcp_frame.point.data
        tcp_quaternion = tcp_frame.quaternion.wxyz

        if cog_pt:
            kwargs.update({"cog_coord": cog_pt.data})

        return cls(tcp_coord, tcp_quaternion, **kwargs)

    @classmethod
    def from_plane_point(cls, tcp_plane, cog_pt=None, **kwargs):
        """Create RapidToolData object from :class:`Rhino.Geometry.GeometryBase` objects.

        Parameters
        ----------
        tcp_plane : :class:`Rhino.Geometry.Plane`
            Plane at tool center plane.
        cog_pt : :class:`Rhino.Geometry.Point3d`, optional
            Point at tool center of gravity.
        name : str, optional
        weight : float, optional
            Tool weight in kg

        Returns
        -------
        :class:`RapidToolData`

        """
        tcp_coord = [tcp_plane.Origin.X, tcp_plane.Origin.Y, tcp_plane.Origin.Z]

        tcp_frame = ensure_frame(tcp_plane)
        tcp_quaternion = tcp_frame.quaternion.wxyz

        if cog_pt:
            cog_coord = [cog_pt.X, cog_pt.Y, cog_pt.Z]
            kwargs.update({"cog_coord": cog_coord})

        return cls(tcp_coord, tcp_quaternion, **kwargs)

    def get_rapid_tooldata(self):
        """Generate Rapid tooldata.

        Returns
        -------
        str
        """
        data = self.tcp_coord + self.tcp_quaternion + [self.weight] + self.cog_coord
        formatted_data = [self._float_str(x) for x in data]

        return self.RAPID_TOOLDATA_FORMAT.format(self.name, *formatted_data)

    def _float_str(self, n):
        """Format float as string with given tolerance.

        Arguments
        ---------
        n : float or int
            Number to format


        Returns
        -------
        str
        """
        # Get tolerance as number of decimals
        tol = -1 * math.floor(math.log(self.tolerance, 10))

        return "{:.{tol}f}".format(float(n), tol=int(tol))
