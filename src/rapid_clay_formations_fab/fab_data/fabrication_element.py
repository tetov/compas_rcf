"""Data representation of discrete fabrication elements."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math

import compas.datastructures
import compas.geometry as cg

try:
    import Rhino.Geometry as rg

    from rapid_clay_formations_fab.rhino import cgframe_to_rgplane
except ImportError:
    pass

try:
    import typing

    if typing.TYPE_CHECKING:
        from compas_rrc import FutureResult

        from rapid_clay_formations_fab.robots import MinimalTrajectories
except ImportError:
    pass


class FabricationElement(object):
    """Describes a fabrication element in the RCF process.

    The element is assumed to be cylindrical.

    Parameters
    ----------
    location : :class:`compas.geometry.Frame`
        Bottom centroid frame of element.
    id_: :obj:`str`
        Unique identifier.
    radius : :obj:`float`, optional
        The radius of the initial element.
    height : :obj:`float`, optional
        The height of the initial element.
    egress_frame_distance : :obj:`float`, optional
        Distance from top frame to travel to before interacting with element.
    attrs : :obj:`dict`, optional
        Any other attributes needed.
    """

    def __init__(
        self,
        location,  # type: cg.Frame
        id_=None,  # type: str
        radius=45,  # type: float
        height=150,  # type: float
        egress_frame_distance=200,  # type: float
        attrs=None,  # type: dict
    ):  # type: (...) -> None
        self.location = location
        self.id_ = id_
        self.radius = radius
        self.height = height
        self.egress_frame_distance = egress_frame_distance
        self.attrs = attrs or {}

        # Not included in data functions since this value is only valid during
        # fabrication run.
        self.cycle_time_future = None  # type: FutureResult

    def __repr__(self):
        return "FabricationElement({}, {}, {}, {}. {})".format(
            self.location,
            self.id_,
            self.radius,
            self.height,
            self.egress_frame_distance,
        )

    @property
    def data(self):
        """:obj:`dict` : The data dictionary that represents the :class:`FabricationElement`."""  # noqa: E501
        return {
            "location": self.location,
            "id_": self.id_,
            "radius": self.radius,
            "height": self.height,
            "egress_frame_distance": self.egress_frame_distance,
            "attrs": self.attrs,
        }

    @data.setter
    def data(self, data):
        self.location = data["location"]
        self.id_ = data["id_"]
        self.radius = data["radius"]
        self.height = data["height"]
        self.egress_frame_distance = data["egress_frame_distance"]
        self.attrs = data["attrs"]

    def transform(self, transformation):
        """Get a transformed copy of :class:`FabricationElement`.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`
        """
        self.location.transform(transformation)

    def transformed(self, transformation):
        """Get a transformed copy of :class:`FabricationElement`.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`

        Returns
        -------
        :class:`FabricationElement`
        """
        copy = self.copy()
        copy.transform(transformation)
        return copy

    # Derived frames
    #####################

    def get_top_frame(self):
        """Top of uncompressed cylinder.

        Returns
        -------
        :class:`compas.geometry.Frame`
        """
        vector = self.get_normal() * self.height
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

        return self.get_top_frame().transformed(T)

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

    def get_weight(self):
        """Get weight in g.

        Returns
        -------
        :obj:`float`
        """
        return self.weight_kg * 1000

    def get_weight_kg(self):
        """Get weight in kg.

        Returns
        -------
        :obj:`float`
        """
        return self.attrs.get("density", 0) * self.volume * 1e-6

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
        return cg.Cylinder(circle, self.get_compressed_height())

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
        return compas.datastructures.Mesh.from_shape(cylinder, u=int(u_res))

    # Construct geometrical representations of object using :any:`Rhino.Geometry`.
    ##############################################################################

    def get_location_rgplane(self):
        """Get location as Rhino.Geometry.Plane.

        Returns
        -------
        :class:`Rhino.Geometry.Plane`
        """
        return cgframe_to_rgplane(self.location)

    def get_rgcircle(self):
        """Get :class:`Rhino.Geometry.Circle` representing element's footprint.

        Returns
        -------
        :class:`Rhino.Geometry.Circle`
        """
        return rg.Circle(self.get_location_rgplane(), self.radius)

    def get_rgcylinder(self):
        """Get :class:`Rhino.Geometry.Cylinder` representation of element.

        Returns
        -------
        :class:`Rhino.Geometry.Cylinder`
        """
        return rg.Cylinder(self.get_rgcircle(), self.height)

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
        v_res = u_res - 2
        return rg.Mesh.CreateFromCylinder(self.get_rgcylinder(), v_res, u_res)

    # Constructors and conversions
    ##############################

    def copy(self):
        """Create a copy of this :class:`FabricationElement`.

        Returns
        -------
        :class:`FabricationElement`
            An instance of :class:`FabricationElement`
        """
        cls = type(self)
        return cls.from_data(self.data)

    def to_data(self):
        """Get :obj:`dict` representation of :class:`FabricationElement`."""
        return self.data

    @classmethod
    def from_data(cls, data):
        """Construct an instance from its data representation.

        Parameters
        ----------
        data : :obj:`dict`

        Returns
        -------
        :class:`FabricationElement`
        """
        obj = cls(cg.Frame.worldXY())
        obj.data = data
        return obj


class PlaceElement(FabricationElement):
    """Describes a fabrication element to be placed in the RCF process.

    The element is assumed to be cylindrical and expected to be compressed
    during fabrication.

    Parameters
    ----------
    location : :class:`compas.geometry.Frame`
        Bottom centroid frame of element.
    id_: :obj:`str`
        Unique identifier.
    radius : :obj:`float`, optional
        The radius of the initial element.
    height : :obj:`float`, optional
        The height of the initial element.
    egress_frame_distance : :obj:`float`, optional
        Distance from top frame to travel to before placing.
    compression_ratio : :obj:`float` (>0, <=1), optional
        The compression height ratio applied to the initial element.
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
        self,
        location,  # type: cg.Frame
        id_,  # type: str
        radius=45,  # type: float
        height=150,  # type: float
        compression_ratio=0.5,  # type: float
        egress_frame_distance=200,  # type: float
        travel_trajectories=None,  # type: MinimalTrajectories
        place_trajectories=None,  # type: MinimalTrajectories
        return_travel_trajectories=None,  # type: MinimalTrajectories
        return_place_trajectories=None,  # type: MinimalTrajectories
        cycle_time=None,  # type: float
        placed=False,  # type: bool
        time_placed=None,  # type: float
        attrs=None,  # type: dict
    ):  # type: (...) -> None
        super(PlaceElement, self).__init__(
            location,
            id_=id_,
            radius=radius,
            height=height,
            egress_frame_distance=egress_frame_distance,
            attrs=attrs,
        )
        self.compression_ratio = compression_ratio

        self.travel_trajectories = travel_trajectories
        self.place_trajectories = place_trajectories
        self.return_travel_trajectories = return_travel_trajectories
        self.return_place_trajectories = return_place_trajectories

        self.cycle_time = cycle_time
        self.placed = placed
        self.time_placed = time_placed

    @property
    def data(self):
        """:obj:`dict` : The data dictionary that represents the :class:`PlaceElement`."""  # noqa: E501
        data = super(PlaceElement, self).data

        data["compression_ratio"] = self.compression_ratio
        data["cycle_time"] = self.cycle_time
        data["placed"] = self.placed
        data["time_placed"] = self.time_placed

        data["travel_trajectories"] = self.travel_trajectories
        data["return_travel_trajectories"] = self.return_travel_trajectories
        data["place_trajectories"] = self.place_trajectories
        data["return_place_trajectories"] = self.return_place_trajectories

        return data

    @data.setter
    def data(self, data):
        # This is needed to use the setter on parent class
        # https://stackoverflow.com/a/37663266
        super(PlaceElement, self.__class__).data.fset(self, data)

        self.compression_ratio = data.get("compression_ratio")
        self.cycle_time = data.get("cycle_time")
        self.placed = data.get("placed")
        self.time_placed = data.get("time_placed")

        self.travel_trajectories = data.get("travel_trajectories")
        self.return_travel_trajectories = data.get("return_travel_trajectories")
        self.place_trajectories = data.get("place_trajectories")
        self.return_place_trajectories = data.get("return_place_trajectories")

    # Derived frames
    ################

    def get_uncompressed_top_frame(self):
        """Top of uncompressed element.

        Alias of :meth:`FabricationElement.get_top_frame`.

        Returns
        -------
        :class:`compas.geometry.Frame`
        """
        return self.get_top_frame()

    def get_compressed_top_frame(self):
        """Top of compressed element.

        Returns
        -------
        :class:`compas.geometry.Frame`
        """
        vector = self.get_normal() * self.get_compressed_height()
        T = cg.Translation(vector)

        return self.location.transformed(T)

    # Derived data points
    #####################

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

    def get_circle(self):
        """Get :class:`compas.geometry.Circle` representing fabrication element.

        Returns
        -------
        :class:`compas.geometry.Circle`
        """
        plane = cg.Plane(self.get_pt(), self.get_normal())
        return cg.Circle(plane, self.get_compressed_radius())

    def get_cylinder(self):
        """Get :class:`compas.geometry.Cylinder` representing fabrication element.

        Returns
        -------
        :class:`compas.geometry.Cylinder`
        """
        circle = self.get_circle()
        return cg.Cylinder(circle, self.get_compressed_height())

    def get_rgcircle(self):
        """Get :class:`Rhino.Geometry.Circle` representing element's footprint.

        Returns
        -------
        :class:`Rhino.Geometry.Circle`
        """
        return rg.Circle(self.get_location_rgplane(), self.get_compressed_radius())

    def get_rgcylinder(self):
        """Get :class:`Rhino.Geometry.Cylinder` representation of element.

        Returns
        -------
        :class:`Rhino.Geometry.Cylinder`
        """
        return rg.Cylinder(self.get_rgcircle(), self.get_compressed_height())

    @classmethod
    def from_data(cls, data):
        """Construct an instance from its data representation.

        Parameters
        ----------
        data : :obj:`dict`

        Returns
        -------
        :class:`FabricationElement`
        """
        obj = cls(cg.Frame.worldXY(), "")
        obj.data = data
        return obj
