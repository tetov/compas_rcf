from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import Network


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
            self.add_edge(u, v, relation='print_order', is_touching=True)

        # TODO: Better distance value
        self._set_attributes_edges_longer_than(26, is_touching=False)

        for i in range(len(self._clay_bullets)):
            self._bullet_neighboors_below(i)
