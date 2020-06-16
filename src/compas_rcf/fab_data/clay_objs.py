"""Data representation of discrete fabrication elements."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import math
from itertools import count

from compas import IPY
from compas.datastructures import Mesh as cg_Mesh
from compas.datastructures import Network
from compas.geometry import Frame
from compas.geometry import Translation
from compas_ghpython.artists import MeshArtist

from compas_rcf.utils import ensure_frame
from compas_rcf.utils import get_offset_frame
from compas_rcf.utils import wrap_list

if IPY:
    import Rhino.Geometry as rg
    from compas_rcf.rhino import cgframe_to_rgplane


class ClayBullet(object):
    """Describes a clay cylinder, this project's building element.

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
    kwargs : :class:`dict`, optional
        Any other attributes needed.
    """  # noqa: E501

    # creates id-s for objects
    _ids = count(0)

    def __init__(
        self,
        location,
        trajectory_to=[],
        trajectory_from=[],
        bullet_id=None,
        radius=45,
        height=100,
        compression_ratio=0.5,
        clay_density=2.0,
        cycle_time=None,
        placed=None,
        **kwargs
    ):
        self.location = location
        self.trajectory_to = trajectory_to
        self.trajectory_from = trajectory_from

        # sortable ID, used for fabrication sequence
        if not bullet_id:
            self.bullet_id = next(self._ids)
        else:
            self.bullet_id = bullet_id

        self.radius = radius
        self.height = height
        self.compression_ratio = compression_ratio

        self.cycle_time = cycle_time
        self.placed = placed

        if kwargs:
            for key in kwargs.keys():
                setattr(self, key, kwargs[key])

    @property
    def location(self):
        """Frame specifying location of bottom of clay cylinder.

        Returns
        -------
        :class:`compas.geometry.Frame`
        """
        return self._location

    @location.setter
    def location(self, frame_like):
        """Ensure that location is stored as :class:`compas.geometry.Frame` object."""
        self._location = ensure_frame(frame_like)

    @property
    def placement_frame(self):
        """Last frame in placement procedure.

        Derived from location, height and compression ratio.

        Returns
        -------
        :class:`compas.geometry.Frame`
        """
        vector = self.location.zaxis * self.compressed_height * -1
        T = Translation(vector)

        return self._location.transformed(T)

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

    @property
    def centroid_frame(self):
        """Get frame at middle of uncompressed bullet."""
        return get_offset_frame(self.location, self.height)

    @property
    def compressed_centroid_frame(self):
        """Get frame at middle of compressed bullet."""
        return get_offset_frame(self.location, self.compressed_height)

    @property
    def plane(self):
        """For compatibility with older scripts."""
        return self.location_plane

    @property
    def location_plane(self):
        """:class:`Rhino.Geometry.Plane` representation of location frame.

        Returns
        -------
        :class:`Rhino.Geometry.Plane`
        """
        return cgframe_to_rgplane(self.location)

    @property
    def placement_plane(self):
        """:class:`Rhino.Geometry.Plane` representation of placement frame.

        Returns
        -------
        :class:`Rhino.Geometry.Plane`
        """
        return cgframe_to_rgplane(self.placement_frame)

    @property
    def trajectory_to_planes(self):
        """:class:`Rhino.Geometry.Plane` representations of trajectory_to frames.

        Returns
        -------
        :class:`list` of :class:`Rhino.Geometry.Plane`
        """
        return [cgframe_to_rgplane(frame) for frame in self.trajectory_to]

    @property
    def trajectory_from_planes(self):
        """:class:`Rhino.Geometry.Plane` representations of trajectory_from frames.

        Returns
        -------
        :class:`list` of :class:`Rhino.Geometry.Plane`
        """
        return [cgframe_to_rgplane(frame) for frame in self.trajectory_from]

    @property
    def centroid_plane(self):
        """Get plane at middle of uncompressed bullet.

        Returns
        -------
        :class:`Rhino.Geometry.Plane`
        """
        return cgframe_to_rgplane(self.centroid_frame)

    @property
    def compressed_centroid_plane(self):
        """Get plane at middle of compressed bullet.

        Returns
        -------
        :class:`Rhino.Geometry.Plane`
        """
        return cgframe_to_rgplane(self.centroid_frame)

    @property
    def volume(self):
        r"""Volume of clay bullet in mm\ :sup:`3`\ .

        Returns
        -------
        float
        """
        return math.pi * self.radius ** 2 * self.height

    @property
    def volume_m3(self):
        r"""Volume of clay bullet in m\ :sup:`3`\ .

        Returns
        -------
        float
        """
        return self.volume * 1e-9

    @property
    def weight_kg(self):
        """Weight of clay bullet in kg.

        Returns
        -------
        float
        """
        return self.density * self.volume * 1e-6

    @property
    def weight(self):
        """Weight of clay bullet in g.

        Returns
        -------
        float
        """
        return self.weight_kg * 1000

    @property
    def compressed_radius(self):
        """Radius of clay bullet in mm when compressed to defined compression ratio.

        Returns
        -------
        float
        """
        return math.sqrt(self.volume / (self.compressed_height * math.pi))

    @property
    def compressed_height(self):
        """Height of clay bullet in mm when compressed to defined compression ratio.

        Returns
        -------
        float
        """
        return self.height * self.compression_ratio

    @property
    def circle(self):
        """:class:`Rhino.Geometry.Circle` representing bullet footprint.

        Returns
        -------
        :class:`Rhino.Geometry.Circle`
        """
        return rg.Circle(self.location_plane, self.compressed_radius)

    @property
    def cylinder(self):
        """:class:`Rhino.Geometry.Cylinder` representing bullet.

        Returns
        -------
        :class:`Rhino.Geometry.Cylinder`
        """
        return rg.Cylinder(self.circle, self.compressed_height)

    @property
    def vector_from_bullet_zaxis(self):
        """Vector through center of bullet.

        Returns
        -------
        :class:`compas.geometry.Vector`
        """
        return self.location.normal * self.compressed_height

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
        location = Frame.from_data(data.pop("_location"))

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
        cls, centroid_frame_like, compression_ratio=0.5, height=100, kwargs={}
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

    def generate_mesh(self, face_count=18):
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
        if face_count < 6:
            sides = 3
        elif face_count < 15:
            sides = 4
        else:
            sides = face_count // 3

        polygons = []
        polygons.append(rg.Polyline.CreateInscribedPolygon(self.circle, sides))

        T = rg.Transform.Translation(self.circle.Normal * -self.compressed_height)

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
        rg_mesh = MeshArtist(mesh).draw_mesh()
        rg_mesh.UnifyNormals()
        rg_mesh.Normals.ComputeNormals()

        return rg_mesh


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
    ids = [bullet.id for bullet in clay_bullets]

    set_of_ids = set()
    for id in ids:
        if id in set_of_ids:
            raise Exception(
                "Id {} appears more than once in list of ClayBullet instances".format(
                    id
                )
            )
        set_of_ids.add(id)


class ClayStructure(Network):
    def __init__(self, clay_bullets):
        super(ClayStructure, self).__init__()
        self._clay_bullets = clay_bullets
        self.network_from_clay_bullets(self._clay_bullets)
        self.update_default_edge_attributes(relation=None)
        self.update_default_edge_attributes(is_touching=False)

    @property
    def clay_bullets(self):
        return self.vertices

    @property
    def average_compressed_radius(self):
        sum_ = sum([bullet.compressed_radius for bullet in self._clay_bullets])
        return sum_ / len(self._clay_bullets)

    def _edges_from_distance(self, i, clay_bullet):
        edges = []
        for j, other_bullet in enumerate(self._clay_bullets):
            if i == j:
                continue
            dist = clay_bullet.plane.Origin.DistanceTo(other_bullet.plane.Origin)
            if dist <= clay_bullet.compressed_radius + other_bullet.compressed_radius:
                edges.append((i, j))  # equivalent to set.update()
        return edges

    def _set_attributes_edges_longer_than(self, dist, **kwargs):
        if len(kwargs) < 1:
            raise Exception("No attributes to set")

        keys = []
        for u, v in self.edges():
            if self.edge_length(u, v) >= dist:
                keys.append((u, v))

        self.set_edges_attributes(kwargs.keys(), kwargs.values(), keys=keys)

    def _bullet_neighboors_below(self, u):
        z_value = self.get_vertex_attribute(u, "z")
        bullets_below = self.vertices_where({"z": (0, z_value)})

        bullets_below_keys = [(u, v) for v in bullets_below if v != u]
        for u, v in bullets_below_keys:
            if self.edge_length(u, v) <= 20:
                self.add_edge(u, v, relation="neighboor_below", is_touching=True)

    def network_from_clay_bullets(self, clay_bullets):
        for i, clay_bullet in enumerate(clay_bullets):
            self.add_vertex(
                key=i,
                x=clay_bullet.plane.Origin.X,
                y=clay_bullet.plane.Origin.Y,
                z=clay_bullet.plane.Origin.Z,
                class_instance=clay_bullet,
            )

        edges_from_order = [(i, i + 1) for i in range(len(clay_bullets) - 1)]

        for u, v in edges_from_order:
            self.add_edge(u, v, relation="print_order", is_touching=True)

        # TODO: Better distance value
        self._set_attributes_edges_longer_than(26, is_touching=False)

        for i in range(len(self._clay_bullets)):
            self._bullet_neighboors_below(i)
