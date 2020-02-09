from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import math
from itertools import count

import compas.geometry as cg
from compas.datastructures import Mesh as cg_Mesh
from compas.geometry import Frame
from compas.geometry import Translation
from compas_ghpython.artists import MeshArtist

from compas_rcf import IPY
from compas_rcf.utils import ensure_frame
from compas_rcf.utils import list_elem_w_index_wrap
from compas_rcf.utils.compas_to_rhino import cgframe_to_rgplane

if IPY:
    import Rhino.Geometry as rg


class ClayBullet(object):
    """Simple Clay Cylinder.

    Parameters
    ----------
    location: Rhino.Geometry.Plane, compas.geometry.Plane, compas.geometry.Frame

    radius : float, optional
        The radius of the initial cylinder.
    height : float, optional
        The height of the initial cylinder.
    compression_ratio : float (>0, <=1), optional
        The ratio of compression applied to the initial cylinder.
    """

    # creates id-s for objects
    _ids = count(0)

    def __init__(self,
                 location,
                 trajectory_to=[],
                 trajectory_from=[],
                 id=None,
                 radius=40,
                 height=200,
                 compression_ratio=1,
                 precision=5,
                 tool=None):
        self.location = location
        self.trajectory_to = trajectory_to  # property & setter to convert planes to frames
        self.trajectory_from = trajectory_from  # property & setter to convert planes to frames

        # sortable ID, used for fabrication sequence
        if id is None:
            self.id = next(self._ids)
        else:
            self.id = str(id) + 'x'

        self.radius = radius
        self.height = height
        self.compression_ratio = compression_ratio
        self.tool = tool

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
        """Ensure that location is stored as compas.geometry.Frame object."""
        self._location = ensure_frame(frame_like)

    @property
    def placement_frame(self):
        """Last frame in placement procedure, derived from location, height and compression ratio.

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
        """Ensure that trajectory_to are stored as compas.geometry.Frame objects."""
        self._trajectory_to = []
        for frame_like in frame_list:
            frame = ensure_frame(frame_like)
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
        """Ensure that trajectory_from are stored as compas.geometry.Frame objects."""
        self._trajectory_from = []
        for frame_like in frame_list:
            frame = ensure_frame(frame_like)
            self._trajectory_from.append(frame)

    @property
    def plane(self):
        """For Compatibility with older scripts."""
        return self.location_plane

    @property
    def location_plane(self):
        """Rhino.Geometry.Plane representation of location frame.

        Returns
        -------
        Rhino.Geometry.Plane
        """
        return cgframe_to_rgplane(self.location)

    @property
    def placement_plane(self):
        """Rhino.Geometry.Plane representation of placement frame.

        Returns
        -------
        Rhino.Geometry.Plane
        """
        return cgframe_to_rgplane(self.placement_frame)

    @property
    def pre_planes(self):
        """Rhino.Geometry.Plane representations of pre frames.

        Returns
        -------
        Rhino.Geometry.Plane
        """
        return [cgframe_to_rgplane(frame) for frame in self.trajectory_to]

    @property
    def post_planes(self):
        """Rhino.Geometry.Plane representation of pre frames.

        Returns
        -------
        Rhino.Geometry.Plane
        """
        return [cgframe_to_rgplane(frame) for frame in self.post_planes]

    @property
    def volume(self):
        """Volume of clay bullet in mm^3.

        Returns
        -------
        float
        """
        return math.pi * self.radius**2 * self.height

    @property
    def volume_m3(self):
        """Volume of clay bullet in m^3.

        Returns
        -------
        float
        """
        return self.volume * 1e-9

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
        """Rhino.Geometry.Circle representing bullet footprint.

        Returns
        -------
        Rhino.Geometry.Circle
        """
        return rg.Circle(self.location_plane, self.compressed_radius)

    @property
    def cylinder(self):
        """Rhino.Geometry.Cylinder representing bullet.

        Returns
        -------
        Rhino.Geometry.Cylinder
        """
        return rg.Cylinder(self.circle, self.compressed_height)

    @property
    def vector(self):
        # TODO: Find better name
        return self.plane.Normal * self.height - self.plane.Normal * self.compressed_height

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
        location = Frame.from_data(data.pop('_location'))

        trajectory_to = []
        for frame_data in data.pop('_trajectory_to'):
            trajectory_to.append(Frame.from_data(frame_data))

        trajectory_from = []
        for frame_data in data.pop('_trajectory_from'):
            trajectory_from.append(Frame.from_data(frame_data))

        # Take the rest of the dictionary
        kwargs = data

        return cls(location, trajectory_to=trajectory_to, trajectory_from=trajectory_from, **kwargs)

    def generate_mesh(self, face_count=18):
        """Generate mesh representation of bullet with custom resolution.

        Parameters
        ----------
        face_count : int, optional
            Desired number of faces, by default 18
            Used as a guide for the resolution of the mesh cylinder

        Returns
        -------
        Rhino.Geometry.Mesh
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
                    next_vkey = list_elem_w_index_wrap(vkeys, i + 1)
                    mesh.add_face([ckey, vkey, next_vkey])

        # generate faces between polygons
        vertex_for_vertex = zip(*outer_verts_polygons)

        for i, mirror_corners_1 in enumerate(vertex_for_vertex):
            mirror_corners_2 = list_elem_w_index_wrap(vertex_for_vertex, i + 1)
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
            raise Exception('Id {} appears more than once in list of ClayBullet instances'.format(id))
        set_of_ids.add(id)


class ClayBulletEncoder(json.JSONEncoder):
    """JSON encoder for :class:`ClayBullet`.

    Implemented from https://docs.python.org/3/library/json.html#json.JSONEncoder
    """

    def default(self, obj):
        if isinstance(obj, ClayBullet):
            return obj.__dict__
        if isinstance(obj, cg.Primitive):
            return obj.to_data()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
