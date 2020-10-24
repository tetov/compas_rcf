"""Data representation of discrete fabrication elements."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import re
from copy import deepcopy

from compas.datastructures import Mesh as cg_Mesh
from compas.geometry import Frame
from compas.geometry import Translation
from compas_fab.robots import JointTrajectory
from compas_ghpython.artists import MeshArtist

from rapid_clay_formations_fab.robots import reversed_trajectories
from rapid_clay_formations_fab.utils import wrap_list


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
    travel_trajectories : :obj:`list` of :class:`compas_fab.robots.JointTrajectory`
        List of trajectories describing motion between picking egress and
        placing egress.
    place_trajectories : :obj:`list` of :class:`compas_fab.robots.JointTrajectory`
        List of trajectories describing place motion.
    return_travel_trajectories : :obj:`list` of :class:`compas_fab.robots.JointTrajectory`
        List of trajectories describing motion between placing and picking.
    return_place_trajectories : :obj:`list` of :class:`compas_fab.robots.JointTrajectory`
        List of trajectories describing return motion from last compression motion to placing egress.
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
        density=2.0,
        cycle_time=None,
        placed=False,
        time_placed=None,
        attrs=None
    ):
        if not isinstance(location, Frame):
            raise Exception("Location should be given as a compas.geometry.Frame")
        self.location = location
        self.id_ = id_

        self.radius = radius
        self.height = height
        self.compression_ratio = compression_ratio
        self.egress_frame_distance = egress_frame_distance

        self.travel_trajectories = travel_trajectories or []
        self.place_trajectories = place_trajectories or []
        self.return_travel_trajectories = return_travel_trajectories or []
        self.return_place_trajectories = return_place_trajectories or []

        self.density = density

        self.cycle_time = cycle_time
        self.placed = placed
        self.time_placed = time_placed

        self.attrs = attrs or {}

    @property
    def return_travel_trajectories(self):
        return self.return_travel_trajectories_ or reversed_trajectories(
            self.travel_trajectories
        )

    @return_travel_trajectories.setter
    def return_travel_trajectories(self, trajectories):
        self.return_travel_trajectories_ = trajectories

    @property
    def return_place_trajectories(self):
        return self.return_place_trajectories_ or reversed_trajectories(
            self.place_trajectories
        )

    @return_place_trajectories.setter
    def return_place_trajectories(self, trajectories):
        self.return_place_trajectories_ = trajectories

    def get_location_plane(self):
        """Get location as Rhino.Geometry.Plane.

        Returns
        -------
        :class:`Rhino.Geometry.Plane`
        """
        from rapid_clay_formations_fab.rhino import cgframe_to_rgplane

        return cgframe_to_rgplane(self.location)

    def get_normal(self):
        """Get normal direction of cylinder.

        Actually the reverse of the location frame's normal as it's used as a
        robot target frame and thus pointing "down".

        Returns
        -------
        :class:`compas.geometry.Vector`
        """
        return self.location.normal * -1

    def get_uncompressed_top_frame(self):
        """Top of uncompressed cylinder.

        Returns
        -------
        :class:`compas.geometry.Frame`
        """
        vector = self.get_normal() * self.height
        T = Translation(vector)

        return self.location.transformed(T)

    def get_compressed_top_frame(self):
        """Top of compressed cylinder.

        Returns
        -------
        :class:`compas.geometry.Frame`
        """
        vector = self.get_normal() * self.get_compressed_height()
        T = Translation(vector)

        return self.location.transformed(T)

    def get_egress_frame(self):
        """Get Frame at end and start of trajectory to and from.

        Returns
        -------
        :class:`compas.geometry.Frame`
        """
        vector = self.get_normal() * self.egress_frame_distance
        T = Translation(vector)

        return self.get_uncompressed_top_frame().transformed(T)

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

    def copy(self):
        """Get a copy of instance.

        Returns
        -------
        :class:`FabricationElement`
        """
        return deepcopy(self)

    def get_cgmesh(self, face_count=18):
        """Get :class:`compas.datastructures.Mesh` representation of element.

        Parameters
        ----------
        face_count : :class:`int`, optional
            Desired number of faces, by default 18
            Used as a guide for the resolution of the mesh cylinder

        Returns
        -------
        :class:`compas.geometry.datastructures.Mesh`
        """
        # TODO: Rewrite as pure compas (unnecessary but neat)
        import Rhino.Geometry as rg

        from rapid_clay_formations_fab.rhino import cgvector_to_rgvector

        if face_count < 6:
            sides = 3
        elif face_count < 15:
            sides = 4
        else:
            sides = face_count // 3

        circle = self.get_rgcircle()

        polygons = []
        polygons.append(rg.Polyline.CreateInscribedPolygon(circle, sides))

        T = rg.Transform.Translation(
            cgvector_to_rgvector(self.get_normal()) * self.get_compressed_height()
        )

        second_polygon = polygons[0].Duplicate()
        second_polygon.Transform(T)

        polygons.append(second_polygon)

        mesh = cg_Mesh()
        outer_verts_polygons = []

        # generate verts at polygon corners
        for polygon in polygons:
            _temp_list = []

            polygon_corners = list(polygon.Item)
            polygon_corners.pop()  # remove end pt since == start pt

            for pt in polygon_corners:
                _temp_list.append(mesh.add_vertex(x=pt.X, y=pt.Y, z=pt.Z))
            outer_verts_polygons.append(_temp_list)

        polygon_faces = []
        for vkeys in outer_verts_polygons:
            polygon_faces.append(mesh.add_face(vkeys))

        # if >4 sides polygon, create faces by tri subd
        if sides > 4:

            centroid_verts = []
            for fkey in polygon_faces:
                x, y, z = mesh.face_centroid(fkey)
                centroid_verts.append(mesh.add_vertex(x=x, y=y, z=z))
                mesh.delete_face(fkey)

            # create new faces
            for vkeys, ckey in zip(outer_verts_polygons, centroid_verts):
                for i, vkey in enumerate(vkeys):
                    next_vkey = wrap_list(vkeys, i + 1)
                    mesh.add_face([ckey, vkey, next_vkey])

        # generate faces between polygons
        vertex_for_vertex = zip(*outer_verts_polygons)

        for i, mirror_corners_1 in enumerate(vertex_for_vertex):
            mirror_corners_2 = wrap_list(vertex_for_vertex, i + 1)
            mesh.add_face(mirror_corners_1 + mirror_corners_2[::-1])

        return mesh

    def get_rgmesh(self, face_count=18):
        """Generate :class:`Rhino.Geometry.Mesh` representation of element.

        Parameters
        ----------
        face_count : :obj:`int`, optional
            Desired number of faces, by default 18
            Used as a guide for the resolution of the mesh cylinder

        Returns
        -------
        :class:`Rhino.Geometry.Mesh`
        """
        mesh = self.get_cgmesh(face_count=face_count)
        # to Rhino.Geometry and clean it up
        rgmesh = MeshArtist(mesh).draw_mesh()
        rgmesh.UnifyNormals()
        rgmesh.Normals.ComputeNormals()

        return rgmesh

    def to_data(self):
        """Get :obj:`dict` representation of :class:`FabricationElement`."""
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

        def trajectory_from_data(traj_data):
            try:
                return JointTrajectory.from_data(traj_data)
            except AttributeError:
                return [Frame.from_data(frame_data) for frame_data in traj_data]

        kwargs = {}

        location = Frame.from_data(data.pop("location"))

        # fmt: off
        # Stop black from adding comma after last element to retain py27 compat
        # See https://github.com/psf/black/issues/1356
        trajectory_attributes = (
            "travel_trajectories",
            "place_trajectories",
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
                    trajectories.append(trajectory_from_data(traj_data))

                kwargs[keyword] = trajectories

        # merge kwargs with data
        kwargs.update(data)

        return cls(location, **kwargs)
