from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math

from compas.geometry import Frame

from rapid_clay_formations_fab.utils import ensure_frame


class RapidToolData(object):
    """Create Rapid ToolData.

    Parameters
    ----------
    tcp_coord : :class:`list` of class:`float`
        Coordinate of tool center point.
    tcp_quaternion : :class:`list` of :class:`float`
        Rotation of tool center plane in quaternions.
    cog_coord : :class:`list` of :class:`float`, optional
        Coordinates of center of gravity of tool. Defaults to ``[0, 0, 100]``.
    name : :class:`str`, optional
        Name of tool, used as variable name in :meth:`get_rapid_tooldata`.
        Defaults to ``"tool"``.
    weight : :class:`float`, optional
        Tool weight in kg. Defaults to ``5.0``.
    tolerance : :class:`int`, optional
        Tolerance used in Rapid tooldata string given by
        :meth:`get_rapid_tooldata`. Defaults to ``1e-6``.

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
        cog_coord=None,
        name="tool",
        weight=5.0,
        tolerance=1e-6,
    ):
        self.tcp_coord = tcp_coord
        self.tcp_quaternion = tcp_quaternion
        self.cog_coord = cog_coord if cog_coord else [0, 0, 100]
        self.name = name
        self.weight = weight
        self.tolerance = tolerance

    @property
    def tcp_frame(self):
        """TCP represented as a :class:`compas.geometry.Frame`."""
        return Frame.from_quaternion(self.tcp_quaternion, point=self.tcp_coord)

    @property
    def tcp_plane(self):
        """TCP represented as a :class:`Rhino.Geometry.Plane`."""
        from rapid_clay_formations_fab.rhino.compas_to_rhino import cgframe_to_rgplane

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
        name : :class:`str`, optional
        weight : :class:`float`, optional
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
        :class:`str`
        """
        data = self.tcp_coord + self.tcp_quaternion + [self.weight] + self.cog_coord
        formatted_data = [self._float_str(x) for x in data]

        return self.RAPID_TOOLDATA_FORMAT.format(self.name, *formatted_data)

    def _float_str(self, n):
        """Format float as string with given tolerance.

        Arguments
        ---------
        n : :class:`float` or :class:`int`
            Number to format

        Returns
        -------
        :class:`str`
        """
        # Get tolerance as number of decimals
        tol = -1 * math.floor(math.log(self.tolerance, 10))

        return "{:.{tol}f}".format(float(n), tol=int(tol))
