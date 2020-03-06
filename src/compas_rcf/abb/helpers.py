"""Helpers for scripts interacting with ABB robots or RAPID code."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from compas import IPY
from compas.geometry import Frame

from compas_rcf.utils.util_funcs import ensure_frame

if IPY:
    from compas_rcf.rhino import rgpoint_to_cgpoint
    from compas_rcf.rhino import cgframe_to_rgplane


log = logging.getLogger(__name__)


class RapidToolData(object):
    """Create Rapid ToolData

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

    RAPID_DECLARATION_PART = "TASK PERS tooldata {}"
    RAPID_TCP_PART = (
        ":=[TRUE,[[{:.8f}, {:.8f}, {:.8f}],[{:.8f}, {:.8f}, {:.8f}, {:.8f}]], "
    )
    RAPID_COG_PART = "[{:.5f},[{:.8f}, {:.8f}, {:.8f}], [1, 0, 0, 0], 0, 0, 0]];"

    def __init__(
        self, tcp_coord, tcp_quaternion, cog_coord=[0, 0, 0], name="tool", weight=5.0
    ):
        self.tcp_coord = tcp_coord
        self.tcp_quaternion = tcp_quaternion
        self.cog_coord = cog_coord
        self.name = name
        self.weight = weight

    def __repr__(self):
        tcp_xyzwxyz = [float(x) for x in self.tcp_coord + self.tcp_quaternion]
        load_data = [float(x) for x in [self.weight] + self.cog_coord]

        declaration = self.RAPID_DECLARATION_PART.format(self.name)
        tcp = self.RAPID_TCP_PART.format(*tcp_xyzwxyz)
        load_data = self.RAPID_COG_PART.format(*load_data)
        return declaration + tcp + load_data

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
            cog_coord = cog_pt.data
        else:
            cog_coord = [0, 0, 0]

        return cls(tcp_coord, tcp_quaternion, cog_coord=cog_coord, **kwargs)

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
        tcp_frame = ensure_frame(tcp_plane)

        if "cog_pt" in kwargs.keys():
            kwargs["cog_pt"] = rgpoint_to_cgpoint(kwargs["cog_pt"])

        return cls.from_frame_point(tcp_frame, **kwargs)
