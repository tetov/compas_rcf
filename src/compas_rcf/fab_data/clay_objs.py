"""Data representation of discrete fabrication elements."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import math
from copy import deepcopy
from itertools import count

from compas.datastructures import Mesh as cg_Mesh
from compas.geometry import Frame
from compas.geometry import Primitive
from compas.geometry import Translation
from compas_ghpython.artists import MeshArtist

from compas_rcf.utils import ensure_frame
from compas_rcf.utils import get_offset_frame
from compas_rcf.utils import wrap_list


class ClayBullet(object):
    r"""Describes a clay cylinder.

    Parameters
    ----------
    location : :class:`Rhino.Geometry.Plane` or :class:`compas.geometry.Frame`
        Bottom centroid frame of clay volume.
    trajectory_to : :class:`list` of :class:`Rhino.Geometry.Plane` or :class:`compas.geometry.Frame`
        Frames defining path to take to place location.
    trajectory_from : :class:`list` of :class:`Rhino.Geometry.Plane` or :class:`compas.geometry.Frame`
        Frames defining path from place location to pick location.
    bullet_id : :class:`int`, optional
        Unique identifier.
    radius : :class:`float`, optional
        The radius of the initial cylinder.
    height : :class:`float`, optional
        The height of the initial cylinder.
    compression_ratio : :class:`float` (>0, <=1), optional
        The compression height ratio applied to the initial cylinder.
    clay_density : :class:`float`, optional
        Density of clay in g/mm\ :sup:`3`
    cycle_time : :class:`float`, optional
        Cycle time from pick to place and back.
    placed : :class:`int`, optional
        Time in epoch (seconds from 1970) of bullet placement.
    attrs : :obj:`dict`, optional
        Any other attributes needed.
    kwargs : :class:`dict`, optional
        Keyword arguments added as key-value pair to `attrs` and replaces value
        if key already present.
    """  # noqa: E501

    # creates id-s for objects
    _ids = count(0)

    def __init__(
        self,
        location,
        egress_frame_distance=200,
        trajectory_to=None,
        trajectory_from=None,
        bullet_id=None,
        radius=45,
        height=100,
        compression_ratio=0.5,
        clay_density=2.0,
        cycle_time=None,
        placed=None,
        attrs=None,
        **kwargs
    ):
        if not isinstance(location, Frame):
            raise Exception("Location should be given as a compas.geometry.Frame")
        self.location = location

        self.trajectory_to = trajectory_to or []
        self.trajectory_from = trajectory_from or []

        # sortable ID, used for fabrication sequence
        if not bullet_id:
            self.bullet_id = next(self._ids)
        else:
            self.bullet_id = bullet_id

        self.radius = radius
        self.height = height
        self.compression_ratio = compression_ratio
        self.egress_frame_distance = egress_frame_distance

        self.clay_density = clay_density

        self.cycle_time = cycle_time
        self.placed = placed

        self.attrs = attrs or {}
        self.attrs.update(kwargs)

    def get_location_plane(self):
        from compas_rcf.rhino import cgframe_to_rgplane

        return cgframe_to_rgplane(self.location)

    def get_normal(self):
        return self.location.normal * -1

    def get_uncompressed_top_frame(self):
        """:class:`compas.geometry.frame` Top of uncompressed cylinder."""
        vector = self.get_normal() * self.height
        T = Translation(vector)

        return self.location.transformed(T)

    def get_compressed_top_frame(self):
        """:class:`compas.geometry.frame` Top of compressed cylinder."""
        vector = self.get_normal() * self.get_compressed_height()
        T = Translation(vector)

        return self.location.transformed(T)

    def get_egress_frame(self):
        """Frame at end and start of trajectory to and from."""
        vector = self.get_normal() * self.egress_frame_distance
        T = Translation(vector)

        return self.get_uncompressed_top_frame().transformed(T)

    @property
    def trajectory_to(self):
        """Frames describing trajectory from picking station to placement moves.

        Returns
        -------
        list of :class:`compas.geometry.Frame`
        """
        return self._trajectory_to

    @trajectory_to.setter
    def trajectory_to(self, frame_list):
        """Ensure trajectory_to elements are :class:`compas.geometry.Frame` objects."""
        self._trajectory_to = []

        if isinstance(frame_list, collections.Sequence):
            for frame_like in frame_list:
                frame = ensure_frame(frame_like)
                self._trajectory_to.append(frame)
        else:
            frame = ensure_frame(frame_list)
            self._trajectory_to.append(frame)

    @property
    def trajectory_from(self):
        """Frames describing trajectory from last placement move to picking station.

        Returns
        -------
        list of :class:`compas.geometry.Frame`
        """
        return self._trajectory_from

    @trajectory_from.setter
    def trajectory_from(self, frame_list):
        """Ensure trajectory_from elements are :class:`compas.geometry.Frame` objects."""  # noqa: E501
        self._trajectory_from = []
        if isinstance(frame_list, collections.Sequence):
            for frame_like in frame_list:
                frame = ensure_frame(frame_like)
                self._trajectory_from.append(frame)
        else:
            frame = ensure_frame(frame_list)
            self._trajectory_from.append(frame)

    def get_uncompressed_centroid_frame(self):
        """Get frame at middle of uncompressed bullet."""
        vector = self.get_normal() * self.height / 2
        T = Translation(vector)

        return self.location.transformed(T)

    def get_compressed_centroid_frame(self):
        """Get frame at middle of compressed bullet."""
        vector = self.get_normal() * self.get_compressed_height() / 2
        T = Translation(vector)

        return self.location.transformed(T)

    def get_volume(self):
        r"""Volume of clay bullet in mm\ :sup:`3`\ .

        Returns
        -------
        float
        """
        return math.pi * self.radius ** 2 * self.height

    def get_volume_m3(self):
        r"""Volume of clay bullet in m\ :sup:`3`\ .

        Returns
        -------
        float
        """
        return self.volume * 1e-9

    def get_weight_kg(self):
        """Weight of clay bullet in kg.

        Returns
        -------
        float
        """
        return self.density * self.volume * 1e-6

    def get_weight(self):
        """Weight of clay bullet in g.

        Returns
        -------
        float
        """
        return self.weight_kg * 1000

    def get_compressed_radius(self):
        """Radius of clay bullet in mm when compressed to defined compression ratio.

        Returns
        -------
        float
        """
        return math.sqrt(self.get_volume() / (self.get_compressed_height() * math.pi))

    def get_compressed_height(self):
        """Height of clay bullet in mm when compressed to defined compression ratio.

        Returns
        -------
        float
        """
        return self.height * self.compression_ratio

    def get_rgcircle(self):
        """:class:`Rhino.Geometry.Circle` representing bullet footprint.

        Returns
        -------
        :class:`Rhino.Geometry.Circle`
        """
        from Rhino.Geometry import Circle

        return Circle(self.get_location_plane(), self.get_compressed_radius())

    def get_rgcylinder(self):
        """:class:`Rhino.Geometry.Cylinder` representing bullet.

        Returns
        -------
        :class:`Rhino.Geometry.Cylinder`
        """
        from Rhino.Geometry import Cylinder

        return Cylinder(self.get_rgcircle(), self.get_compressed_height())

    def get_rgvector_from_bullet_zaxis(self):
        """Vector through center of bullet.

        Returns
        -------
        :class:`compas.geometry.Vector`
        """
        return self.get_normal() * self.get_compressed_height()

    def copy(self):
        return deepcopy(self)

    def get_rgmesh(self, face_count=18):
        """Generate mesh representation of bullet with custom resolution.

        Parameters
        ----------
        face_count : :class:`int`, optional
            Desired number of faces, by default 18
            Used as a guide for the resolution of the mesh cylinder

        Returns
        -------
        :class:`Rhino.Geometry.Mesh`
        """
        import Rhino.Geometry as rg

        if face_count < 6:
            sides = 3
        elif face_count < 15:
            sides = 4
        else:
            sides = face_count // 3

        circle = self.get_rgcircle()

        polygons = []
        polygons.append(rg.Polyline.CreateInscribedPolygon(circle, sides))

        T = rg.Transform.Translation(circle.Normal * -self.get_compressed_height())

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

        # to Rhino.Geometry and clean it up
        rgmesh = MeshArtist(mesh).draw_mesh()
        rgmesh.UnifyNormals()
        rgmesh.Normals.ComputeNormals()

        return rgmesh

    def to_data(self):
        data = {}

        for key, value in self.__dict__.items():
            if isinstance(value, Primitive):
                data[key] = value.to_data()
            else:
                data[key] = value

        return data

    @classmethod
    def from_data(cls, data):
        """Construct a :class:`ClayBullet` instance from its data representation.

        Parameters
        ----------
        data : :obj:`dict`
            The data dictionary.

        Returns
        -------
        :class:`ClayBullet`
            The constructed ClayBullet instance
        """
        location = Frame.from_data(data.pop("location"))

        trajectory_to = []
        for frame_data in data.pop("_trajectory_to"):
            trajectory_to.append(Frame.from_data(frame_data))

        trajectory_from = []
        for frame_data in data.pop("_trajectory_from"):
            trajectory_from.append(Frame.from_data(frame_data))

        # To check for old attr name for id
        if "bullet_id" in data.keys():
            bullet_id = data.pop("bullet_id")
        elif "id" in data.keys():
            bullet_id = data.pop("id")
        else:
            bullet_id = None

        # Take the rest of the dictionary
        kwargs = data

        return cls(
            location,
            trajectory_to=trajectory_to,
            trajectory_from=trajectory_from,
            bullet_id=bullet_id,
            **kwargs
        )

    @classmethod
    def from_compressed_centroid_frame_like(
        cls, centroid_frame_like, compression_ratio=0.5, height=100, **kwargs
    ):
        """Construct a :class:`ClayBullet` instance from centroid plane.

        Parameters
        ----------
        centroid_frame_like : :class:`compas.geometry.Frame` or :class:`Rhino.Geometry.Plane`
            Frame between bottom of clay bullet and compressed top.
        compression_ratio : :class:`float`
            The compressed height as a percentage of the original height.
        height : :class:`float`
            The height of the bullet before compression.
        kwargs : :class:`dict`
            Other attributes.

        Returns
        -------
        :class:`ClayBullet`
            The constructed ClayBullet instance
        """  # noqa: E501
        centroid_frame = ensure_frame(centroid_frame_like)
        compressed_height = height * compression_ratio
        location = get_offset_frame(centroid_frame, -compressed_height / 2)

        return cls(
            location, compression_ratio=compression_ratio, height=height, **kwargs
        )


def check_id_collision(clay_bullets):
    """Check for duplicate ids in list of ClayBullet instances.

    Parameters
    ----------
    clay_bullets : list of :class:`ClayBullet`

    Raises
    ------
    Exception
        Raises exception when first duplicate is found
    """
    ids = [bullet.bullet_id for bullet in clay_bullets]

    set_of_ids = set()
    for id_ in ids:
        if id_ in set_of_ids:
            raise Exception(
                "Id {} appears more than once in list of ClayBullet instances".format(
                    id_
                )
            )
        set_of_ids.add(id_)
