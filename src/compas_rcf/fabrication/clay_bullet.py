from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math

import Rhino.Geometry as rg

from compas_rcf import utils

from compas.datastructures import Mesh as cg_Mesh
from compas_ghpython.artists import MeshArtist


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
    def __init__(self, plane, radius=40, height=200, compression_ratio=1):
        self.plane = plane
        self.radius = radius
        self.height = height
        self.compression_ratio = compression_ratio

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
                    next_vkey = utils.list_elem_w_index_wrap(vkeys, i + 1)
                    mesh.add_face([ckey, vkey, next_vkey])

        # generate faces between polygons
        vertex_for_vertex = zip(*outer_verts_polygons)

        for i, mirror_corners_1 in enumerate(vertex_for_vertex):
            mirror_corners_2 = utils.list_elem_w_index_wrap(vertex_for_vertex, i + 1)
            mesh.add_face(mirror_corners_1 + mirror_corners_2[::-1])

        # to Rhino.Geometry and clean it up
        rg_mesh = MeshArtist(mesh).draw_mesh()
        rg_mesh.UnifyNormals()
        rg_mesh.Normals.ComputeNormals()

        return rg_mesh
