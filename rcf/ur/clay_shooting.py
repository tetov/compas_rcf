from __future__ import division, absolute_import, print_function
import math as m

import Rhino.Geometry as rg

from compas.datastructures import Network
from compas.datastructures import Mesh as cg_Mesh
from compas_ghpython.artists import MeshArtist

from rcf import utils
from rcf.ur import ur_standard, comm, ur_utils

# UR movement
ROBOT_L_SPEED = 0.6  # m/s
ROBOT_ACCEL = 0.8  # m/s2
ROBOT_SAFE_SPEED = .8
ROBOT_J_SPEED = .8
BLEND_RADIUS_PUSHING = .002  # m

# Tool related variables
TOOL_HEIGHT = 192  # mm
ACTUATOR_IO = 4


def _get_offset_plane(initial_plane, dist, vertical_offset_bool):
    """
    generates an offset plane.
    archetypical use: generate entry or exit planes for robotic processes.
    """

    plane_normal = initial_plane.Normal

    if vertical_offset_bool:
        directions = [rg.Vector3d(0, 0, -1), plane_normal]
    else:
        directions = [plane_normal, plane_normal]

    entry_plane = initial_plane.Clone()
    exit_plane = initial_plane.Clone()

    entry_plane.Translate(directions[0] * dist)
    exit_plane.Translate(directions[1] * dist)

    return entry_plane, exit_plane


def _default_movel(plane, blend_radius=0):
    return ur_standard.move_l(plane, ROBOT_L_SPEED, ROBOT_ACCEL, blend_radius=blend_radius)


def _picking_moves(plane, entry_exit_offset, rotation, vertical_offset_bool):
    script = ""

    entry_plane, exit_plane = _get_offset_plane(plane, entry_exit_offset, vertical_offset_bool)

    if rotation > 0:
        rotated_plane = plane.Clone()
        rotated_plane.Rotate(m.radians(rotation), plane.Normal)

    script += _default_movel(entry_plane)
    script += _default_movel(plane)
    if rotation > 0:
        script += _default_movel(rotated_plane)
    script += _default_movel(exit_plane)

    return script


def _shooting_moves(plane, entry_exit_offset, push_conf, vertical_offset_bool, sleep=.5):
    script = ""

    entry_plane, exit_plane = _get_offset_plane(plane, entry_exit_offset, vertical_offset_bool)

    script += _default_movel(entry_plane)
    script += _default_movel(plane)

    script += ur_standard.set_digital_out(ACTUATOR_IO, True)
    script += ur_standard.sleep(sleep)

    if push_conf['pushing']:
        script += _push_moves(plane, push_conf, vertical_offset_bool)

    script += _default_movel(exit_plane)

    script += ur_standard.set_digital_out(ACTUATOR_IO, False)

    return script


def _push_moves(plane, push_conf, vertical_offset_bool):

    n = push_conf['n_pushes']
    dist = push_conf['push_offsets']
    angle_step = push_conf['angle_steps']
    rot_axis = push_conf['push_rotation_axis']

    script = ""

    offset_plane = plane.Clone()
    if vertical_offset_bool:
        direction = rg.Vector3d(0, 0, -1)
    else:
        direction = plane.Normal

    offset_plane.Translate(direction * -dist)

    for i in range(n):
        rot_plane = offset_plane.Clone()

        rot_plane.Rotate(m.radians((i + 1) * angle_step), rot_axis, plane.Origin)

        script += _default_movel(rot_plane, blend_radius=BLEND_RADIUS_PUSHING)

    return script


def _safe_travel_moves(safe_pos_list, reverse=False):

    if reverse:
        safe_pos_list = safe_pos_list[::-1]

    script = ""
    for safe_pos in safe_pos_list:
        script += ur_standard.move_j(safe_pos, ROBOT_SAFE_SPEED, ROBOT_ACCEL)

    return script


