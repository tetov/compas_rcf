from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import math

import compas.geometry as cg
from compas.datastructures import Mesh as cg_Mesh
from compas.geometry import Frame
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
    plane: Rhino.Geometry.Plane
        The origin plane of the cylinder.
    radius : float, optional
        The radius of the initial cylinder.
    height : float, optional
        The height of the initial cylinder.
    compression_ratio : float (>0, <=1), optional
        The ratio of compression applied to the initial cylinder.
    """
    def __init__(self,
                 placement_frame,
                 pre_frames=[],
                 post_frames=[],
                 radius=40,
                 height=200,
                 compression_ratio=1,
                 tool=None):
        self.placement_frame = placement_frame  # property & setter to convert planes to frames
        self.pre_frames = pre_frames  # property & setter to convert planes to frames
        self.post_frames = post_frames  # property & setter to convert planes to frames

        self.radius = radius
        self.height = height
        self.compression_ratio = compression_ratio
        self.tool = tool

    @property
    def placement_frame(self):
        return self._placement_frame

    @placement_frame.setter
    def placement_frame(self, frame_like):
        self._placement_frame = ensure_frame(frame_like)

    @property
    def pre_frames(self):
        return self._pre_frames

    @pre_frames.setter
    def pre_frames(self, frame_list):
        self._pre_frames = []
        for frame_like in frame_list:
            frame = ensure_frame(frame_like)
            self._pre_frames.append(frame)

    @property
    def post_frames(self):
        return self._post_frames

    @post_frames.setter
    def post_frames(self, frame_list):
        self._post_frames = []
        for frame_like in frame_list:
            frame = ensure_frame(frame_like)
            self._post_frames.append(frame)

    @property
    def plane(self):
        """ For Compatibility with older scripts
        """
        return self.placement_plane

    @property
    def placement_plane(self):
        return cgframe_to_rgplane(self.placement_frame)

    @property
    def pre_planes(self):
        return [cgframe_to_rgplane(frame) for frame in self.pre_frames]

    @property
    def post_planes(self):
        return [cgframe_to_rgplane(frame) for frame in self.post_planes]

    @property
    def volume(self):
        return math.pi * self.radius**2 * self.height

    @property
    def volume_m3(self):
        return self.volume * 1000

    @property
    def compressed_radius(self):
        return math.sqrt(self.volume / (self.compressed_height * math.pi))

    @property
    def compressed_height(self):
        return self.height * self.compression_ratio

    @property
    def circle(self):
        return rg.Circle(self.plane, self.compressed_radius)

    @property
    def cylinder(self):
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

        placement_frame = Frame.from_data(data.pop('_placement_frame'))

        pre_frames = []
        for frame_data in data.pop('_pre_frames'):
            pre_frames.append(Frame.from_data(frame_data))

        post_frames = []
        for frame_data in data.pop('_post_frames'):
            post_frames.append(Frame.from_data(frame_data))

        # Take the rest of the dictionary
        kwargs = data

        return cls(placement_frame, pre_frames=pre_frames, post_frames=post_frames, **kwargs)

    def generate_mesh(self, face_count=18):
        """Generate mesh representation of bullet with custom resolution

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


class ClayBulletEncoder(json.JSONEncoder):
    """ JSON encoder for :class:ClayBullet
        Implemented from https://docs.python.org/3/library/json.html#json.JSONEncoder
    """
    def default(self, obj):
        if isinstance(obj, ClayBullet):
            return obj.__dict__
        if isinstance(obj, cg.Primitive):
            return obj.to_data()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
