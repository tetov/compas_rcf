"""Data representation of discrete fabrication elements."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import re
from copy import deepcopy

import compas.datastructures
import compas.geometry as cg
import compas_ghpython.artists

from rapid_clay_formations_fab.robots import MinimalTrajectory
from rapid_clay_formations_fab.robots import two_levels_reversed


class FabricationElement(object):
    r"""Describes a fabrication element for the RCF process.

    The element is assumed to be a cylinder and is expected to be compressed
    during fabrication.

    Parameters
    ----------
    location : :class:`Rhino.Geometry.Plane` or :class:`compas.geometry.Frame`
        Bottom centroid frame of element.
    id_: :obj:`str`
        Unique identifier.
    travel_trajectories : :obj:`list` of :class:`rapid_clay_formations_fab.robots.MinimalTrajectory`
        List of trajectories describing motion between picking egress and
        placing egress.
    place_trajectories : :obj:`list` of :class:`rapid_clay_formations_fab.robots.MinimalTrajectory`
        List of trajectories describing place motion.
    return_travel_trajectories : :obj:`list` of :class:`rapid_clay_formations_fab.robots.MinimalTrajectory`
        List of trajectories describing motion between placing and picking.
    return_place_trajectories : :obj:`list` of :class:`rapid_clay_formations_fab.robots.MinimalTrajectory`
        List of trajectories describing return motion from last compression
        motion to placing egress.
    radius : :obj:`float`, optional
        The radius of the initial cylinder.
    height : :obj:`float`, optional
        The height of the initial cylinder.
    compression_ratio : :obj:`float` (>0, <=1), optional
        The compression height ratio applied to the initial cylinder.
    density : :obj:`float`, optional
        Density in g/mm\ :sup:`3`.
    cycle_time : :obj:`float`, optional
        Cycle time from pick to place and back.
    placed : :obj:`bool`, optional
        If fabrication element has been placed or not.
    time_placed : :obj:`int`, optional
        Time in epoch (seconds from 1970) of fabrication element placement.
    attrs : :obj:`dict`, optional
        Any other attributes needed.
    """  # noqa: E501

    def __init__(
        # fmt: off
        # Stop black from adding comma after last element to retain py27 compat
        # See https://github.com/psf/black/issues/1356
        self,
        location,
        id_,
        radius=45,
        height=150,
        compression_ratio=0.5,
        egress_frame_distance=200,
        travel_trajectories=None,
        place_trajectories=None,
        return_travel_trajectories=None,
        return_place_trajectories=None,
        density=None,
        cycle_time=None,
        placed=False,
        time_placed=None,
        attrs=None
        # fmt: on
    ):
        if not isinstance(location, cg.Frame):
            raise Exception("Location should be given as a compas.geometry.Frame")
        self.location = location
        self.id_ = id_

        self.radius = radius
        self.height = height
        self.compression_ratio = compression_ratio
        self.egress_frame_distance = egress_frame_distance

        self.travel_trajectories = travel_trajectories
        self.place_trajectories = place_trajectories
        self.return_travel_trajectories = return_travel_trajectories
        self.return_place_trajectories = return_place_trajectories

        self.density = density

        self.cycle_time = cycle_time
        self.placed = placed
        self.time_placed = time_placed

        self.attrs = attrs or {}

    # Trajectories setup
    ######################

    @property
    def return_travel_trajectories(self):
        """:class:`rapid_clay_formations_fab.robots.MinimalTrajectory` : Either specific trajectories or reversed travel trajectories."""  # noqa: E501
        return self.return_travel_trajectories_ or two_levels_reversed(
            self.travel_trajectories
        )

    @return_travel_trajectories.setter
    def return_travel_trajectories(self, trajectories):
        self.return_travel_trajectories_ = trajectories

    @property
    def place_trajectories(self):
        """:class:`rapid_clay_formations_fab.robots.MinimalTrajectory` : Either specific trajectories or frame trajectories derived from location."""  # noqa: E501
        return self.place_trajectories_ or [
            MinimalTrajectory(
                [self.get_egress_frame(), self.get_uncompressed_top_frame()]
            ),
            MinimalTrajectory([self.get_compressed_top_frame()]),
        ]

    @place_trajectories.setter
    def place_trajectories(self, trajectories):
        self.place_trajectories_ = trajectories

    @property
    def return_place_trajectories(self):
        """:class:`rapid_clay_formations_fab.robots.MinimalTrajectory` : Either specific trajectories or reversed place trajectories."""  # noqa: E501
        return self.return_place_trajectories_ or two_levels_reversed(
            self.place_trajectories
        )

    @return_place_trajectories.setter
    def return_place_trajectories(self, trajectories):
        self.return_place_trajectories_ = trajectories

    # Derived frames
    ################

    def get_uncompressed_top_frame(self):
        """Top of uncompressed cylinder.

        Returns
        -------
        :class:`compas.geometry.Frame`
        """
        vector = self.get_normal() * self.height
        T = cg.Translation(vector)

        return self.location.transformed(T)

    def get_compressed_top_frame(self):
        """Top of compressed cylinder.

        Returns
        -------
        :class:`compas.geometry.Frame`
        """
        vector = self.get_normal() * self.get_compressed_height()
        T = cg.Translation(vector)

        return self.location.transformed(T)

    def get_egress_frame(self):
        """Get Frame at end and start of trajectory to and from.

        Returns
        -------
        :class:`compas.geometry.Frame`
        """
        vector = self.get_normal() * self.egress_frame_distance
        T = cg.Translation(vector)

        return self.get_uncompressed_top_frame().transformed(T)

    # Derived data points
    #####################

    def get_volume(self):
        r"""Get volume in mm\ :sup:`3`\ .

        Returns
        -------
        :obj:`float`
        """
        return math.pi * self.radius ** 2 * self.height

    def get_volume_m3(self):
        r"""Get volume in m\ :sup:`3`\ .

        Returns
        -------
        :obj:`float`
        """
        return self.volume * 1e-9

    def get_weight_kg(self):
        """Get weight in kg.

        Returns
        -------
        :obj:`float`
        """
        return self.density * self.volume * 1e-6

    def get_weight(self):
        """Get weight in g.

        Returns
        -------
        :obj:`float`
        """
        return self.weight_kg * 1000

    def get_compressed_radius(self):
        """Get radius in mm when compressed to defined compression ratio.

        This value assumes that fabrication material is completely elastic
        and that deformation is uniform.

        Returns
        -------
        :obj:`float`
        """
        return math.sqrt(self.get_volume() / (self.get_compressed_height() * math.pi))

    def get_compressed_height(self):
        """Get height of mm when compressed to defined compression ratio.

        Returns
        -------
        :obj:`float`
        """
        return self.height * self.compression_ratio

    # Construct geometrical representations of object using :any:`compas.geometry`.
    ###############################################################################

    def get_pt(self):
        """Get :class:`compas.geometry.Point` representation of bottom centroid of element.

        Returns
        -------
        :class:`compas.geometry.Point`
        """  # noqa: E501
        return self.location.point

    def get_normal(self):
        """Get normal direction of cylinder.

        Actually the reverse of the location frame's normal as it's used as a
        robot target frame and thus pointing "down".

        Returns
        -------
        :class:`compas.geometry.Vector`
        """
        return self.location.normal * -1

    def get_circle(self):
        """Get :class:`compas.geometry.Circle` representing fabrication element.

        Returns
        -------
        :class:`compas.geometry.Circle`
        """
        plane = cg.Plane(self.get_pt(), self.get_normal())
        return cg.Circle(plane, self.radius)

    def get_cylinder(self):
        """Get :class:`compas.geometry.Cylinder` representing fabrication element.

        Returns
        -------
        :class:`compas.geometry.Cylinder`
        """
        circle = self.get_circle()
        return cg.Cylinder(circle, self.height)

    def get_cgmesh(self, u_res=18):
        """Generate mesh representation of bullet with custom resolution.

        Parameters
        ----------
        face_count : :class:`int`, optional
            Desired number of faces, by default 18
            Used as a guide for the resolution of the mesh cylinder

        Returns
        -------
        :class:`compas.geometry.datastructures.Mesh`
        """
        cylinder = self.get_cylinder()
        return compas.datastructures.Mesh.from_shape(cylinder, u=u_res)

    # Construct geometrical representations of object using :any:`Rhino.Geometry`.
    ##############################################################################

    def get_location_rgplane(self):
        """Get location as Rhino.Geometry.Plane.

        Returns
        -------
        :class:`Rhino.Geometry.Plane`
        """
        from rapid_clay_formations_fab.rhino import cgframe_to_rgplane

        return cgframe_to_rgplane(self.location)

    def get_rgcircle(self):
        """Get :class:`Rhino.Geometry.Circle` representing element's footprint.

        Returns
        -------
        :class:`Rhino.Geometry.Circle`
        """
        from Rhino.Geometry import Circle

        return Circle(self.get_location_plane(), self.get_compressed_radius())

    def get_rgcylinder(self):
        """Get :class:`Rhino.Geometry.Cylinder` representation of element.

        Returns
        -------
        :class:`Rhino.Geometry.Cylinder`
        """
        from Rhino.Geometry import Cylinder

        return Cylinder(self.get_rgcircle(), self.get_compressed_height())

    def get_rgmesh(self, u_res=18):
        """Generate mesh representation of bullet with custom resolution.

        Parameters
        ----------
        face_count : :obj:`int`, optional
            Desired number of faces, by default 18
            Used as a guide for the resolution of the mesh cylinder

        Returns
        -------
        :class:`Rhino.Geometry.Mesh`
        """
        mesh = self.get_cgmesh(u_res=u_res)
        return compas_ghpython.artists.MeshArtist(mesh).draw_mesh()

    def copy(self):
        """Get a copy of instance.

        Returns
        -------
        :class:`FabricationElement`
        """
        return deepcopy(self)

    def to_data(self):
        """Get :obj:`dict` representation of :class:`FabricationElement`."""
        # TODO: Refactor this to independent to_data function.
        data = {}

        for key, value in self.__dict__.items():
            if hasattr(value, "to_data"):
                data[key] = value.to_data()
            else:
                data[key] = value

        return data

    @classmethod
    def from_data(cls, data):
        """Construct a :class:`FabricationElement` from a dictionary representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        :class:`FabricationElement`
        """

        kwargs = {}

        location = cg.Frame.from_data(data.pop("location"))

        # fmt: off
        # Stop black from adding comma after last element to retain py27 compat
        # See https://github.com/psf/black/issues/1356
        trajectory_attributes = (
            "travel_trajectories",
            "place_trajectories_",
            "return_travel_trajectories_",
            "return_place_trajectories_"
        )
        # fmt: on

        for key in trajectory_attributes:
            trajectories_data = data.pop(key, None)

            if trajectories_data:
                keyword = re.sub(r"_$", "", key)  # Strip underscore from end of key
                trajectories = []
                for traj_data in trajectories_data:
                    trajectories.append(MinimalTrajectory.from_data(traj_data))

                kwargs[keyword] = trajectories

        # merge kwargs with data
        kwargs.update(data)

        return cls(location, **kwargs)