def clay_shooting(picking_planes,
                  placing_planes,
                  safe_pos_list,
                  dry_run=False,
                  push_conf={'pushing': [False]},
                  tool_rotation=0,
                  picking_rotation=0,
                  tool_height_correction=0,
                  z_calib_picking=0,
                  z_calib_placing=0,
                  entry_exit_offset=-40,
                  vertical_offset_bool=False,
                  viz_planes_bool=False,
                  placing_index=0):

    reload(comm)  # noqa E0602
    reload(ur_standard)  # noqa E0602

    # extract planes if input is ClayBullets
    if not is_elems_rgPlane(placing_planes):
        placing_planes = [bullet.plane.Clone() for bullet in placing_planes]

    # Create a string object to store script
    script = ""

    # set tcp
    tool_height = TOOL_HEIGHT + tool_height_correction
    script += ur_standard.set_tcp_by_plane_angles(0, 0, tool_height, 0.0, 0.0, m.radians(tool_rotation))
    # Ensure actuator is retracted ###
    script += ur_standard.set_digital_out(ACTUATOR_IO, False)

    # Send Robot to an initial known configuration ###
    script += ur_standard.move_j(safe_pos_list[0], ROBOT_ACCEL, ROBOT_SAFE_SPEED)

    # setup instructions

    for key, value in push_conf.iteritems():
        if value is None:
            continue
        if len(value) == len(placing_planes) or len(value) == 1:
            continue

        raise Exception('Mismatched between {} list and placing_plane list'.format(key))

    instructions = []
    for i, placing_plane in enumerate(placing_planes):
        instruction = []

        picking_plane = utils.list_elem_w_index_wrap(picking_planes, i)
        instruction.append(picking_plane)

        instruction.append(placing_plane)

        plane_push_conf = {}

        for key, value in push_conf.iteritems():
            if value is not None:
                list_elem = utils.list_elem_w_index_wrap(value, i)
                plane_push_conf.update({key: list_elem})
            else:
                plane_push_conf.update({key: None})

        instruction.append(plane_push_conf)

        instructions.append(instruction)

    # Start general clay fabrication process ###
    for i, instruction in enumerate(instructions):
        picking_plane, placing_plane, push_conf = instruction

        # Pick clay
        if not dry_run:
            # apply z calibration specific to picking station
            picking_plane.Translate(rg.Vector3d(0, 0, z_calib_picking))

            script += _picking_moves(picking_plane, entry_exit_offset, picking_rotation, vertical_offset_bool)

        # safe moves
        script += _safe_travel_moves(safe_pos_list)

        # apply z calibration specific to placing station
        placing_plane.Translate(rg.Vector3d(0, 0, z_calib_placing))

        script += _shooting_moves(placing_plane, entry_exit_offset, push_conf, vertical_offset_bool)
        script += ur_standard.UR_log('Bullet {} placed.'.format(i + placing_index))

        # safe moves
        script += _safe_travel_moves(safe_pos_list, reverse=True)

    if viz_planes_bool:
        viz_planes = ur_utils.visualize_ur_script(script)
    else:
        viz_planes = None

    return comm.concatenate_script(script), viz_planes


def is_elems_rgPlane(obj):
    """ From https://stackoverflow.com/a/18495146
    """
    return bool(obj) and all(isinstance(elem, rg.Plane) for elem in obj)


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
        return m.pi * self.radius**2 * self.height

    @property
    def volume_m3(self):
        return self.volume * 1000

    @property
    def compressed_radius(self):
        return m.sqrt(self.volume / (self.compressed_height * m.pi))

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
            raise Exception('No attributes to set')

        keys = []
        for u, v in self.edges():
            if self.edge_length(u, v) >= dist:
                keys.append((u, v))

        self.set_edges_attributes(kwargs.keys(), kwargs.values(), keys=keys)

    def _bullet_neighboors_below(self, u):
        z_value = self.get_vertex_attribute(u, 'z')
        bullets_below = self.vertices_where({'z': (0, z_value)})

        bullets_below_keys = [(u, v) for v in bullets_below if v != u]
        for u, v in bullets_below_keys:
            if self.edge_length(u, v) <= 20:
                self.add_edge(u, v, relation='neighboor_below', is_touching=True)

    def network_from_clay_bullets(self, clay_bullets):
        for i, clay_bullet in enumerate(clay_bullets):
            self.add_vertex(key=i,
                            x=clay_bullet.plane.Origin.X,
                            y=clay_bullet.plane.Origin.Y,
                            z=clay_bullet.plane.Origin.Z,
                            class_instance=clay_bullet)

        # edges_by_dists = (self._edges_from_distance(i, c) for i, c in enumerate(clay_bullets))

        edges_from_order = [(i, i + 1) for i in range(len(clay_bullets) - 1)]

        for u, v in edges_from_order:
            pass
            # self.add_edge(u, v, relation='print_order', is_touching=True)

        # TODO: Better distance value
        self._set_attributes_edges_longer_than(26, is_touching=False)

        for i in range(len(self._clay_bullets)):
            self._bullet_neighboors_below(i)
